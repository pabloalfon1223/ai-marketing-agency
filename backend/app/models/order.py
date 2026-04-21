from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from datetime import datetime, timezone
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String(50), nullable=False, unique=True)  # POL-2025-001, etc

    # Customer info
    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(200))
    customer_phone = Column(String(20))
    customer_whatsapp = Column(String(20))

    # Product details
    product_type = Column(String(100), nullable=False)  # biblioteca, cama, placar, etc
    product_description = Column(Text, nullable=False)  # descripcion del mueble
    custom_specs = Column(Text)  # especificaciones a medida

    # Pricing
    estimated_cost = Column(Float)  # costo estimado inicial
    final_cost = Column(Float)  # costo final
    currency = Column(String(10), default="ARS")
    payment_status = Column(String(50), default="pending")  # pending, partial, completed, refunded

    # Production tracking
    order_status = Column(String(50), default="quote_sent")  # quote_sent, quote_accepted, in_production, completed, delivered
    production_start_date = Column(DateTime)
    estimated_delivery_date = Column(DateTime)
    actual_delivery_date = Column(DateTime)
    assigned_producer = Column(String(100))  # quien produce

    # Communication & notifications
    email_notifications_sent = Column(String(500))  # JSON: list of emails sent
    whatsapp_notifications_sent = Column(String(500))  # JSON: list of whatsapp messages
    last_notification_at = Column(DateTime)

    # Documentation
    images_path = Column(Text)  # JSON: rutas de imagenes del progreso
    work_guide_path = Column(String(500))  # ruta del documento guia para el taller
    notes = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
