"""
Telegram Bot Service for Polt Mobilier

Provides access to potenciales and produccion data via Telegram
"""

import logging
import aiohttp
from typing import Optional, List, Dict, Any
from app.config import get_settings

logger = logging.getLogger(__name__)


class TelegramBotService:
    """Service for sending messages and managing Telegram bot"""

    def __init__(self):
        self.settings = get_settings()
        self.base_url = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}"
        self.chat_id = self.settings.telegram_chat_id

    async def send_message(
        self,
        text: str,
        chat_id: Optional[str] = None,
        parse_mode: str = "HTML",
    ) -> bool:
        """
        Send a message to Telegram

        Args:
            text: Message text (supports HTML formatting)
            chat_id: Optional chat ID (defaults to configured)
            parse_mode: 'HTML' or 'Markdown'

        Returns:
            True if sent successfully
        """
        if not self.settings.telegram_enabled or not self.settings.telegram_bot_token:
            logger.warning("Telegram bot not enabled")
            return False

        target_chat = chat_id or self.chat_id

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "chat_id": target_chat,
                    "text": text,
                    "parse_mode": parse_mode,
                }

                async with session.post(
                    f"{self.base_url}/sendMessage", json=payload
                ) as response:
                    if response.status == 200:
                        logger.info(f"Telegram message sent to {target_chat}")
                        return True
                    else:
                        logger.error(
                            f"Failed to send Telegram message: {response.status}"
                        )
                        return False

        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
            return False

    def format_potencial(self, potencial: Dict[str, Any]) -> str:
        """Format potencial data for Telegram message"""
        texto = f"""
<b>📋 POTENCIAL</b>
<b>Nombre:</b> {potencial.get('nombre', 'N/A')}
<b>Mueble:</b> {potencial.get('mueble', 'N/A')}
<b>Estado:</b> {potencial.get('estado', 'N/A')}
<b>Valor Est.:</b> ARS {potencial.get('valor_estimado', 0):,.0f}
<b>Vendedor:</b> {potencial.get('quien_lo_tiene', 'N/A')}
<b>Teléfono:</b> {potencial.get('telefono', 'N/A')}
<b>Contacto:</b> {potencial.get('fecha_contacto', 'N/A')}
"""
        return texto.strip()

    def format_produccion(self, orden: Dict[str, Any]) -> str:
        """Format produccion order data for Telegram message"""
        dias = ""
        if orden.get("fecha_inicio") and orden.get("fecha_entrega_est"):
            from datetime import datetime

            inicio = datetime.fromisoformat(orden["fecha_inicio"])
            fin = datetime.fromisoformat(orden["fecha_entrega_est"])
            dias_num = (fin - inicio).days
            dias = f"\n<b>Días de Producción:</b> {dias_num}d"

        texto = f"""
<b>📦 ORDEN DE PRODUCCIÓN</b>
<b>Orden ID:</b> <code>{orden.get('orden_id', 'N/A')}</code>
<b>Cliente:</b> {orden.get('cliente', 'N/A')}
<b>Mueble:</b> {orden.get('mueble', 'N/A')}
<b>Estado:</b> {orden.get('estado', 'N/A')}
<b>Inicio:</b> {orden.get('fecha_inicio', 'N/A')}
<b>Entrega Est.:</b> {orden.get('fecha_entrega_est', 'N/A')}{dias}
<b>Precio Final:</b> ARS {orden.get('precio_final', 0):,.0f}
<b>Productor:</b> {orden.get('productor', 'N/A')}
"""
        return texto.strip()

    def format_stats(self, summary: Dict[str, Any]) -> str:
        """Format dashboard stats for Telegram message"""
        texto = f"""
<b>📊 ESTADÍSTICAS CONSOLIDADAS</b>

<b>POTENCIALES:</b>
  Total: {summary.get('total_potenciales', 0)}
  Conversion Rate: <b>{summary.get('conversion_rate', 0):.1f}%</b>
  Valor Estimado: ARS {summary.get('total_estimated_value', 0):,.0f}

<b>PRODUCCIÓN:</b>
  Total Órdenes: {summary.get('total_produccion', 0)}
  Ingresos: ARS {summary.get('total_ingresos', 0):,.0f}
  Moneda: {summary.get('currency', 'ARS')}

<b>CLAVE:</b>
  ROI Estimado: {((summary.get('total_ingresos', 0) - summary.get('total_estimated_value', 0)) / max(summary.get('total_estimated_value', 1), 1) * 100):.1f}%
"""
        return texto.strip()

    async def notify_conversion(self, potencial_nombre: str, orden_id: str) -> bool:
        """Notify about potencial conversion to produccion"""
        texto = f"""
✅ <b>CONVERSIÓN EXITOSA</b>

<b>Potencial:</b> {potencial_nombre}
<b>Orden ID:</b> <code>{orden_id}</code>

La orden ha sido creada automáticamente en producción.
"""
        return await self.send_message(texto)

    async def notify_status_change(
        self, tipo: str, id: str, nuevo_estado: str
    ) -> bool:
        """Notify about status change"""
        emoji = "📋" if tipo == "potencial" else "📦"
        texto = f"""
{emoji} <b>CAMBIO DE ESTADO</b>

<b>Tipo:</b> {tipo.upper()}
<b>ID:</b> <code>{id}</code>
<b>Nuevo Estado:</b> <b>{nuevo_estado}</b>
"""
        return await self.send_message(texto)
