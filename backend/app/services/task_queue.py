import asyncio
import json
import logging
from datetime import datetime, timezone
from sqlalchemy import select
from app.database import async_session
from app.agents.claude_client import ClaudeClient
from app.models import Task

logger = logging.getLogger(__name__)


class TaskQueue:
    def __init__(self):
        self._queue: asyncio.Queue = asyncio.Queue()
        self._workers: list[asyncio.Task] = []
        self._running = False
        self._claude_client: ClaudeClient | None = None

    async def start(self, num_workers: int = 3):
        """Start worker coroutines."""
        from app.config import get_settings
        settings = get_settings()
        self._claude_client = ClaudeClient()
        self._running = True
        for i in range(num_workers):
            worker = asyncio.create_task(self._worker(i))
            self._workers.append(worker)
        logger.info(f"TaskQueue started with {num_workers} workers")

    async def stop(self):
        self._running = False
        for w in self._workers:
            w.cancel()
        self._workers.clear()

    async def enqueue(self, task_id: int):
        await self._queue.put(task_id)
        logger.info(f"Task {task_id} enqueued")

    async def _worker(self, worker_id: int):
        while self._running:
            try:
                task_id = await asyncio.wait_for(self._queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

            logger.info(f"Worker {worker_id} processing task {task_id}")
            async with async_session() as db:
                try:
                    task = await db.get(Task, task_id)
                    if not task or task.status != "pending":
                        continue

                    task.status = "running"
                    task.started_at = datetime.now(timezone.utc)
                    await db.commit()

                    # Broadcast status update via WebSocket
                    await self._broadcast_update(task)

                    # Get the right agent
                    agent = self._get_agent(task.agent_type, db)
                    if not agent:
                        task.status = "failed"
                        task.error_message = f"Unknown agent type: {task.agent_type}"
                        await db.commit()
                        continue

                    # Execute the agent
                    result = await agent.execute(task)

                    task.output_data = json.dumps(result)
                    task.status = "completed"
                    task.completed_at = datetime.now(timezone.utc)
                    await db.commit()

                    # Broadcast completion
                    await self._broadcast_update(task)

                    # Check if this task has a campaign - trigger workflow engine
                    if task.campaign_id and task.parent_task_id:
                        from app.services.workflow_engine import workflow_engine
                        await workflow_engine.on_task_completed(task, db)

                except Exception as e:
                    logger.exception(f"Worker {worker_id} error on task {task_id}")
                    task = await db.get(Task, task_id)
                    if task:
                        task.status = "failed"
                        task.error_message = str(e)
                        task.completed_at = datetime.now(timezone.utc)
                        await db.commit()
                        await self._broadcast_update(task)

    def _get_agent(self, agent_type: str, db):
        from app.agents import AGENT_MAP
        agent_class = AGENT_MAP.get(agent_type)
        if not agent_class:
            return None
        return agent_class(self._claude_client, db)

    async def _broadcast_update(self, task: Task):
        try:
            from app.api.websocket import manager
            await manager.broadcast_task_update(task.id, task.status, task.agent_type)
        except Exception:
            pass  # WebSocket errors shouldn't break task processing


# Singleton instance
task_queue = TaskQueue()
