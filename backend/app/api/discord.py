from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/discord", tags=["discord"])


class NotifyRequest(BaseModel):
    tipo: str                    # "content" | "lead" | "opportunity" | "error" | "digest"
    titulo: str
    descripcion: Optional[str] = ""
    brand: Optional[str] = ""
    valor: Optional[str] = ""


@router.post("/notify")
async def discord_notify(payload: NotifyRequest):
    """Endpoint para que los agentes/backend envíen notificaciones a Discord."""
    try:
        from app.services.discord_bot import (
            notify_new_content,
            notify_new_lead,
            notify_opportunity,
            notify_error,
            notify_daily_digest,
            bot,
        )

        if not bot.is_ready():
            return {"status": "skipped", "reason": "Discord bot no conectado"}

        if payload.tipo == "content":
            await notify_new_content(payload.brand, payload.titulo, payload.descripcion)
        elif payload.tipo == "lead":
            await notify_new_lead(payload.titulo, payload.descripcion, payload.valor)
        elif payload.tipo == "opportunity":
            await notify_opportunity(payload.titulo, payload.descripcion, payload.valor)
        elif payload.tipo == "error":
            await notify_error(payload.titulo, payload.descripcion)
        elif payload.tipo == "digest":
            await notify_daily_digest(payload.descripcion)
        else:
            raise HTTPException(status_code=400, detail=f"Tipo desconocido: {payload.tipo}")

        return {"status": "ok", "tipo": payload.tipo, "titulo": payload.titulo}

    except ImportError:
        raise HTTPException(status_code=503, detail="Discord bot no disponible")
    except Exception as e:
        logger.error(f"Error enviando notificación Discord: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def discord_status():
    """Ver si el bot de Discord está conectado."""
    try:
        from app.services.discord_bot import bot
        return {
            "connected": bot.is_ready(),
            "user":      str(bot.user) if bot.user else None,
            "guilds":    len(bot.guilds) if bot.is_ready() else 0,
        }
    except Exception as e:
        return {"connected": False, "error": str(e)}
