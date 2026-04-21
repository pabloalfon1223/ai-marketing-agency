from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.database import get_db
from app.models import Task, AgentLog
from app.schemas import (
    AgentRunRequest,
    AgentStatusResponse,
    AgentLogResponse,
    TaskResponse,
)

router = APIRouter(tags=["agents"])

# Registry of known agent types
AGENT_REGISTRY = {
    "orchestrator": {
        "display_name": "Orchestrator Agent",
        "description": "Coordinates campaign workflows and delegates tasks to other agents",
    },
    "strategy": {
        "display_name": "Strategy Agent",
        "description": "Develops marketing strategies and campaign briefs",
    },
    "content_creator": {
        "display_name": "Content Creator Agent",
        "description": "Generates marketing content across platforms",
    },
    "seo": {
        "display_name": "SEO Agent",
        "description": "Analyzes and optimizes content for search engines",
    },
    "analytics": {
        "display_name": "Analytics Agent",
        "description": "Tracks performance metrics and generates reports",
    },
    "social_media": {
        "display_name": "Social Media Agent",
        "description": "Manages social media scheduling and engagement",
    },
}


@router.post("/agents/run", response_model=TaskResponse)
async def run_agent(request: AgentRunRequest, db: AsyncSession = Depends(get_db)):
    """Run a single agent task ad-hoc."""
    task = Task(
        agent_type=request.agent_type,
        task_type=request.task_type,
        project_id=request.project_id,
        campaign_id=request.campaign_id,
        input_data=request.input_data,
        priority=5,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/agents/status", response_model=list[AgentStatusResponse])
async def get_agent_status(db: AsyncSession = Depends(get_db)):
    """Return status of all agent types with running/completed counts."""
    statuses = []

    for agent_type, info in AGENT_REGISTRY.items():
        # Count completed tasks
        completed_result = await db.execute(
            select(func.count(Task.id)).where(
                Task.agent_type == agent_type,
                Task.status == "completed",
            )
        )
        tasks_completed = completed_result.scalar() or 0

        # Count running tasks
        running_result = await db.execute(
            select(func.count(Task.id)).where(
                Task.agent_type == agent_type,
                Task.status == "running",
            )
        )
        tasks_running = running_result.scalar() or 0

        statuses.append(
            AgentStatusResponse(
                agent_type=agent_type,
                display_name=info["display_name"],
                description=info["description"],
                status="busy" if tasks_running > 0 else "idle",
                tasks_completed=tasks_completed,
                tasks_running=tasks_running,
            )
        )

    return statuses


@router.get("/tasks", response_model=list[TaskResponse])
async def list_tasks(
    status: Optional[str] = Query(None),
    agent_type: Optional[str] = Query(None),
    campaign_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Task).order_by(Task.created_at.desc())
    if status is not None:
        query = query.where(Task.status == status)
    if agent_type is not None:
        query = query.where(Task.agent_type == agent_type)
    if campaign_id is not None:
        query = query.where(Task.campaign_id == campaign_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks/{task_id}/retry", response_model=TaskResponse)
async def retry_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """Retry a failed task by resetting its status to pending."""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "failed":
        raise HTTPException(status_code=400, detail="Only failed tasks can be retried")

    task.status = "pending"
    task.error_message = None
    task.started_at = None
    task.completed_at = None

    await db.commit()
    await db.refresh(task)
    return task


@router.get("/tasks/{task_id}/logs", response_model=list[AgentLogResponse])
async def get_task_logs(task_id: int, db: AsyncSession = Depends(get_db)):
    """Get agent logs for a specific task."""
    # Verify task exists
    task_result = await db.execute(select(Task).where(Task.id == task_id))
    if not task_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Task not found")

    result = await db.execute(
        select(AgentLog)
        .where(AgentLog.task_id == task_id)
        .order_by(AgentLog.created_at.asc())
    )
    return result.scalars().all()
