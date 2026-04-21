"""
Endpoints para gestión de PRODUCCION
Sincronizado con Google Sheets hoja "PRODUCCION"

Los 8 estados válidos son:
- PLANIFICACIÓN
- CARPINTERIA
- LAQUEADO
- RETIRO PARA REMODELAR
- PENDIENTE
- POST VENTA
- FIDELIZACION
- FINALIZADO
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime, timezone, timedelta
from app.models.produccion import Produccion
from app.schemas.produccion import (
    ProduccionCreate,
    ProduccionUpdate,
    ProduccionResponse,
    ProduccionListResponse,
)
from app.database import get_db
from typing import Optional

router = APIRouter(prefix="/api/v1/produccion", tags=["produccion"])


@router.post("", response_model=ProduccionResponse, summary="Crear nueva orden de producción")
async def crear_produccion(
    produccion: ProduccionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crear un nuevo registro de producción"""
    try:
        db_produccion = Produccion(**produccion.dict())
        db.add(db_produccion)
        await db.commit()
        await db.refresh(db_produccion)
        return db_produccion
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear producción: {str(e)}")


@router.get("", response_model=ProduccionListResponse, summary="Listar órdenes de producción")
async def listar_produccion(
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    """Listar todos los registros de producción con filtros opcionales"""
    query = select(Produccion)

    if estado:
        query = query.where(Produccion.estado == estado)

    # Obtener total
    count_result = await db.execute(select(Produccion))
    total = len(count_result.scalars().all())

    # Obtener datos paginados, ordenados por actualización más reciente
    query = query.order_by(desc(Produccion.updated_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    ordenes = result.scalars().all()

    return ProduccionListResponse(total=total, items=ordenes)


@router.get("/{produccion_id}", response_model=ProduccionResponse, summary="Obtener orden de producción por ID")
async def obtener_produccion(
    produccion_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener un registro de producción específico"""
    stmt = select(Produccion).where(Produccion.id == produccion_id)
    result = await db.execute(stmt)
    produccion = result.scalar_one_or_none()

    if not produccion:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

    return produccion


@router.put("/{produccion_id}", response_model=ProduccionResponse, summary="Actualizar orden de producción")
async def actualizar_produccion(
    produccion_id: int,
    produccion_update: ProduccionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Actualizar un registro de producción"""
    stmt = select(Produccion).where(Produccion.id == produccion_id)
    result = await db.execute(stmt)
    db_produccion = result.scalar_one_or_none()

    if not db_produccion:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

    update_data = produccion_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_produccion, key, value)

    db_produccion.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(db_produccion)
    return db_produccion


@router.delete("/{produccion_id}", summary="Eliminar orden de producción")
async def eliminar_produccion(
    produccion_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Eliminar un registro de producción"""
    stmt = select(Produccion).where(Produccion.id == produccion_id)
    result = await db.execute(stmt)
    produccion = result.scalar_one_or_none()

    if not produccion:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")

    await db.delete(produccion)
    await db.commit()

    return {"status": "ok", "message": f"Orden de producción {produccion_id} eliminada"}


@router.get("/alertas/sin-actualizar", summary="Obtener alertas de registros sin actualizar")
async def obtener_alertas_sin_actualizar(
    dias: int = Query(5, description="Días sin actualización para generar alerta"),
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener registros de producción que no han sido actualizados en X días
    Por defecto retorna los que no se actualizaron en más de 5 días
    """
    fecha_limite = datetime.now(timezone.utc) - timedelta(days=dias)

    stmt = select(Produccion).where(Produccion.updated_at < fecha_limite)
    result = await db.execute(stmt)
    ordenes_alerta = result.scalars().all()

    return {
        "total_alertas": len(ordenes_alerta),
        "dias_sin_actualizar": dias,
        "ordenes": ordenes_alerta
    }
