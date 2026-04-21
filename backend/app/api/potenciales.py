"""
Endpoints para gestión de POTENCIALES
Sincronizado con Google Sheets hoja "POTENCIALES"
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime, timezone
from app.models.potencial import Potencial
from app.schemas.potencial import (
    PotencialCreate,
    PotencialUpdate,
    PotencialResponse,
    PotencialListResponse,
)
from app.database import get_db
from typing import Optional

router = APIRouter(prefix="/api/v1/potenciales", tags=["potenciales"])


@router.post("", response_model=PotencialResponse, summary="Crear nuevo potencial")
async def crear_potencial(
    potencial: PotencialCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo potencial"""
    try:
        db_potencial = Potencial(**potencial.dict())
        db.add(db_potencial)
        await db.commit()
        await db.refresh(db_potencial)
        return db_potencial
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear potencial: {str(e)}")


@router.get("", response_model=PotencialListResponse, summary="Listar potenciales")
async def listar_potenciales(
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    prioridad: Optional[str] = Query(None, description="Filtrar por prioridad"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    """Listar todos los potenciales con filtros opcionales"""
    query = select(Potencial)

    if estado:
        query = query.where(Potencial.estado == estado)
    if prioridad:
        query = query.where(Potencial.prioridad == prioridad)

    # Obtener total
    count_result = await db.execute(select(Potencial))
    total = len(count_result.scalars().all())

    # Obtener datos paginados
    query = query.order_by(desc(Potencial.updated_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    potenciales = result.scalars().all()

    return PotencialListResponse(total=total, items=potenciales)


@router.get("/{potencial_id}", response_model=PotencialResponse, summary="Obtener potencial por ID")
async def obtener_potencial(
    potencial_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener un potencial específico por su ID"""
    stmt = select(Potencial).where(Potencial.id == potencial_id)
    result = await db.execute(stmt)
    potencial = result.scalar_one_or_none()

    if not potencial:
        raise HTTPException(status_code=404, detail="Potencial no encontrado")

    return potencial


@router.put("/{potencial_id}", response_model=PotencialResponse, summary="Actualizar potencial")
async def actualizar_potencial(
    potencial_id: int,
    potencial_update: PotencialUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un potencial existente"""
    stmt = select(Potencial).where(Potencial.id == potencial_id)
    result = await db.execute(stmt)
    db_potencial = result.scalar_one_or_none()

    if not db_potencial:
        raise HTTPException(status_code=404, detail="Potencial no encontrado")

    update_data = potencial_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_potencial, key, value)

    db_potencial.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(db_potencial)
    return db_potencial


@router.delete("/{potencial_id}", summary="Eliminar potencial")
async def eliminar_potencial(
    potencial_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un potencial"""
    stmt = select(Potencial).where(Potencial.id == potencial_id)
    result = await db.execute(stmt)
    potencial = result.scalar_one_or_none()

    if not potencial:
        raise HTTPException(status_code=404, detail="Potencial no encontrado")

    await db.delete(potencial)
    await db.commit()

    return {"status": "ok", "message": f"Potencial {potencial_id} eliminado"}
