from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class CampaignBase(BaseModel):
    project_id: int
    name: str
    campaign_type: Optional[str] = None
    status: Optional[str] = "draft"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    target_channels: Optional[str] = None
    strategy_brief: Optional[str] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    campaign_type: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    target_channels: Optional[str] = None
    strategy_brief: Optional[str] = None


class CampaignResponse(CampaignBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
