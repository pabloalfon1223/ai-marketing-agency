import json
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Task, Campaign
from app.services.task_queue import task_queue

logger = logging.getLogger(__name__)

# Workflow definitions - each step can depend on other steps
WORKFLOWS = {
    "full_campaign": [
        {"step": 1, "agent": "strategy", "task": "create_strategy_brief", "depends_on": []},
        {"step": 2, "agent": "branding", "task": "define_brand_voice", "depends_on": [1]},
        {"step": 3, "agent": "seo", "task": "keyword_research", "depends_on": [1]},
        {"step": 4, "agent": "content", "task": "generate_content", "depends_on": [2, 3]},
        {"step": 5, "agent": "seo", "task": "score_content", "depends_on": [4]},
        {"step": 6, "agent": "social_media", "task": "create_calendar", "depends_on": [4]},
        {"step": 7, "agent": "email_marketing", "task": "create_sequence", "depends_on": [2, 4]},
        {"step": 8, "agent": "advertising", "task": "create_ad_plan", "depends_on": [1, 3]},
        {"step": 9, "agent": "analytics", "task": "setup_kpis", "depends_on": [1]},
    ],
    "content_only": [
        {"step": 1, "agent": "seo", "task": "keyword_research", "depends_on": []},
        {"step": 2, "agent": "content", "task": "generate_content", "depends_on": [1]},
        {"step": 3, "agent": "seo", "task": "score_content", "depends_on": [2]},
    ],
    "social_campaign": [
        {"step": 1, "agent": "strategy", "task": "audience_analysis", "depends_on": []},
        {"step": 2, "agent": "content", "task": "generate_social_posts", "depends_on": [1]},
        {"step": 3, "agent": "social_media", "task": "create_calendar", "depends_on": [2]},
    ],
    "email_campaign": [
        {"step": 1, "agent": "strategy", "task": "audience_analysis", "depends_on": []},
        {"step": 2, "agent": "branding", "task": "define_brand_voice", "depends_on": [1]},
        {"step": 3, "agent": "email_marketing", "task": "create_sequence", "depends_on": [1, 2]},
    ],
    "ads_campaign": [
        {"step": 1, "agent": "strategy", "task": "create_strategy_brief", "depends_on": []},
        {"step": 2, "agent": "seo", "task": "keyword_research", "depends_on": [1]},
        {"step": 3, "agent": "advertising", "task": "create_ad_plan", "depends_on": [1, 2]},
    ],
}


class WorkflowEngine:
    async def launch_workflow(self, workflow_name: str, campaign_id: int,
                              project_id: int, input_data: dict, db: AsyncSession) -> list[Task]:
        """Launch a complete workflow for a campaign."""
        workflow = WORKFLOWS.get(workflow_name)
        if not workflow:
            # Default to full campaign
            workflow = WORKFLOWS["full_campaign"]

        # Determine workflow type from campaign_type if workflow_name not specified
        tasks_created = []
        step_to_task = {}  # step number -> Task object

        # Create all task records first (pending state)
        for step in workflow:
            step_input = {
                **input_data,
                "workflow_step": step["step"],
                "workflow_name": workflow_name,
            }

            task = Task(
                project_id=project_id,
                campaign_id=campaign_id,
                agent_type=step["agent"],
                task_type=step["task"],
                input_data=json.dumps(step_input),
                status="pending",
                priority=step["step"],  # Earlier steps = higher priority
            )
            db.add(task)
            await db.flush()  # Get the ID
            step_to_task[step["step"]] = task
            tasks_created.append(task)

        # Set parent_task_id for dependency tracking (use first dependency as parent)
        for step in workflow:
            if step["depends_on"]:
                task = step_to_task[step["step"]]
                task.parent_task_id = step_to_task[step["depends_on"][0]].id

        await db.commit()

        # Store step mapping in memory for dependency resolution
        # We need a way to track which steps map to which tasks
        # Store this on the campaign's strategy_brief as metadata
        step_mapping = {str(s): t.id for s, t in step_to_task.items()}
        campaign = await db.get(Campaign, campaign_id)
        if campaign:
            existing = json.loads(campaign.strategy_brief) if campaign.strategy_brief else {}
            existing["_workflow_step_mapping"] = step_mapping
            existing["_workflow_name"] = workflow_name
            campaign.strategy_brief = json.dumps(existing)
            await db.commit()

        # Enqueue tasks that have no dependencies (step 1s)
        for step in workflow:
            if not step["depends_on"]:
                await task_queue.enqueue(step_to_task[step["step"]].id)

        return tasks_created

    async def on_task_completed(self, completed_task: Task, db: AsyncSession):
        """Called when a task completes. Check if dependent tasks can now run."""
        if not completed_task.campaign_id:
            return

        campaign = await db.get(Campaign, completed_task.campaign_id)
        if not campaign or not campaign.strategy_brief:
            return

        try:
            meta = json.loads(campaign.strategy_brief)
        except json.JSONDecodeError:
            return

        step_mapping = meta.get("_workflow_step_mapping", {})
        workflow_name = meta.get("_workflow_name", "full_campaign")
        workflow = WORKFLOWS.get(workflow_name, WORKFLOWS["full_campaign"])

        # Find which step just completed
        task_to_step = {int(v): int(k) for k, v in step_mapping.items()}
        completed_step = task_to_step.get(completed_task.id)
        if completed_step is None:
            return

        # Inject completed task's output as dependency data for dependent tasks
        for step in workflow:
            if completed_step in step["depends_on"]:
                task_id = step_mapping.get(str(step["step"]))
                if not task_id:
                    continue

                dependent_task = await db.get(Task, int(task_id))
                if not dependent_task or dependent_task.status != "pending":
                    continue

                # Check if ALL dependencies are completed
                all_deps_done = True
                dep_outputs = {}
                for dep_step in step["depends_on"]:
                    dep_task_id = step_mapping.get(str(dep_step))
                    if dep_task_id:
                        dep_task = await db.get(Task, int(dep_task_id))
                        if not dep_task or dep_task.status != "completed":
                            all_deps_done = False
                            break
                        if dep_task.output_data:
                            dep_outputs[dep_task.agent_type] = json.loads(dep_task.output_data)

                if all_deps_done:
                    # Inject dependency outputs into task input
                    input_data = json.loads(dependent_task.input_data) if dependent_task.input_data else {}
                    input_data["dependencies"] = dep_outputs
                    dependent_task.input_data = json.dumps(input_data)
                    await db.commit()

                    await task_queue.enqueue(dependent_task.id)
                    logger.info(f"Enqueued dependent task {dependent_task.id} (step {step['step']})")

        # Check if all tasks in the workflow are completed
        all_completed = True
        for step_num, tid in step_mapping.items():
            t = await db.get(Task, int(tid))
            if t and t.status not in ("completed", "failed"):
                all_completed = False
                break

        if all_completed and campaign:
            campaign.status = "completed" if campaign.status == "planning" else campaign.status
            await db.commit()


# Singleton
workflow_engine = WorkflowEngine()
