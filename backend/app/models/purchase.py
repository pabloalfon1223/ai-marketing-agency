from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from datetime import datetime, timezone
from app.database import Base


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), nullable=False, unique=True)
    product = Column(String(100), nullable=False)  # mente-pausada-ebook, etc
    amount = Column(Float, nullable=False)  # precio en USD
    currency = Column(String(10), default="USD")
    status = Column(String(20), default="completed")  # completed, refunded, pending
    payment_method = Column(String(50))  # stripe, mercadopago, etc
    payment_id = Column(String(200))  # ID transaccion externa

    # Email tracking
    email_sequence_status = Column(String(50), default="pending")  # pending, sent_1, sent_2, sent_3, sent_4, sent_5, completed
    email_sent_count = Column(Integer, default=0)
    last_email_sent_at = Column(DateTime)

    # Analytics
    source = Column(String(100))  # google, meta, organic, direct
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))

    # Timestamps
    purchased_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Notes
    notes = Column(Text)
