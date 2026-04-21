from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database import Base


class Potencial(Base):
    """
    Modelo para POTENCIALES (oportunidades de venta)
    Sincronizado con Google Sheets hoja "POTENCIALES"
    """
    __tablename__ = "potenciales"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Información del cliente
    nombre = Column(String(200), nullable=False)  # Nombre del cliente
    mueble = Column(String(100), nullable=False)  # Tipo de mueble (Biblioteca, Cama, Placar, etc)
    celular = Column(String(20))  # Número de teléfono del cliente

    # Seguimiento de contacto
    fecha = Column(DateTime, nullable=False)  # Última fecha de contacto/actualización
    estado = Column(String(50), nullable=False, default="SIN_RESPUESTA")
    # Estados: SIN_RESPUESTA, ESPERAMOS_RESPUESTA, COTIZACION_ENVIADA, CLIENTE, CERRAR, RECONTACTAR

    quien_lo_tiene = Column(String(100))  # Vendedor/persona asignada (ej: PABLO)
    prioridad = Column(String(20), default="MEDIA")  # ALTA, MEDIA, BAJA

    # Seguimiento
    fecha_seguimiento = Column(DateTime)  # Fecha de próximo seguimiento requerido

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
