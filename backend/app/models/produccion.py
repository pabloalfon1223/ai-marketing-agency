from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey
from datetime import datetime, timezone
from app.database import Base


class Produccion(Base):
    __tablename__ = "produccion"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Order identification
    orden_id = Column(String(50), nullable=False, unique=True)  # ORD-001-2026, etc

    # Customer & Product info
    cliente = Column(String(200), nullable=False)  # Del POTENCIAL convertido
    mueble = Column(String(100), nullable=False)  # Del POTENCIAL convertido

    # Production status
    estado = Column(String(50), nullable=False, default="ACCEPTED")
    # Estados: ACCEPTED, IN_PRODUCTION, COMPLETED, DELIVERED

    # Timeline
    fecha_inicio = Column(DateTime, nullable=False)  # Cuando empezó producción
    fecha_entrega_est = Column(DateTime)  # Entrega estimada

    # Production assignment
    productor = Column(String(100))  # Quién produce (ej: Producer A)

    # Financials
    costo_real = Column(Float)  # Costo final de producción
    precio_final = Column(Float)  # Precio de venta final

    # Notes
    notas = Column(Text)  # Notas de producción (retrasos, cambios, etc)

    # Related potencial
    potencial_id = Column(Integer)  # FK a Potencial de donde proviene

    # Sync tracking
    sincronizado_sheets = Column(Boolean, default=False)  # Indica si fue sincronizado a Sheets

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
