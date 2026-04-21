from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from datetime import datetime, timezone
from app.database import Base


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String(100), nullable=False)  # saas, servicios, ecommerce, creator, hibrido

    # Viability scoring (0-100)
    demand_score = Column(Float)  # demanda (40% weight)
    scalability_score = Column(Float)  # escalabilidad a $20k (40% weight)
    competition_score = Column(Float)  # competencia y gaps (20% weight)
    overall_score = Column(Float)  # weighted average

    # Details
    target_market = Column(Text)  # descripcion del mercado objetivo
    revenue_model = Column(String(200))  # suscripcion, one-time, hibrido, etc
    estimated_time_to_20k = Column(String(100))  # "3-6 meses", "6-12 meses", etc
    initial_capital_required = Column(Float)  # USD estimado
    complexity = Column(String(50))  # low, medium, high

    # Validation details
    demand_evidence = Column(Text)  # Google Trends, Reddit, ProductHunt, etc findings
    competitor_analysis = Column(Text)  # competidores existentes, pricing, gaps
    mvp_outline = Column(Text)  # que seria el MVP minimo

    # Status & tracking
    status = Column(String(50), default="idea_cruda")  # idea_cruda, en_validacion, mvp_diseñado, mvp_en_desarrollo, mvp_validando, track_a_20k, exitosa, pivotada, descartada
    validation_started_at = Column(DateTime)
    last_update_at = Column(DateTime)
    owner = Column(String(100))  # quien esta validando esta idea

    # Results & learnings
    mvp_launch_date = Column(DateTime)  # cuando se lanzo el MVP
    current_monthly_revenue = Column(Float)  # USD, if in production
    reached_20k = Column(String(10), default="no")  # yes, no, in_progress
    learnings = Column(Text)  # que aprendimos en el proceso
    pivot_reason = Column(Text)  # si fue pivotada, por que
    discard_reason = Column(Text)  # si fue descartada, por que

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
