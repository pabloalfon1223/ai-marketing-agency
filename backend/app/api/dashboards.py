"""
Endpoints para dashboards y estadísticas
Proporciona datos para visualización en React
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone, timedelta
from app.models.potencial import Potencial
from app.models.produccion import Produccion
from app.database import get_db
from typing import Dict

router = APIRouter(prefix="/api/v1/dashboards", tags=["dashboards"])

# Estados válidos
ESTADOS_POTENCIAL = ["SIN_RESPUESTA", "ESPERAMOS_RESPUESTA", "COTIZACION_ENVIADA", "CLIENTE", "CERRAR", "RECONTACTAR"]
ESTADOS_PRODUCCION = ["PLANIFICACIÓN", "CARPINTERIA", "LAQUEADO", "RETIRO PARA REMODELAR", "PENDIENTE", "POST VENTA", "FIDELIZACION", "FINALIZADO"]


@router.get("/potenciales/resumen", summary="Resumen de POTENCIALES")
async def resumen_potenciales(db: AsyncSession = Depends(get_db)):
    """Obtener resumen de potenciales con conteos por estado"""
    resumen = {"total": 0}

    # Contar total
    stmt_total = select(func.count(Potencial.id))
    result_total = await db.execute(stmt_total)
    resumen["total"] = result_total.scalar() or 0

    # Contar por estado
    for estado in ESTADOS_POTENCIAL:
        stmt = select(func.count(Potencial.id)).where(Potencial.estado == estado)
        result = await db.execute(stmt)
        count = result.scalar() or 0
        resumen[estado] = count

    return resumen


@router.get("/potenciales/funnel", summary="Funnel de conversión")
async def funnel_potenciales(db: AsyncSession = Depends(get_db)):
    """
    Obtener datos de funnel de conversión:
    SIN_RESPUESTA → ESPERAMOS_RESPUESTA → COTIZACION_ENVIADA → CLIENTE
    """
    funnel_estados = ["SIN_RESPUESTA", "ESPERAMOS_RESPUESTA", "COTIZACION_ENVIADA", "CLIENTE"]
    funnel = {}

    for estado in funnel_estados:
        stmt = select(func.count(Potencial.id)).where(Potencial.estado == estado)
        result = await db.execute(stmt)
        count = result.scalar() or 0
        funnel[estado] = count

    return funnel


@router.get("/potenciales/conversion-rate", summary="Tasa de conversión")
async def tasa_conversion(db: AsyncSession = Depends(get_db)):
    """
    Obtener tasa de conversión: (CLIENTE / Total) * 100
    Indica qué porcentaje de potenciales se convirtieron en clientes
    """
    # Total potenciales
    stmt_total = select(func.count(Potencial.id))
    result_total = await db.execute(stmt_total)
    total = result_total.scalar() or 0

    # Clientes (estado CLIENTE)
    stmt_cliente = select(func.count(Potencial.id)).where(Potencial.estado == "CLIENTE")
    result_cliente = await db.execute(stmt_cliente)
    clientes = result_cliente.scalar() or 0

    conversion_pct = (clientes / total * 100) if total > 0 else 0

    return {
        "total_potenciales": total,
        "clientes_convertidos": clientes,
        "tasa_conversion_porcentaje": round(conversion_pct, 2)
    }


@router.get("/potenciales/por-prioridad", summary="Distribución por prioridad")
async def por_prioridad(db: AsyncSession = Depends(get_db)):
    """Obtener distribución de potenciales por prioridad"""
    prioridades = ["ALTA", "MEDIA", "BAJA"]
    distribucion = {}

    for prioridad in prioridades:
        stmt = select(func.count(Potencial.id)).where(Potencial.prioridad == prioridad)
        result = await db.execute(stmt)
        count = result.scalar() or 0
        distribucion[prioridad] = count

    return distribucion


@router.get("/produccion/resumen", summary="Resumen de PRODUCCION")
async def resumen_produccion(db: AsyncSession = Depends(get_db)):
    """Obtener resumen de producción con conteos por estado"""
    resumen = {"total": 0}

    # Contar total
    stmt_total = select(func.count(Produccion.id))
    result_total = await db.execute(stmt_total)
    resumen["total"] = result_total.scalar() or 0

    # Contar por estado
    for estado in ESTADOS_PRODUCCION:
        stmt = select(func.count(Produccion.id)).where(Produccion.estado == estado)
        result = await db.execute(stmt)
        count = result.scalar() or 0
        resumen[estado] = count

    # Contar finalizados
    stmt_finalizados = select(func.count(Produccion.id)).where(Produccion.estado == "FINALIZADO")
    result_finalizados = await db.execute(stmt_finalizados)
    resumen["finalizados"] = result_finalizados.scalar() or 0

    # Contar alertas (>5 días sin actualizar)
    fecha_limite = datetime.now(timezone.utc) - timedelta(days=5)
    stmt_alertas = select(func.count(Produccion.id)).where(Produccion.updated_at < fecha_limite)
    result_alertas = await db.execute(stmt_alertas)
    resumen["alertas_sin_actualizar"] = result_alertas.scalar() or 0

    return resumen


@router.get("/produccion/alertas", summary="Alertas de actualización")
async def alertas_produccion(dias: int = 5, db: AsyncSession = Depends(get_db)):
    """
    Obtener registros de producción que no se actualizaron en X días
    Por defecto retorna los sin actualizar >5 días
    """
    fecha_limite = datetime.now(timezone.utc) - timedelta(days=dias)

    stmt = select(Produccion).where(Produccion.updated_at < fecha_limite)
    result = await db.execute(stmt)
    alertas = result.scalars().all()

    return {
        "total_alertas": len(alertas),
        "dias_umbral": dias,
        "registros": [
            {
                "id": a.id,
                "cliente": a.cliente,
                "estado": a.estado,
                "updated_at": a.updated_at,
                "dias_sin_actualizar": (datetime.now(timezone.utc) - a.updated_at).days
            }
            for a in alertas
        ]
    }


@router.get("/resumen-general", summary="Resumen general del sistema")
async def resumen_general(db: AsyncSession = Depends(get_db)):
    """Obtener resumen general con KPIs principales"""

    # POTENCIALES
    stmt_total_pot = select(func.count(Potencial.id))
    result_total_pot = await db.execute(stmt_total_pot)
    total_potenciales = result_total_pot.scalar() or 0

    stmt_cliente = select(func.count(Potencial.id)).where(Potencial.estado == "CLIENTE")
    result_cliente = await db.execute(stmt_cliente)
    clientes = result_cliente.scalar() or 0

    # PRODUCCION
    stmt_total_prod = select(func.count(Produccion.id))
    result_total_prod = await db.execute(stmt_total_prod)
    total_produccion = result_total_prod.scalar() or 0

    stmt_finalizado = select(func.count(Produccion.id)).where(Produccion.estado == "FINALIZADO")
    result_finalizado = await db.execute(stmt_finalizado)
    finalizados = result_finalizado.scalar() or 0

    # Alertas
    fecha_limite = datetime.now(timezone.utc) - timedelta(days=5)
    stmt_alertas = select(func.count(Produccion.id)).where(Produccion.updated_at < fecha_limite)
    result_alertas = await db.execute(stmt_alertas)
    alertas = result_alertas.scalar() or 0

    # Tasa conversión
    conversion_pct = (clientes / total_potenciales * 100) if total_potenciales > 0 else 0

    return {
        "potenciales": {
            "total": total_potenciales,
            "clientes": clientes,
            "tasa_conversion": round(conversion_pct, 2)
        },
        "produccion": {
            "total": total_produccion,
            "finalizados": finalizados,
            "alertas_sin_actualizar": alertas
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
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
