from pydantic import BaseModel
from typing import Optional


class AgentRunRequest(BaseModel):
    agent_type: str
    task_type: str
    project_id: Optional[int] = None
    campaign_id: Optional[int] = None
    input_data: Optional[str] = None


class AgentStatusResponse(BaseModel):
    agent_type: str
    display_name: str
    description: str
    status: str  # idle | busy
    tasks_completed: int
    tasks_running: int


class AgentLogResponse(BaseModel):
    id: int
    task_id: int
    agent_type: Optional[str] = None
    log_level: Optional[str] = None
    message: Optional[str] = None
    created_at: str

    model_config = {"from_attributes": True}
