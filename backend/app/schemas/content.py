from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ContentBase(BaseModel):
    project_id: int
    campaign_id: Optional[int] = None
    content_type: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    platform: Optional[str] = None
    status: Optional[str] = "draft"


class ContentCreate(ContentBase):
    pass


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    platform: Optional[str] = None
    status: Optional[str] = None
    review_notes: Optional[str] = None


class ContentStatusUpdate(BaseModel):
    status: str  # approved | rejected
    review_notes: Optional[str] = None


class ContentResponse(ContentBase):
    id: int
    seo_score: Optional[float] = None
    seo_suggestions: Optional[str] = None
    review_notes: Optional[str] = None
    agent_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
