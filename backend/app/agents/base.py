import json
import logging
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.claude_client import ClaudeClient
from app.models import AgentLog, Content, Task

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all marketing-agency agents.

    Subclasses must set ``agent_type``, ``system_prompt``, and ``tools`` (from
    :pymod:`app.agents.tool_registry`).  Override ``_handle_tool_call`` for
    custom persistence logic.
    """

    agent_type: str = ""
    display_name: str = ""
    description: str = ""
    system_prompt: str = ""
    tools: list[dict] = []
    model: str | None = None  # None -> use default from settings

    def __init__(self, claude_client: ClaudeClient, db: AsyncSession):
        self.claude = claude_client
        self.db = db

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    async def execute(self, task: Task) -> dict:
        """Run the agentic loop with tool_use until the model stops."""
        await self._log(
            task, "info", f"Starting {self.agent_type} agent for task: {task.task_type}"
        )

        messages = self._build_messages(task)
        result: dict = {}
        max_iterations = 10

        for _i in range(max_iterations):
            # Build the API kwargs, omitting optional fields when empty
            api_kwargs: dict = {
                "max_tokens": 4096,
                "system": self.system_prompt,
                "messages": messages,
            }
            if self.model is not None:
                api_kwargs["model"] = self.model
            if self.tools:
                api_kwargs["tools"] = self.tools

            response = await self.claude.create(**api_kwargs)

            # Check for tool-use blocks in the response
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

            if tool_use_blocks:
                tool_results = []
                for tool_block in tool_use_blocks:
                    await self._log(task, "info", f"Tool call: {tool_block.name}")
                    tool_result = await self._handle_tool_call(
                        task, tool_block.name, tool_block.input
                    )
                    result.update(tool_result.get("data", {}))
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_block.id,
                            "content": json.dumps(tool_result),
                        }
                    )

                # Feed assistant response + tool results back into the conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})
            else:
                # Final text response -- extract summary and break
                text_blocks = [b for b in response.content if hasattr(b, "text")]
                if text_blocks:
                    result["summary"] = text_blocks[0].text
                break

        await self._log(
            task, "info", f"Agent {self.agent_type} completed task {task.task_type}"
        )
        return result

    # ------------------------------------------------------------------
    # Message construction
    # ------------------------------------------------------------------

    def _build_messages(self, task: Task) -> list:
        """Build the initial message list from *task.input_data*."""
        input_data: dict = json.loads(task.input_data) if task.input_data else {}

        parts: list[str] = []
        if input_data.get("context"):
            parts.append(f"Context:\n{input_data['context']}")
        if input_data.get("brief"):
            parts.append(f"Brief:\n{input_data['brief']}")
        if input_data.get("instructions"):
            parts.append(f"Instructions:\n{input_data['instructions']}")
        if input_data.get("client_info"):
            parts.append(
                f"Client Info:\n{json.dumps(input_data['client_info'], indent=2)}"
            )
        if input_data.get("dependencies"):
            parts.append(
                f"Previous Agent Results:\n{json.dumps(input_data['dependencies'], indent=2)}"
            )

        # Fall back to raw JSON when no structured keys are present
        if not parts:
            parts.append(
                json.dumps(input_data) if input_data else "Execute the assigned task."
            )

        return [{"role": "user", "content": "\n\n".join(parts)}]

    # ------------------------------------------------------------------
    # Tool handling
    # ------------------------------------------------------------------

    async def _handle_tool_call(
        self, task: Task, tool_name: str, tool_input: dict
    ) -> dict:
        """Process a tool call.  Override in subclasses for custom logic."""
        return {"status": "ok", "data": {tool_name: tool_input}}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _log(
        self, task: Task, level: str, message: str, metadata: dict | None = None
    ):
        """Persist a log entry to the database."""
        log = AgentLog(
            task_id=task.id,
            agent_type=self.agent_type,
            log_level=level,
            message=message,
            metadata_=json.dumps(metadata) if metadata else None,
        )
        self.db.add(log)
        await self.db.commit()

    async def _save_content(
        self,
        task: Task,
        title: str,
        body: str,
        content_type: str,
        platform: str | None = None,
        meta_description: str | None = None,
    ) -> Content:
        """Convenience method to persist generated content."""
        content = Content(
            project_id=task.project_id,
            campaign_id=task.campaign_id,
            content_type=content_type,
            title=title,
            body=body,
            platform=platform,
            status="review",
            agent_id=self.agent_type,
        )
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)
        return content
