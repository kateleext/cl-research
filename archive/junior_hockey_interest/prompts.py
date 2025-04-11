# prompts.py (multi-episode + insight scoring schema)

# Single decision unit schema
single_episode_schema = {
    "type": "object",
    "properties": {
        "include": {"type": "boolean"},
        "post_id": {"type": "string"},
        "post_title": {"type": "string"},

        "decision_summary": {"type": "string"},
        "factors_summary": {"type": "string"},
        "behavioral_insight": {"type": "string"},
        "evidence_quote": {"type": "string"},

        "drivers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "description": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["High", "Medium", "Low"]},
                    "evidence": {"type": "string"}
                },
                "required": ["label", "description", "confidence", "evidence"]
            }
        },

        "fan_engagement_level": {
            "type": "string",
            "enum": ["Observer", "Casual Fan", "Participant", "Deep Fan"]
        },

        "fan_onboarding_signal": {
            "type": "string",
            "enum": ["None", "Considering", "First-Time Attendee", "Emerging Fan", "Converted Fan"]
        },

        "hockey_context_type": {
            "type": "string",
            "enum": ["Professional", "Junior", "Recreational", "Pickup", "Watch Party", "Other"]
        },

        "event_stage": {
            "type": "string",
            "enum": ["Considering", "Planning", "Attending", "Reflecting"]
        },

        "group_context": {
            "type": "string",
            "enum": ["Solo", "Couple", "Small Group", "Large Group", "Family", "Unknown"]
        },

        "emotional_state": {
            "type": "string",
            "enum": [
                "Energized", "Burned Out", "Curious", "Lonely", "Restless",
                "Relaxed", "Anxious", "Indifferent", "Unknown"
            ]
        },

        "alternative_considered": {"type": "string"},
        "potential_barrier": {"type": "string"},

        "has_sufficient_context": {"type": "boolean"},
        "context_gaps": {
            "type": "array",
            "items": {"type": "string"}
        },

        "insight_quality": {
            "type": "string",
            "enum": ["Superficial", "Moderate", "Deep"]
        }
    },
    "required": [
        "include", "post_id", "post_title", "decision_summary", "factors_summary",
        "behavioral_insight", "evidence_quote", "drivers", "fan_engagement_level",
        "fan_onboarding_signal", "hockey_context_type", "event_stage",
        "has_sufficient_context", "context_gaps", "insight_quality"
    ],
    "additionalProperties": False
}

# Multi-episode wrapper schema
flexible_drivers_schema = {
    "type": "object",
    "properties": {
        "episodes": {
            "type": "array",
            "items": single_episode_schema
        }
    },
    "required": ["episodes"],
    "additionalProperties": False
}

# System prompt
system_message = """
You are an assistant trained to analyze Reddit posts and identify situational drivers behind a user's interest in junior hockey, particularly if they've been to a game. Many of these posts are of a more generic nature, and don't exhibit much energy; don't over-analyze them. You'll be fed many many posts, so only include those that offer genuine insight.

- Focus ONLY on junior hockey contexts (e.g. USHL, development leagues, suburban teams).
- If the post refers exclusively to NHL, watching TV, or general hockey chat with no event context, set `include` = false.
When `include` = false:
- Return an empty object.

When `include` = true:
- Return an object with an `episodes` array, where each item represents a distinct behavioral decision from the post or its comments.
- Each `episode` must:
  - Include summaries of decision logic, drivers, and evidence
  - Provide emotional context, potential blockers, and fan conversion state
  - Tag any information gaps using `context_gaps`
  - Score the `insight_quality` as one of:
    - "Superficial": Minimal context or generic behavior
    - "Moderate": Shows motivation or intent but limited emotional/situational richness
    - "Deep": Clear, personal, emotionally grounded moment of decision or reflection

Prioritize insight depth and clarity over quantity. Avoid inventing signals when information is missing.
"""

drivers_schema = flexible_drivers_schema
