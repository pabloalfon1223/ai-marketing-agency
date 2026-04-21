"""Orchestrator Agent -- coordinates specialist agents and manages workflow."""

import json

from app.agents.base import BaseAgent
from app.agents.tool_registry import ALL_TOOLS
from app.models import Task


class OrchestratorAgent(BaseAgent):
    agent_type = "orchestrator"
    display_name = "Orchestrator Agent"
    description = (
        "Lead marketing strategist and project coordinator that breaks down campaign "
        "briefs into tasks for specialized agents and compiles their results."
    )
    system_prompt = (
        "You are the lead marketing strategist and project coordinator for an AI-powered "
        "marketing agency. You manage a team of specialist agents and are responsible for "
        "turning high-level campaign briefs into a structured execution plan.\n\n"
        "Your specialist agents are:\n"
        "- strategy: Market analysis, competitive research, SWOT, and strategic planning.\n"
        "- content: Blog posts, articles, landing pages, and general copywriting.\n"
        "- seo: Keyword research, content scoring, and SEO optimization.\n"
        "- social_media: Platform-specific social posts and content calendars.\n"
        "- email_marketing: Email sequences, nurture campaigns, and newsletters.\n"
        "- analytics: KPI setup, performance reporting, and data analysis.\n"
        "- branding: Brand voice, personality, messaging pillars, and guidelines.\n"
        "- advertising: Paid ad campaigns, ad copy, targeting, and budget allocation.\n\n"
        "When you receive a campaign brief, follow this workflow:\n"
        "1. Analyze the brief to understand the client's goals, audience, budget, and timeline.\n"
        "2. Break the project into discrete, well-scoped tasks for the appropriate specialist agents.\n"
        "3. Determine the correct execution order -- some tasks depend on outputs from others "
        "(e.g., branding before content, strategy before advertising).\n"
        "4. Use delegate_task to assign each task to the right agent with clear, detailed input_data "
        "that includes all context the agent needs to succeed.\n"
        "5. Set priorities (1 = highest) to ensure critical-path tasks are executed first.\n"
        "6. After all tasks are delegated, use compile_results to produce an executive summary "
        "that ties all agent outputs together into a cohesive campaign plan.\n\n"
        "Be strategic about task ordering. For example, run branding and strategy tasks first so "
        "their outputs can inform content, social media, email, and advertising tasks. Always "
        "include sufficient context in each delegated task so agents can work independently."
    )
    tools = ALL_TOOLS["orchestrator"]

    async def _handle_tool_call(
        self, task: Task, tool_name: str, tool_input: dict
    ) -> dict:
        if tool_name == "delegate_task":
            subtask = Task(
                project_id=task.project_id,
                campaign_id=task.campaign_id,
                agent_type=tool_input["agent_type"],
                task_type=tool_input["task_type"],
                input_data=tool_input["input_data"],
                priority=tool_input.get("priority", 5),
                parent_task_id=task.id,
                status="pending",
            )
            self.db.add(subtask)
            await self.db.commit()
            await self.db.refresh(subtask)
            return {
                "status": "ok",
                "data": {
                    "delegate_task": {
                        "task_id": subtask.id,
                        "agent_type": subtask.agent_type,
                        "task_type": subtask.task_type,
                        "status": subtask.status,
                    }
                },
            }

        if tool_name == "compile_results":
            return {"status": "ok", "data": {"compile_results": tool_input}}

        return await super()._handle_tool_call(task, tool_name, tool_input)
