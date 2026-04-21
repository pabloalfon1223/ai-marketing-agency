from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Client, Project, Campaign, Content, Task

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
async def get_overview(db: AsyncSession = Depends(get_db)):
    """Return overall stats for the dashboard."""
    total_clients = (await db.execute(select(func.count(Client.id)))).scalar() or 0
    total_projects = (await db.execute(select(func.count(Project.id)))).scalar() or 0
    total_campaigns = (await db.execute(select(func.count(Campaign.id)))).scalar() or 0
    total_content = (await db.execute(select(func.count(Content.id)))).scalar() or 0

    # Tasks by status
    task_status_result = await db.execute(
        select(Task.status, func.count(Task.id)).group_by(Task.status)
    )
    tasks_by_status = {row[0]: row[1] for row in task_status_result.all()}

    # Content by status
    content_status_result = await db.execute(
        select(Content.status, func.count(Content.id)).group_by(Content.status)
    )
    content_by_status = {row[0]: row[1] for row in content_status_result.all()}

    return {
        "total_clients": total_clients,
        "total_projects": total_projects,
        "total_campaigns": total_campaigns,
        "total_content": total_content,
        "tasks_by_status": tasks_by_status,
        "content_by_status": content_by_status,
    }


@router.get("/project/{project_id}")
async def get_project_stats(project_id: int, db: AsyncSession = Depends(get_db)):
    """Return project-specific stats."""
    # Verify project exists
    project_result = await db.execute(select(Project).where(Project.id == project_id))
    project = project_result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Campaign count
    campaign_count = (
        await db.execute(
            select(func.count(Campaign.id)).where(Campaign.project_id == project_id)
        )
    ).scalar() or 0

    # Content count
    content_count = (
        await db.execute(
            select(func.count(Content.id)).where(Content.project_id == project_id)
        )
    ).scalar() or 0

    # Tasks by status for this project
    task_status_result = await db.execute(
        select(Task.status, func.count(Task.id))
        .where(Task.project_id == project_id)
        .group_by(Task.status)
    )
    tasks_by_status = {row[0]: row[1] for row in task_status_result.all()}

    # Content by status for this project
    content_status_result = await db.execute(
        select(Content.status, func.count(Content.id))
        .where(Content.project_id == project_id)
        .group_by(Content.status)
    )
    content_by_status = {row[0]: row[1] for row in content_status_result.all()}

    # Content by platform
    content_platform_result = await db.execute(
        select(Content.platform, func.count(Content.id))
        .where(Content.project_id == project_id)
        .group_by(Content.platform)
    )
    content_by_platform = {row[0]: row[1] for row in content_platform_result.all()}

    return {
        "project_id": project_id,
        "project_name": project.name,
        "total_campaigns": campaign_count,
        "total_content": content_count,
        "tasks_by_status": tasks_by_status,
        "content_by_status": content_by_status,
        "content_by_platform": content_by_platform,
    }


@router.get("/agents")
async def get_agent_stats(db: AsyncSession = Depends(get_db)):
    """Return per-agent-type stats."""
    # Tasks completed per agent type
    completed_result = await db.execute(
        select(Task.agent_type, func.count(Task.id))
        .where(Task.status == "completed")
        .group_by(Task.agent_type)
    )
    completed_by_agent = {row[0]: row[1] for row in completed_result.all()}

    # Total tasks per agent type
    total_result = await db.execute(
        select(Task.agent_type, func.count(Task.id))
        .group_by(Task.agent_type)
    )
    total_by_agent = {row[0]: row[1] for row in total_result.all()}

    # Failed tasks per agent type
    failed_result = await db.execute(
        select(Task.agent_type, func.count(Task.id))
        .where(Task.status == "failed")
        .group_by(Task.agent_type)
    )
    failed_by_agent = {row[0]: row[1] for row in failed_result.all()}

    # Build per-agent stats
    all_agents = set(total_by_agent.keys())
    agent_stats = []
    for agent_type in sorted(all_agents):
        total = total_by_agent.get(agent_type, 0)
        completed = completed_by_agent.get(agent_type, 0)
        failed = failed_by_agent.get(agent_type, 0)
        success_rate = round((completed / total) * 100, 1) if total > 0 else 0.0

        agent_stats.append({
            "agent_type": agent_type,
            "total_tasks": total,
            "tasks_completed": completed,
            "tasks_failed": failed,
            "success_rate": success_rate,
            "avg_duration": None,  # Placeholder - implement when timing data is available
        })

    return agent_stats
