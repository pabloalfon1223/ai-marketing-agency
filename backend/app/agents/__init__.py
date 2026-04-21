from app.agents.claude_client import ClaudeClient
from app.agents.base import BaseAgent
from app.agents.tool_registry import ALL_TOOLS

from app.agents.strategy import StrategyAgent
from app.agents.content_agent import ContentAgent
from app.agents.seo import SEOAgent
from app.agents.social_media import SocialMediaAgent
from app.agents.email_marketing import EmailMarketingAgent
from app.agents.analytics_agent import AnalyticsAgent
from app.agents.branding import BrandingAgent
from app.agents.advertising import AdvertisingAgent
from app.agents.orchestrator import OrchestratorAgent

AGENT_MAP: dict[str, type[BaseAgent]] = {
    "orchestrator": OrchestratorAgent,
    "strategy": StrategyAgent,
    "content": ContentAgent,
    "seo": SEOAgent,
    "social_media": SocialMediaAgent,
    "email_marketing": EmailMarketingAgent,
    "analytics": AnalyticsAgent,
    "branding": BrandingAgent,
    "advertising": AdvertisingAgent,
}

__all__ = [
    "ClaudeClient",
    "BaseAgent",
    "ALL_TOOLS",
    "AGENT_MAP",
    "StrategyAgent",
    "ContentAgent",
    "SEOAgent",
    "SocialMediaAgent",
    "EmailMarketingAgent",
    "AnalyticsAgent",
    "BrandingAgent",
    "AdvertisingAgent",
    "OrchestratorAgent",
]
