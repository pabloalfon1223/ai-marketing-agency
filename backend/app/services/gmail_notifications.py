"""
Servicio para enviar notificaciones por Gmail
Maneja eventos críticos del sistema (conversión de potenciales, alertas, etc)
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.config import get_settings

logger = logging.getLogger(__name__)

class GmailNotificationService:
    """Servicio para enviar notificaciones por correo electrónico"""

    def __init__(self):
        self.settings = get_settings()
        self.sender_email = self.settings.gmail_sender_email
        self.app_password = self.settings.gmail_app_password
        self.recipient_email = self.settings.gmail_recipient_email
        self.enabled = self.settings.gmail_enabled
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    async def enviar_notificacion(self, asunto: str, cuerpo_html: str, cuerpo_texto: str = None) -> bool:
        """
        Envía una notificación por correo electrónico

        Args:
            asunto: Asunto del correo
            cuerpo_html: Cuerpo en formato HTML
            cuerpo_texto: Cuerpo en formato texto (fallback)

        Returns:
            bool: True si se envió correctamente, False si falló
        """

        if not self.enabled or not all([self.sender_email, self.app_password, self.recipient_email]):
            logger.warning("Gmail no está configurado. Notificación no enviada.")
            return False

        try:
            # Crear mensaje MIME
            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = asunto
            mensaje["From"] = self.sender_email
            mensaje["To"] = self.recipient_email

            # Agregar versiones de texto y HTML
            if cuerpo_texto:
                parte_texto = MIMEText(cuerpo_texto, "plain")
                mensaje.attach(parte_texto)

            parte_html = MIMEText(cuerpo_html, "html")
            mensaje.attach(parte_html)

            # Conectar a Gmail y enviar
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.send_message(mensaje)

            logger.info(f"Notificación enviada exitosamente: {asunto}")
            return True

        except Exception as e:
            logger.error(f"Error al enviar notificación: {str(e)}")
            return False

    async def notificar_potencial_convertido(self, nombre: str, mueble: str, celular: str) -> bool:
        """
        Notifica cuando un POTENCIAL se convierte a PRODUCCIÓN (CLIENTE)
        """

        asunto = f"✅ Nuevo Cliente Convertido: {nombre}"

        cuerpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #28a745;">✅ Nuevo Cliente Convertido a Producción</h2>

                    <p><strong>Fecha/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>

                    <div style="background-color: white; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
                        <p><strong>Cliente:</strong> {nombre}</p>
                        <p><strong>Producto/Mueble:</strong> {mueble}</p>
                        <p><strong>Celular:</strong> {celular}</p>
                        <p><strong>Estado Inicial:</strong> PLANIFICACIÓN</p>
                    </div>

                    <p style="color: #666; font-size: 14px;">
                        Este cliente ha sido automáticamente creado en la sección PRODUCCIÓN.
                        Puedes comenzar el seguimiento desde el dashboard.
                    </p>
                </div>
            </body>
        </html>
        """

        cuerpo_texto = f"""
        ✅ NUEVO CLIENTE CONVERTIDO A PRODUCCIÓN

        Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

        Cliente: {nombre}
        Producto/Mueble: {mueble}
        Celular: {celular}
        Estado Inicial: PLANIFICACIÓN

        Este cliente ha sido automáticamente creado en la sección PRODUCCIÓN.
        """

        return await self.enviar_notificacion(asunto, cuerpo_html, cuerpo_texto)

    async def notificar_alerta_actualizacion(self, cliente: str, dias_sin_actualizar: int) -> bool:
        """
        Notifica cuando un registro de PRODUCCIÓN no se actualiza por más de 5 días
        """

        asunto = f"⚠️ Alerta: {cliente} - Sin actualizar hace {dias_sin_actualizar} días"

        cuerpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="background-color: #fff3cd; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #ff9800;">⚠️ Acción Requerida: Actualización Pendiente</h2>

                    <p><strong>Fecha/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>

                    <div style="background-color: white; padding: 15px; border-left: 4px solid #ff9800; margin: 20px 0;">
                        <p><strong>Cliente:</strong> {cliente}</p>
                        <p><strong>Días sin actualizar:</strong> {dias_sin_actualizar} días</p>
                        <p style="color: #d32f2f; font-weight: bold;">Estado: REQUIERE ATENCIÓN</p>
                    </div>

                    <p style="color: #666; font-size: 14px;">
                        Este registro no ha sido actualizado en más de 5 días.
                        Por favor, revisa el estado y actualiza la información cuando sea posible.
                    </p>
                </div>
            </body>
        </html>
        """

        cuerpo_texto = f"""
        ⚠️ ALERTA: ACTUALIZACIÓN PENDIENTE

        Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

        Cliente: {cliente}
        Días sin actualizar: {dias_sin_actualizar} días

        Este registro requiere atención - por favor actualiza cuando sea posible.
        """

        return await self.enviar_notificacion(asunto, cuerpo_html, cuerpo_texto)

    async def notificar_estado_cambio(self, cliente: str, estado_anterior: str, estado_nuevo: str) -> bool:
        """
        Notifica cuando cambia el estado de un registro en PRODUCCIÓN
        """

        asunto = f"📋 Cambio de Estado: {cliente} - {estado_anterior} → {estado_nuevo}"

        cuerpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="background-color: #e3f2fd; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #1976d2;">📋 Cambio de Estado Registrado</h2>

                    <p><strong>Fecha/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>

                    <div style="background-color: white; padding: 15px; border-left: 4px solid #1976d2; margin: 20px 0;">
                        <p><strong>Cliente:</strong> {cliente}</p>
                        <p><strong>Estado Anterior:</strong> {estado_anterior}</p>
                        <p><strong>Estado Nuevo:</strong> {estado_nuevo}</p>
                    </div>

                    <p style="color: #666; font-size: 14px;">
                        El estado de este cliente ha sido actualizado exitosamente.
                    </p>
                </div>
            </body>
        </html>
        """

        cuerpo_texto = f"""
        📋 CAMBIO DE ESTADO REGISTRADO

        Fecha/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

        Cliente: {cliente}
        Estado Anterior: {estado_anterior}
        Estado Nuevo: {estado_nuevo}
        """

        return await self.enviar_notificacion(asunto, cuerpo_html, cuerpo_texto)


# Instancia global del servicio
notification_service = GmailNotificationService()
