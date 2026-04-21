from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
from app.database import get_db
from app.models import Campaign, Task
from app.schemas import CampaignCreate, CampaignUpdate, CampaignResponse, TaskResponse

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("/", response_model=list[CampaignResponse])
async def list_campaigns(
    project_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Campaign).order_by(Campaign.created_at.desc())
    if project_id is not None:
        query = query.where(Campaign.project_id == project_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=CampaignResponse, status_code=201)
async def create_campaign(campaign_in: CampaignCreate, db: AsyncSession = Depends(get_db)):
    campaign = Campaign(**campaign_in.model_dump())
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Campaign)
        .options(selectinload(Campaign.tasks))
        .where(Campaign.id == campaign_id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(campaign_id: int, campaign_in: CampaignUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    update_data = campaign_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campaign, field, value)

    await db.commit()
    await db.refresh(campaign)
    return campaign


@router.delete("/{campaign_id}", status_code=204)
async def delete_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    await db.delete(campaign)
    await db.commit()


@router.post("/{campaign_id}/launch", response_model=TaskResponse)
async def launch_campaign(campaign_id: int, db: AsyncSession = Depends(get_db)):
    """Launch a campaign workflow by creating an orchestrator task."""
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    # Update campaign status to planning
    campaign.status = "planning"

    # Create orchestrator task
    task = Task(
        project_id=campaign.project_id,
        campaign_id=campaign.id,
        agent_type="orchestrator",
        task_type="launch_campaign",
        input_data=f'{{"campaign_id": {campaign.id}}}',
        priority=1,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
