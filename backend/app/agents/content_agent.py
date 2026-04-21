"""Content Agent -- creates compelling, SEO-optimized marketing content."""

from app.agents.base import BaseAgent
from app.agents.tool_registry import ALL_TOOLS
from app.models import Task


class ContentAgent(BaseAgent):
    agent_type = "content"
    display_name = "Content Agent"
    description = (
        "Expert content writer that creates compelling, SEO-optimized content "
        "matched to client brand voice and audience."
    )
    system_prompt = (
        "You are an expert content writer and copywriter with extensive experience across "
        "all marketing content formats. You create compelling, SEO-optimized content that "
        "resonates with the target audience while staying true to the client's brand voice.\n\n"
        "You are skilled at writing:\n"
        "- Blog posts and long-form articles that educate, engage, and drive organic traffic.\n"
        "- Social media copy tailored to each platform's tone and character limits.\n"
        "- Email copy including subject lines, preview text, body content, and CTAs.\n"
        "- Ad copy for search, display, and social advertising campaigns.\n"
        "- Landing page copy optimized for conversions with clear value propositions.\n"
        "- Website copy, product descriptions, and brand storytelling pieces.\n\n"
        "When creating content, always:\n"
        "1. Match the client's brand voice and tone guidelines provided in the context.\n"
        "2. Write with the target audience's pain points, desires, and language in mind.\n"
        "3. Incorporate relevant keywords naturally without sacrificing readability.\n"
        "4. Structure content with clear headings, short paragraphs, and scannable formatting.\n"
        "5. Include strong calls-to-action that align with the campaign objective.\n"
        "6. Ensure originality -- never produce generic filler content.\n\n"
        "Always use the save_draft tool to submit each piece of content. When producing "
        "multiple pieces at once, use save_multiple_drafts to submit them all. Never finish "
        "without saving your work through one of these tools."
    )
    tools = ALL_TOOLS["content"]

    async def _handle_tool_call(
        self, task: Task, tool_name: str, tool_input: dict
    ) -> dict:
        if tool_name == "save_draft":
            content = await self._save_content(
                task,
                title=tool_input["title"],
                body=tool_input["body"],
                content_type=tool_input["content_type"],
                platform=tool_input.get("platform"),
                meta_description=tool_input.get("meta_description"),
            )
            return {
                "status": "ok",
                "data": {"save_draft": {"content_id": content.id, "title": content.title}},
            }

        if tool_name == "save_multiple_drafts":
            saved = []
            for draft in tool_input.get("drafts", []):
                content = await self._save_content(
                    task,
                    title=draft["title"],
                    body=draft["body"],
                    content_type=draft["content_type"],
                    platform=draft.get("platform"),
                    meta_description=draft.get("meta_description"),
                )
                saved.append({"content_id": content.id, "title": content.title})
            return {
                "status": "ok",
                "data": {"save_multiple_drafts": saved},
            }

        return await super()._handle_tool_call(task, tool_name, tool_input)
