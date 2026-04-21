from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    project_id: Optional[int] = None
    campaign_id: Optional[int] = None
    agent_type: str
    task_type: str
    input_data: Optional[str] = None
    priority: Optional[int] = 5


class TaskResponse(BaseModel):
    id: int
    project_id: Optional[int] = None
    campaign_id: Optional[int] = None
    agent_type: str
    task_type: str
    input_data: Optional[str] = None
    output_data: Optional[str] = None
    status: str
    priority: int
    parent_task_id: Optional[int] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}
