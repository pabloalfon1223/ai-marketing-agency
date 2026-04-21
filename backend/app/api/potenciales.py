from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.models.potencial import Potencial
from app.schemas.potencial import PotencialCreate, PotencialUpdate, PotencialResponse
from app.database import get_db
from typing import List, Optional

router = APIRouter(prefix="/api/v1/potenciales", tags=["potenciales"])


@router.post("", response_model=PotencialResponse)
async def create_potencial(
    potencial: PotencialCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new potencial"""
    try:
        db_potencial = Potencial(**potencial.dict())
        db.add(db_potencial)
        await db.commit()
        await db.refresh(db_potencial)
        return db_potencial
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[PotencialResponse])
async def list_potenciales(
    estado: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all potenciales, optionally filtered by estado"""
    if estado:
        stmt = select(Potencial).where(Potencial.estado == estado)
    else:
        stmt = select(Potencial)

    result = await db.execute(stmt)
    potenciales = result.scalars().all()
    return potenciales


@router.get("/{potencial_id}", response_model=PotencialResponse)
async def get_potencial(
    potencial_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get potencial by ID"""
    stmt = select(Potencial).where(Potencial.id == potencial_id)
    result = await db.execute(stmt)
    potencial = result.scalar_one_or_none()

    if not potencial:
        raise HTTPException(status_code=404, detail="Potencial not found")

    return potencial


@router.put("/{potencial_id}", response_model=PotencialResponse)
async def update_potencial(
    potencial_id: int,
    potencial_update: PotencialUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update potencial"""
    stmt = select(Potencial).where(Potencial.id == potencial_id)
    result = await db.execute(stmt)
    db_potencial = result.scalar_one_or_none()

    if not db_potencial:
        raise HTTPException(status_code=404, detail="Potencial not found")

    update_data = potencial_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_potencial, key, value)

    db_potencial.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(db_potencial)
    return db_potencial


@router.post("/{potencial_id}/convert")
async def convert_to_produccion(
    potencial_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Convert POTENCIAL to PRODUCCION (QUOTE_ACCEPTED)"""
    # Get potencial
    stmt = select(Potencial).where(Potencial.id == potencial_id)
    result = await db.execute(stmt)
    potencial = result.scalar_one_or_none()

    if not potencial:
        raise HTTPException(status_code=404, detail="Potencial not found")

    # Update estado to QUOTE_ACCEPTED
    potencial.estado = "QUOTE_ACCEPTED"
    potencial.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(potencial)

    return {
        "status": "ok",
        "message": "Potencial converted to QUOTE_ACCEPTED. Produccion order will be created on next sync.",
        "potencial_id": potencial_id
    }
