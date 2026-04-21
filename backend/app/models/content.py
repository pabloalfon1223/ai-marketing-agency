from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    content_type = Column(String(50))  # blog | social_post | email | ad_copy | landing_page
    title = Column(String(500))
    body = Column(Text)
    platform = Column(String(50))  # instagram | linkedin | twitter | email | blog | google_ads
    status = Column(String(20), default="draft")  # draft | review | approved | published | rejected
    seo_score = Column(Float)  # 0-100
    seo_suggestions = Column(Text)  # JSON from SEO agent
    review_notes = Column(Text)
    agent_id = Column(String(50))  # which agent generated it
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    campaign = relationship("Campaign", back_populates="contents")
    project = relationship("Project", back_populates="contents")
