from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from datetime import datetime, timezone
from app.models import Idea
from app.database import get_db
from typing import Optional

router = APIRouter()


@router.post("/ideas")
async def create_idea(
    title: str,
    description: str,
    type: str,
    target_market: str,
    revenue_model: str,
    initial_capital_required: float,
    db: AsyncSession = Depends(get_db)
):
    """Create new idea for Cerebro"""
    try:
        idea = Idea(
            title=title,
            description=description,
            type=type,
            target_market=target_market,
            revenue_model=revenue_model,
            initial_capital_required=initial_capital_required,
            status="idea_cruda"
        )
        db.add(idea)
        await db.commit()
        await db.refresh(idea)
        return {"status": "ok", "idea_id": idea.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/ideas/{idea_id}")
async def get_idea(idea_id: int, db: AsyncSession = Depends(get_db)):
    """Get idea by ID"""
    stmt = select(Idea).where(Idea.id == idea_id)
    result = await db.execute(stmt)
    idea = result.scalar_one_or_none()

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    return {
        "id": idea.id,
        "title": idea.title,
        "type": idea.type,
        "overall_score": idea.overall_score,
        "status": idea.status,
        "estimated_time_to_20k": idea.estimated_time_to_20k,
        "initial_capital_required": idea.initial_capital_required,
        "current_monthly_revenue": idea.current_monthly_revenue,
        "created_at": idea.created_at
    }


@router.put("/ideas/{idea_id}/validate")
async def validate_idea(
    idea_id: int,
    demand_score: float,
    scalability_score: float,
    competition_score: float,
    demand_evidence: str,
    competitor_analysis: str,
    db: AsyncSession = Depends(get_db)
):
    """Update idea validation scores"""
    stmt = select(Idea).where(Idea.id == idea_id)
    result = await db.execute(stmt)
    idea = result.scalar_one_or_none()

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    idea.demand_score = demand_score
    idea.scalability_score = scalability_score
    idea.competition_score = competition_score
    idea.overall_score = (demand_score * 0.4 + scalability_score * 0.4 + competition_score * 0.2)
    idea.demand_evidence = demand_evidence
    idea.competitor_analysis = competitor_analysis
    idea.status = "en_validacion"
    idea.validation_started_at = datetime.now(timezone.utc)
    idea.last_update_at = datetime.now(timezone.utc)
    idea.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(idea)
    return {
        "status": "ok",
        "overall_score": idea.overall_score,
        "idea_status": idea.status
    }


@router.put("/ideas/{idea_id}/status")
async def update_idea_status(
    idea_id: int,
    status: str,
    learnings: Optional[str] = None,
    current_monthly_revenue: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    """Update idea status"""
    stmt = select(Idea).where(Idea.id == idea_id)
    result = await db.execute(stmt)
    idea = result.scalar_one_or_none()

    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")

    idea.status = status
    if status == "mvp_en_desarrollo":
        idea.mvp_launch_date = datetime.now(timezone.utc)
    if learnings:
        idea.learnings = learnings
    if current_monthly_revenue is not None:
        idea.current_monthly_revenue = current_monthly_revenue
        if current_monthly_revenue >= 20000:
            idea.reached_20k = "yes"
    idea.last_update_at = datetime.now(timezone.utc)
    idea.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(idea)
    return {"status": "ok", "idea_status": idea.status}


@router.get("/ideas/list/by-score")
async def get_ideas_by_score(
    min_score: float = 0,
    max_score: float = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get ideas ordered by score"""
    stmt = select(Idea).where(
        and_(Idea.overall_score >= min_score, Idea.overall_score <= max_score)
    ).order_by(desc(Idea.overall_score))
    result = await db.execute(stmt)
    ideas = result.scalars().all()

    return [
        {
            "id": i.id,
            "title": i.title,
            "type": i.type,
            "overall_score": i.overall_score,
            "status": i.status,
            "initial_capital_required": i.initial_capital_required,
            "estimated_time_to_20k": i.estimated_time_to_20k
        }
        for i in ideas
    ]


@router.get("/ideas/list/active")
async def get_active_ideas(db: AsyncSession = Depends(get_db)):
    """Get ideas in validation or development"""
    stmt = select(Idea).where(
        Idea.status.in_(["en_validacion", "mvp_diseñado", "mvp_en_desarrollo", "mvp_validando", "track_a_20k"])
    ).order_by(desc(Idea.overall_score))
    result = await db.execute(stmt)
    ideas = result.scalars().all()

    return [
        {
            "id": i.id,
            "title": i.title,
            "type": i.type,
            "overall_score": i.overall_score,
            "status": i.status,
            "current_monthly_revenue": i.current_monthly_revenue or 0
        }
        for i in ideas
    ]
