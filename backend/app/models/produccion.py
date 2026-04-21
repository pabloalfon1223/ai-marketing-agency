from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database import Base


class Produccion(Base):
    """
    Modelo para PRODUCCION (órdenes en producción)
    Sincronizado con Google Sheets hoja "PRODUCCION"

    Estados permitidos (mantener todos los 8):
    - PLANIFICACIÓN: En fase inicial de planificación
    - CARPINTERIA: En proceso de carpintería
    - LAQUEADO: En proceso de laqueado
    - RETIRO PARA REMODELAR: Enviado a remodelar
    - PENDIENTE: Pendiente de acción
    - POST VENTA: En fase post-venta
    - FIDELIZACION: En proceso de fidelización
    - FINALIZADO: Completado y finalizado
    """
    __tablename__ = "produccion"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Información del cliente
    cliente = Column(String(200), nullable=False)  # Nombre del cliente
    celular = Column(String(20))  # Teléfono del cliente

    # Descripción breve del trabajo
    descripcion_breve = Column(String(500))  # Qué se está haciendo (ej: el mueble)

    # Estado de producción (uno de los 8 estados válidos)
    estado = Column(String(50), nullable=False, default="PLANIFICACIÓN")

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
