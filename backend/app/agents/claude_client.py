import anthropic

from app.config import get_settings


class ClaudeClient:
    """Thin async wrapper around anthropic.AsyncAnthropic."""

    def __init__(self):
        settings = get_settings()
        self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.default_model = settings.default_model

    async def create(self, **kwargs):
        """Create a message, falling back to the default model when none is specified."""
        if "model" not in kwargs:
            kwargs["model"] = self.default_model
        return await self.client.messages.create(**kwargs)
