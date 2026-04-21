"""
Telegram Bot API Router

Handles Telegram bot commands and webhook updates
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.potencial import Potencial
from app.models.produccion import Produccion
from app.services.telegram_bot import TelegramBotService
from app.config import get_settings
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/telegram", tags=["telegram"])

telegram_service = TelegramBotService()


@router.post("/webhook")
async def telegram_webhook(update: Dict[str, Any]):
    """Handle Telegram webhook updates"""
    try:
        message = update.get("message")
        if not message:
            return {"ok": True}

        chat_id = str(message.get("chat", {}).get("id"))
        text = message.get("text", "").strip()
        user_name = message.get("from", {}).get("first_name", "Usuario")

        logger.info(f"Telegram message from {user_name}: {text}")

        # Parse commands
        if text.startswith("/"):
            await handle_command(text, chat_id, user_name)
        else:
            # Natural language query
            await handle_query(text, chat_id)

        return {"ok": True}

    except Exception as e:
        logger.error(f"Error in telegram webhook: {str(e)}")
        return {"ok": False, "error": str(e)}


async def handle_command(command: str, chat_id: str, user_name: str):
    """Handle Telegram bot commands"""
    cmd = command.lower().split()[0]

    if cmd == "/start":
        text = f"""
👋 ¡Hola {user_name}!

Soy el bot de <b>Polt Mobilier</b>. Puedo ayudarte con:

<b>Comandos disponibles:</b>
/potenciales - Ver lista de potenciales
/produccion - Ver órdenes en producción
/stats - Ver estadísticas consolidadas
/ayuda - Mostrar esta ayuda

<b>O simplemente pregunta:</b>
"¿Cuántos potenciales hay?"
"Mostrar potenciales en cotización"
"Órdenes entregadas"

¿En qué puedo ayudarte?
"""
        await telegram_service.send_message(text, chat_id)

    elif cmd == "/potenciales":
        async with get_db() as db:
            stmt = select(Potencial).order_by(Potencial.updated_at.desc()).limit(10)
            result = await db.execute(stmt)
            potenciales = result.scalars().all()

            if not potenciales:
                text = "❌ No hay potenciales registrados"
            else:
                text = "<b>📋 ÚLTIMOS 10 POTENCIALES:</b>\n\n"
                for p in potenciales:
                    text += f"• <b>{p.nombre}</b> - {p.estado} (ARS {p.valor_estimado:,.0f})\n"

            await telegram_service.send_message(text, chat_id)

    elif cmd == "/produccion":
        async with get_db() as db:
            stmt = select(Produccion).order_by(Produccion.updated_at.desc()).limit(10)
            result = await db.execute(stmt)
            ordenes = result.scalars().all()

            if not ordenes:
                text = "❌ No hay órdenes registradas"
            else:
                text = "<b>📦 ÚLTIMAS 10 ÓRDENES:</b>\n\n"
                for o in ordenes:
                    text += f"• <code>{o.orden_id}</code> - {o.cliente} ({o.estado})\n"

            await telegram_service.send_message(text, chat_id)

    elif cmd == "/stats":
        async with get_db() as db:
            # Calcular estadísticas
            stmt_total = select(func.count(Potencial.id))
            result_total = await db.execute(stmt_total)
            total_pot = result_total.scalar() or 0

            stmt_accepted = select(func.count(Potencial.id)).where(
                Potencial.estado == "QUOTE_ACCEPTED"
            )
            result_accepted = await db.execute(stmt_accepted)
            accepted = result_accepted.scalar() or 0

            stmt_value = select(func.sum(Potencial.valor_estimado))
            result_value = await db.execute(stmt_value)
            total_value = result_value.scalar() or 0

            stmt_prod = select(func.count(Produccion.id))
            result_prod = await db.execute(stmt_prod)
            total_prod = result_prod.scalar() or 0

            stmt_ingresos = select(func.sum(Produccion.precio_final)).where(
                Produccion.estado.in_(["COMPLETED", "DELIVERED"])
            )
            result_ingresos = await db.execute(stmt_ingresos)
            total_ingresos = result_ingresos.scalar() or 0

            conversion_rate = (
                (accepted / total_pot * 100) if total_pot > 0 else 0
            )

            text = f"""
<b>📊 ESTADÍSTICAS EN VIVO</b>

<b>POTENCIALES:</b>
  Total: {total_pot}
  Aceptados: {accepted}
  Conversion Rate: <b>{conversion_rate:.1f}%</b>
  Valor Estimado: ARS {total_value:,.0f}

<b>PRODUCCIÓN:</b>
  Total Órdenes: {total_prod}
  Ingresos: ARS {total_ingresos:,.0f}
"""
            await telegram_service.send_message(text, chat_id)

    elif cmd == "/ayuda":
        text = """
<b>🤖 COMANDOS DISPONIBLES</b>

/start - Mensaje de bienvenida
/potenciales - Ver últimos potenciales
/produccion - Ver últimas órdenes
/stats - Ver estadísticas
/ayuda - Mostrar esta ayuda

<b>PREGUNTAS NATURALES:</b>
Puedes hacer preguntas como:
• "¿Cuántos potenciales sin respuesta hay?"
• "Mostrar potenciales en cotización"
• "¿Cuál es el cliente más valioso?"
• "Órdenes entregadas este mes"

Estoy aquí para ayudarte 😊
"""
        await telegram_service.send_message(text, chat_id)

    else:
        text = f"❌ Comando desconocido: <code>{cmd}</code>\n\nUsa /ayuda para ver los comandos disponibles"
        await telegram_service.send_message(text, chat_id)


async def handle_query(query: str, chat_id: str):
    """Handle natural language queries"""
    query_lower = query.lower()

    async with get_db() as db:
        # Detect query type and respond
        if "potencial" in query_lower and "sin respuesta" in query_lower:
            stmt = select(func.count(Potencial.id)).where(
                Potencial.estado == "SIN_RESPUESTA"
            )
            result = await db.execute(stmt)
            count = result.scalar() or 0
            text = f"📋 Hay <b>{count}</b> potenciales sin respuesta"

        elif "potencial" in query_lower and "cotización" in query_lower:
            stmt = select(Potencial).where(
                Potencial.estado == "COTIZACION_ENVIADA"
            ).limit(5)
            result = await db.execute(stmt)
            potenciales = result.scalars().all()

            if potenciales:
                text = "<b>📋 Potenciales en cotización:</b>\n\n"
                for p in potenciales:
                    text += f"• {p.nombre} - ARS {p.valor_estimado:,.0f}\n"
            else:
                text = "No hay potenciales en cotización"

        elif "orden" in query_lower and "entrega" in query_lower:
            stmt = select(Produccion).where(
                Produccion.estado == "DELIVERED"
            ).limit(5)
            result = await db.execute(stmt)
            ordenes = result.scalars().all()

            if ordenes:
                text = "<b>📦 Órdenes entregadas:</b>\n\n"
                for o in ordenes:
                    text += f"• {o.orden_id} - {o.cliente} (ARS {o.precio_final:,.0f})\n"
            else:
                text = "No hay órdenes entregadas"

        elif "ingresos" in query_lower or "revenue" in query_lower:
            stmt = select(func.sum(Produccion.precio_final)).where(
                Produccion.estado.in_(["COMPLETED", "DELIVERED"])
            )
            result = await db.execute(stmt)
            total = result.scalar() or 0
            text = f"💰 Ingresos totales: <b>ARS {total:,.0f}</b>"

        elif "conversión" in query_lower or "conversion" in query_lower:
            stmt_total = select(func.count(Potencial.id))
            result_total = await db.execute(stmt_total)
            total = result_total.scalar() or 0

            stmt_accepted = select(func.count(Potencial.id)).where(
                Potencial.estado == "QUOTE_ACCEPTED"
            )
            result_accepted = await db.execute(stmt_accepted)
            accepted = result_accepted.scalar() or 0

            rate = (accepted / total * 100) if total > 0 else 0
            text = f"📈 Tasa de conversión: <b>{rate:.1f}%</b> ({accepted}/{total})"

        else:
            text = f"🤔 No entendí tu pregunta: '{query}'\n\nTry /ayuda para ver comandos disponibles"

    await telegram_service.send_message(text, chat_id)


@router.get("/send-test")
async def send_test_message(message: str = "Test message from Polt Mobilier"):
    """Send a test message to Telegram (for debugging)"""
    if not get_settings().telegram_enabled:
        raise HTTPException(status_code=400, detail="Telegram not enabled")

    success = await telegram_service.send_message(message)
    return {"success": success, "message": message}
