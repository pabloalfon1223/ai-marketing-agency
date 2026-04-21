from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.potencial import Potencial
from app.models.produccion import Produccion
from app.database import get_db
from typing import Dict, List, Optional

router = APIRouter(prefix="/api/v1/dashboards", tags=["dashboards"])


@router.get("/potenciales/funnel")
async def funnel_potenciales(db: AsyncSession = Depends(get_db)):
    """Get potenciales funnel data (count by estado)"""
    estados = ["SIN_RESPUESTA", "ESPERAMOS_RESPUESTA", "COTIZACION_ENVIADA", "QUOTE_ACCEPTED"]
    funnel = {}

    for estado in estados:
        stmt = select(func.count(Potencial.id)).where(Potencial.estado == estado)
        result = await db.execute(stmt)
        count = result.scalar() or 0
        funnel[estado] = count

    return funnel


@router.get("/potenciales/value-by-status")
async def value_by_status(db: AsyncSession = Depends(get_db)):
    """Get total estimated value grouped by estado"""
    estados = ["SIN_RESPUESTA", "ESPERAMOS_RESPUESTA", "COTIZACION_ENVIADA", "QUOTE_ACCEPTED"]
    value_data = {}

    for estado in estados:
        stmt = select(func.sum(Potencial.valor_estimado)).where(Potencial.estado == estado)
        result = await db.execute(stmt)
        total = result.scalar() or 0
        value_data[estado] = total

    return value_data


@router.get("/potenciales/conversion-rate")
async def conversion_rate(db: AsyncSession = Depends(get_db)):
    """Get conversion rate: QUOTE_ACCEPTED / Total"""
    # Total potenciales
    stmt_total = select(func.count(Potencial.id))
    result_total = await db.execute(stmt_total)
    total = result_total.scalar() or 0

    # QUOTE_ACCEPTED count
    stmt_accepted = select(func.count(Potencial.id)).where(Potencial.estado == "QUOTE_ACCEPTED")
    result_accepted = await db.execute(stmt_accepted)
    accepted = result_accepted.scalar() or 0

    conversion_pct = (accepted / total * 100) if total > 0 else 0

    return {
        "total": total,
        "quote_accepted": accepted,
        "conversion_rate": round(conversion_pct, 2)
    }


@router.get("/produccion/timeline")
async def timeline_produccion(db: AsyncSession = Depends(get_db)):
    """Get produccion orders with timeline data for Gantt chart"""
    stmt = select(Produccion).order_by(Produccion.fecha_inicio)
    result = await db.execute(stmt)
    ordenes = result.scalars().all()

    timeline_data = []
    for orden in ordenes:
        timeline_data.append({
            "orden_id": orden.orden_id,
            "cliente": orden.cliente,
            "mueble": orden.mueble,
            "estado": orden.estado,
            "fecha_inicio": orden.fecha_inicio,
            "fecha_entrega_est": orden.fecha_entrega_est,
            "dias_produccion": (orden.fecha_entrega_est - orden.fecha_inicio).days if orden.fecha_entrega_est else None
        })

    return timeline_data


@router.get("/produccion/ingresos")
async def ingresos_totales(db: AsyncSession = Depends(get_db)):
    """Get total revenue (COMPLETED and DELIVERED orders)"""
    stmt = select(func.sum(Produccion.precio_final)).where(
        Produccion.estado.in_(["COMPLETED", "DELIVERED"])
    )
    result = await db.execute(stmt)
    total_ingresos = result.scalar() or 0

    return {
        "total_ingresos": total_ingresos,
        "currency": "ARS"
    }


@router.get("/summary")
async def dashboard_summary(db: AsyncSession = Depends(get_db)):
    """Get overall dashboard summary"""
    # Count potenciales
    stmt_total_pot = select(func.count(Potencial.id))
    result_total_pot = await db.execute(stmt_total_pot)
    total_potenciales = result_total_pot.scalar() or 0

    # Count produccion
    stmt_total_prod = select(func.count(Produccion.id))
    result_total_prod = await db.execute(stmt_total_prod)
    total_produccion = result_total_prod.scalar() or 0

    # Conversion rate
    stmt_accepted = select(func.count(Potencial.id)).where(Potencial.estado == "QUOTE_ACCEPTED")
    result_accepted = await db.execute(stmt_accepted)
    accepted = result_accepted.scalar() or 0

    conversion_pct = (accepted / total_potenciales * 100) if total_potenciales > 0 else 0

    # Total value
    stmt_value = select(func.sum(Potencial.valor_estimado))
    result_value = await db.execute(stmt_value)
    total_value = result_value.scalar() or 0

    # Total ingresos
    stmt_ingresos = select(func.sum(Produccion.precio_final)).where(
        Produccion.estado.in_(["COMPLETED", "DELIVERED"])
    )
    result_ingresos = await db.execute(stmt_ingresos)
    total_ingresos = result_ingresos.scalar() or 0

    return {
        "total_potenciales": total_potenciales,
        "total_produccion": total_produccion,
        "conversion_rate": round(conversion_pct, 2),
        "total_estimated_value": total_value,
        "total_ingresos": total_ingresos,
        "currency": "ARS"
    }
