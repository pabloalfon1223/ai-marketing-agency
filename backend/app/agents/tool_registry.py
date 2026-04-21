"""
Tool schemas for every agent in the AI Marketing Agency.

Each tool follows the Anthropic tool_use schema format:
  {"name": "...", "description": "...", "input_schema": {"type": "object", "properties": {...}, "required": [...]}}
"""

# ---------------------------------------------------------------------------
# Strategy Agent Tools
# ---------------------------------------------------------------------------

STRATEGY_TOOLS = [
    {
        "name": "save_strategy_brief",
        "description": "Save a complete marketing strategy brief.",
        "input_schema": {
            "type": "object",
            "properties": {
                "objective": {
                    "type": "string",
                    "description": "The primary marketing objective.",
                },
                "target_audience": {
                    "type": "string",
                    "description": "Description of the target audience.",
                },
                "key_messages": {
                    "type": "string",
                    "description": "Core messages to communicate.",
                },
                "channels": {
                    "type": "string",
                    "description": "Recommended marketing channels.",
                },
                "timeline": {
                    "type": "string",
                    "description": "Proposed timeline / schedule.",
                },
                "budget_allocation": {
                    "type": "string",
                    "description": "How the budget should be distributed.",
                },
            },
            "required": [
                "objective",
                "target_audience",
                "key_messages",
                "channels",
                "timeline",
                "budget_allocation",
            ],
        },
    },
    {
        "name": "save_swot",
        "description": "Save a SWOT analysis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "strengths": {
                    "type": "string",
                    "description": "Internal strengths.",
                },
                "weaknesses": {
                    "type": "string",
                    "description": "Internal weaknesses.",
                },
                "opportunities": {
                    "type": "string",
                    "description": "External opportunities.",
                },
                "threats": {
                    "type": "string",
                    "description": "External threats.",
                },
            },
            "required": ["strengths", "weaknesses", "opportunities", "threats"],
        },
    },
    {
        "name": "save_competitor_analysis",
        "description": "Save a competitor analysis with details for each competitor.",
        "input_schema": {
            "type": "object",
            "properties": {
                "competitors": {
                    "type": "array",
                    "description": "List of competitors with analysis.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Competitor name.",
                            },
                            "strengths": {
                                "type": "string",
                                "description": "Competitor strengths.",
                            },
                            "weaknesses": {
                                "type": "string",
                                "description": "Competitor weaknesses.",
                            },
                            "market_position": {
                                "type": "string",
                                "description": "Competitor market position.",
                            },
                        },
                        "required": [
                            "name",
                            "strengths",
                            "weaknesses",
                            "market_position",
                        ],
                    },
                },
            },
            "required": ["competitors"],
        },
    },
]

# ---------------------------------------------------------------------------
# Content Agent Tools
# ---------------------------------------------------------------------------

CONTENT_TOOLS = [
    {
        "name": "save_draft",
        "description": "Save a single content draft.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Content title.",
                },
                "body": {
                    "type": "string",
                    "description": "Full body / text of the content.",
                },
                "content_type": {
                    "type": "string",
                    "description": "Type of content (blog, article, landing_page, etc.).",
                },
                "platform": {
                    "type": "string",
                    "description": "Target platform.",
                },
                "meta_description": {
                    "type": "string",
                    "description": "SEO meta description.",
                },
            },
            "required": ["title", "body", "content_type", "platform"],
        },
    },
    {
        "name": "save_multiple_drafts",
        "description": "Save multiple content drafts at once.",
        "input_schema": {
            "type": "object",
            "properties": {
                "drafts": {
                    "type": "array",
                    "description": "List of content drafts.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Content title.",
                            },
                            "body": {
                                "type": "string",
                                "description": "Full body / text of the content.",
                            },
                            "content_type": {
                                "type": "string",
                                "description": "Type of content.",
                            },
                            "platform": {
                                "type": "string",
                                "description": "Target platform.",
                            },
                        },
                        "required": ["title", "body", "content_type", "platform"],
                    },
                },
            },
            "required": ["drafts"],
        },
    },
]

# ---------------------------------------------------------------------------
# SEO Agent Tools
# ---------------------------------------------------------------------------

SEO_TOOLS = [
    {
        "name": "save_keywords",
        "description": "Save keyword research results.",
        "input_schema": {
            "type": "object",
            "properties": {
                "primary_keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Primary target keywords.",
                },
                "secondary_keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Secondary keywords.",
                },
                "long_tail_keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Long-tail keyword phrases.",
                },
            },
            "required": [
                "primary_keywords",
                "secondary_keywords",
                "long_tail_keywords",
            ],
        },
    },
    {
        "name": "score_content",
        "description": "Score content for SEO quality and provide suggestions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "score": {
                    "type": "number",
                    "description": "SEO score from 0 to 100.",
                },
                "suggestions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Actionable SEO improvement suggestions.",
                },
                "keyword_density": {
                    "type": "number",
                    "description": "Keyword density percentage.",
                },
                "readability_score": {
                    "type": "number",
                    "description": "Readability score.",
                },
            },
            "required": [
                "score",
                "suggestions",
                "keyword_density",
                "readability_score",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Social Media Agent Tools
# ---------------------------------------------------------------------------

SOCIAL_MEDIA_TOOLS = [
    {
        "name": "save_calendar",
        "description": "Save a social media content calendar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "posts": {
                    "type": "array",
                    "description": "Scheduled posts for the calendar.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "platform": {
                                "type": "string",
                                "description": "Social media platform.",
                            },
                            "content": {
                                "type": "string",
                                "description": "Post content / copy.",
                            },
                            "hashtags": {
                                "type": "string",
                                "description": "Hashtags to include.",
                            },
                            "suggested_date": {
                                "type": "string",
                                "description": "Suggested publish date.",
                            },
                            "post_type": {
                                "type": "string",
                                "description": "Type of post (image, video, carousel, text, story).",
                            },
                        },
                        "required": [
                            "platform",
                            "content",
                            "hashtags",
                            "suggested_date",
                            "post_type",
                        ],
                    },
                },
            },
            "required": ["posts"],
        },
    },
    {
        "name": "save_post",
        "description": "Save a single social media post.",
        "input_schema": {
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "description": "Social media platform.",
                },
                "content": {
                    "type": "string",
                    "description": "Post content / copy.",
                },
                "hashtags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Hashtags to include.",
                },
                "call_to_action": {
                    "type": "string",
                    "description": "Call-to-action text.",
                },
                "media_suggestions": {
                    "type": "string",
                    "description": "Suggestions for accompanying media.",
                },
            },
            "required": ["platform", "content", "hashtags", "call_to_action"],
        },
    },
]

# ---------------------------------------------------------------------------
# Email Marketing Agent Tools
# ---------------------------------------------------------------------------

EMAIL_TOOLS = [
    {
        "name": "save_email_sequence",
        "description": "Save a multi-step email sequence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sequence_name": {
                    "type": "string",
                    "description": "Name of the email sequence.",
                },
                "emails": {
                    "type": "array",
                    "description": "Ordered list of emails in the sequence.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "subject": {
                                "type": "string",
                                "description": "Email subject line.",
                            },
                            "body": {
                                "type": "string",
                                "description": "Email body content.",
                            },
                            "send_day": {
                                "type": "integer",
                                "description": "Day number to send (relative to sequence start).",
                            },
                            "segment": {
                                "type": "string",
                                "description": "Target audience segment.",
                            },
                        },
                        "required": ["subject", "body", "send_day", "segment"],
                    },
                },
            },
            "required": ["sequence_name", "emails"],
        },
    },
    {
        "name": "save_subject_lines",
        "description": "Save subject line variants for A/B testing.",
        "input_schema": {
            "type": "object",
            "properties": {
                "variants": {
                    "type": "array",
                    "description": "Subject line variants with rationale.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "subject": {
                                "type": "string",
                                "description": "Subject line text.",
                            },
                            "rationale": {
                                "type": "string",
                                "description": "Why this variant may perform well.",
                            },
                        },
                        "required": ["subject", "rationale"],
                    },
                },
            },
            "required": ["variants"],
        },
    },
]

# ---------------------------------------------------------------------------
# Analytics Agent Tools
# ---------------------------------------------------------------------------

ANALYTICS_TOOLS = [
    {
        "name": "save_report",
        "description": "Save an analytics report with metrics and insights.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Report title.",
                },
                "period": {
                    "type": "string",
                    "description": "Reporting period (e.g. 'Q1 2026', 'March 2026').",
                },
                "metrics": {
                    "type": "object",
                    "description": "Key metrics as key-value pairs.",
                },
                "insights": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key insights drawn from the data.",
                },
                "recommendations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Actionable recommendations.",
                },
            },
            "required": ["title", "period", "metrics", "insights", "recommendations"],
        },
    },
    {
        "name": "save_kpi_setup",
        "description": "Save KPI definitions and targets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "kpis": {
                    "type": "array",
                    "description": "List of KPI definitions.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "KPI name.",
                            },
                            "target": {
                                "type": "string",
                                "description": "Target value or range.",
                            },
                            "measurement_method": {
                                "type": "string",
                                "description": "How this KPI is measured.",
                            },
                            "frequency": {
                                "type": "string",
                                "description": "Measurement frequency (daily, weekly, monthly, etc.).",
                            },
                        },
                        "required": [
                            "name",
                            "target",
                            "measurement_method",
                            "frequency",
                        ],
                    },
                },
            },
            "required": ["kpis"],
        },
    },
]

# ---------------------------------------------------------------------------
# Branding Agent Tools
# ---------------------------------------------------------------------------

BRANDING_TOOLS = [
    {
        "name": "save_brand_guidelines",
        "description": "Save brand voice and messaging guidelines.",
        "input_schema": {
            "type": "object",
            "properties": {
                "voice_tone": {
                    "type": "string",
                    "description": "Overall brand voice and tone description.",
                },
                "personality_traits": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Brand personality traits.",
                },
                "dos": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Brand communication dos.",
                },
                "donts": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Brand communication don'ts.",
                },
                "messaging_pillars": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Core messaging pillars.",
                },
                "tagline_options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Proposed tagline options.",
                },
            },
            "required": [
                "voice_tone",
                "personality_traits",
                "dos",
                "donts",
                "messaging_pillars",
                "tagline_options",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Advertising Agent Tools
# ---------------------------------------------------------------------------

ADVERTISING_TOOLS = [
    {
        "name": "save_ad_campaign",
        "description": "Save an advertising campaign plan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "campaign_name": {
                    "type": "string",
                    "description": "Name of the ad campaign.",
                },
                "platform": {
                    "type": "string",
                    "description": "Advertising platform (Google Ads, Meta, LinkedIn, etc.).",
                },
                "objective": {
                    "type": "string",
                    "description": "Campaign objective.",
                },
                "target_audience": {
                    "type": "string",
                    "description": "Target audience description.",
                },
                "budget": {
                    "type": "string",
                    "description": "Campaign budget.",
                },
                "ad_sets": {
                    "type": "array",
                    "description": "Ad sets within the campaign.",
                    "items": {
                        "type": "object",
                        "description": "An ad set with targeting and creative details.",
                    },
                },
            },
            "required": [
                "campaign_name",
                "platform",
                "objective",
                "target_audience",
                "budget",
                "ad_sets",
            ],
        },
    },
    {
        "name": "save_ad_copy",
        "description": "Save advertising copy for a single ad.",
        "input_schema": {
            "type": "object",
            "properties": {
                "headline": {
                    "type": "string",
                    "description": "Ad headline.",
                },
                "body": {
                    "type": "string",
                    "description": "Ad body copy.",
                },
                "call_to_action": {
                    "type": "string",
                    "description": "Call-to-action text.",
                },
                "platform": {
                    "type": "string",
                    "description": "Ad platform.",
                },
                "ad_format": {
                    "type": "string",
                    "description": "Ad format (search, display, video, carousel, etc.).",
                },
                "target_url": {
                    "type": "string",
                    "description": "Landing page / target URL.",
                },
            },
            "required": [
                "headline",
                "body",
                "call_to_action",
                "platform",
                "ad_format",
                "target_url",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Orchestrator Agent Tools
# ---------------------------------------------------------------------------

ORCHESTRATOR_TOOLS = [
    {
        "name": "delegate_task",
        "description": "Delegate a task to a specialist agent.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_type": {
                    "type": "string",
                    "description": "Type of agent to delegate to (strategy, content, seo, social_media, email, analytics, branding, advertising).",
                },
                "task_type": {
                    "type": "string",
                    "description": "Specific task for the agent to perform.",
                },
                "input_data": {
                    "type": "string",
                    "description": "JSON-encoded input data for the task.",
                },
                "priority": {
                    "type": "integer",
                    "description": "Task priority (1 = highest, 5 = lowest).",
                },
            },
            "required": ["agent_type", "task_type", "input_data", "priority"],
        },
    },
    {
        "name": "compile_results",
        "description": "Compile and summarize results from multiple agents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Executive summary of compiled results.",
                },
                "results": {
                    "type": "array",
                    "description": "Results from each agent.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "agent": {
                                "type": "string",
                                "description": "Agent type that produced the result.",
                            },
                            "task_type": {
                                "type": "string",
                                "description": "Task that was performed.",
                            },
                            "key_findings": {
                                "type": "string",
                                "description": "Key findings or output summary.",
                            },
                        },
                        "required": ["agent", "task_type", "key_findings"],
                    },
                },
            },
            "required": ["summary", "results"],
        },
    },
]

# ---------------------------------------------------------------------------
# Aggregate lookup
# ---------------------------------------------------------------------------

ALL_TOOLS: dict[str, list[dict]] = {
    "strategy": STRATEGY_TOOLS,
    "content": CONTENT_TOOLS,
    "seo": SEO_TOOLS,
    "social_media": SOCIAL_MEDIA_TOOLS,
    "email": EMAIL_TOOLS,
    "analytics": ANALYTICS_TOOLS,
    "branding": BRANDING_TOOLS,
    "advertising": ADVERTISING_TOOLS,
    "orchestrator": ORCHESTRATOR_TOOLS,
}
