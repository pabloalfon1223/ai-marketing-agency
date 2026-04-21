from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.models import Content, Task
from app.schemas import (
    ContentCreate,
    ContentUpdate,
    ContentResponse,
    ContentStatusUpdate,
    TaskResponse,
)

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/", response_model=list[ContentResponse])
async def list_content(
    campaign_id: Optional[int] = Query(None),
    project_id: Optional[int] = Query(None),
    content_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Content).order_by(Content.created_at.desc())
    if campaign_id is not None:
        query = query.where(Content.campaign_id == campaign_id)
    if project_id is not None:
        query = query.where(Content.project_id == project_id)
    if content_type is not None:
        query = query.where(Content.content_type == content_type)
    if status is not None:
        query = query.where(Content.status == status)
    if platform is not None:
        query = query.where(Content.platform == platform)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(content_id: int, content_in: ContentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    update_data = content_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(content, field, value)

    await db.commit()
    await db.refresh(content)
    return content


@router.patch("/{content_id}/status", response_model=ContentResponse)
async def update_content_status(
    content_id: int,
    status_update: ContentStatusUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Approve or reject content."""
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if status_update.status not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")

    content.status = status_update.status
    if status_update.review_notes is not None:
        content.review_notes = status_update.review_notes

    await db.commit()
    await db.refresh(content)
    return content


@router.post("/{content_id}/regenerate", response_model=TaskResponse)
async def regenerate_content(content_id: int, db: AsyncSession = Depends(get_db)):
    """Regenerate content by creating a new content agent task."""
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Reset content status to draft
    content.status = "draft"

    # Create a content agent task
    task = Task(
        project_id=content.project_id,
        campaign_id=content.campaign_id,
        agent_type="content_creator",
        task_type="regenerate_content",
        input_data=f'{{"content_id": {content.id}, "content_type": "{content.content_type}", "platform": "{content.platform}"}}',
        priority=3,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
