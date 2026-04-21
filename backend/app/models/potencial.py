from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from datetime import datetime, timezone
from app.database import Base


class Potencial(Base):
    __tablename__ = "potenciales"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Customer info
    nombre = Column(String(200), nullable=False)  # Nombre del cliente
    mueble = Column(String(100), nullable=False)  # Tipo de mueble (Biblioteca, Cama, Placar, etc)

    # Contact tracking
    fecha_contacto = Column(DateTime, nullable=False)  # Cuando se contactó
    estado = Column(String(50), nullable=False, default="SIN_RESPUESTA")
    # Estados: SIN_RESPUESTA, ESPERAMOS_RESPUESTA, COTIZACION_ENVIADA, QUOTE_ACCEPTED

    quien_lo_tiene = Column(String(100))  # Vendedor/persona asignada (ej: PABLO)
    telefono = Column(String(20))  # Teléfono de contacto

    # Follow-up
    nota = Column(Text)  # Notas adicionales
    fecha_seguimiento = Column(DateTime)  # Fecha de próximo seguimiento

    # Valuation
    valor_estimado = Column(Float)  # Estimado de venta en ARS

    # Related production order (when converted)
    orden_id_asignada = Column(String(50))  # FK a Produccion cuando se convierte (ej: ORD-001-2026)

    # Sync tracking
    sincronizado_sheets = Column(Boolean, default=False)  # Indica si fue sincronizado a Sheets

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
