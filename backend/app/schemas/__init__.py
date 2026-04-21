from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.schemas.content import ContentCreate, ContentUpdate, ContentResponse, ContentStatusUpdate
from app.schemas.task import TaskCreate, TaskResponse
from app.schemas.agent import AgentRunRequest, AgentStatusResponse, AgentLogResponse
from app.schemas.potencial import (
    PotencialBase,
    PotencialCreate,
    PotencialUpdate,
    PotencialResponse,
    PotencialListResponse,
)
from app.schemas.produccion import (
    ProduccionBase,
    ProduccionCreate,
    ProduccionUpdate,
    ProduccionResponse,
    ProduccionListResponse,
)
