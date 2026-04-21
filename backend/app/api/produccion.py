from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.models.produccion import Produccion
from app.schemas.produccion import ProduccionCreate, ProduccionUpdate, ProduccionResponse
from app.database import get_db
from typing import List, Optional

router = APIRouter(prefix="/api/v1/produccion", tags=["produccion"])


@router.post("", response_model=ProduccionResponse)
async def create_produccion(
    produccion: ProduccionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new produccion order"""
    try:
        db_produccion = Produccion(**produccion.dict())
        db.add(db_produccion)
        await db.commit()
        await db.refresh(db_produccion)
        return db_produccion
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[ProduccionResponse])
async def list_produccion(
    estado: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all produccion orders, optionally filtered by estado"""
    if estado:
        stmt = select(Produccion).where(Produccion.estado == estado)
    else:
        stmt = select(Produccion)

    result = await db.execute(stmt)
    ordenes = result.scalars().all()
    return ordenes


@router.get("/{orden_id}", response_model=ProduccionResponse)
async def get_orden(
    orden_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get produccion order by orden_id"""
    stmt = select(Produccion).where(Produccion.orden_id == orden_id)
    result = await db.execute(stmt)
    orden = result.scalar_one_or_none()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden not found")

    return orden


@router.put("/{orden_id}", response_model=ProduccionResponse)
async def update_orden(
    orden_id: str,
    produccion_update: ProduccionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update produccion order"""
    stmt = select(Produccion).where(Produccion.orden_id == orden_id)
    result = await db.execute(stmt)
    db_produccion = result.scalar_one_or_none()

    if not db_produccion:
        raise HTTPException(status_code=404, detail="Orden not found")

    update_data = produccion_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_produccion, key, value)

    db_produccion.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(db_produccion)
    return db_produccion
