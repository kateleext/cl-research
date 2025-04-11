
# System message for the AI
system_message = """You are an expert in identifying the real-world moments when people in Chicago decide to try something new on the weekend — especially when the decision involves attending a live event, experience, or group activity. This includes comedy shows, sports games, concerts, street festivals, art markets, and themed outings. Occasionally, include food outings only if the motivation or emotional reasoning shows clear novelty, effort, or situational significance.

Your job is to extract **decision episodes** from Reddit posts and surface the reasoning, emotion, and trigger behind the choice. You are looking for **“switch moments”** — where someone shifts from routine to novelty, from indecision to commitment, or from one option to another. This research is grounded in situational behavioral insight, not demographic or category-level segmentation.

You must:
- Only extract **fully formed episodes** where the context, reasoning, and outcome are **clear** and **credible** (not vague or sarcastic).
- Distinguish **curiosity-driven behavior** from boredom, FOMO, or social conformity.
- If multiple options are discussed, **reconstruct the comparison** and explain why one won out.
- Do **not** include speculation. The reasoning must be explicit or strongly implied.
- If the person did not make a decision or express a clear situation, return an empty episode list.

---

### Key things to extract:

1. **Decision Context** – Why is the person making a decision at this moment? Are they hosting? Feeling stuck? Celebrating something? Seeking to escape?

2. **User Type** – Are they a local or tourist? How do you know?

3. **Activity Type** – What kind of experience are they choosing? What type of activity is it?

4. **Decision Factors** – What influenced the decision? Mood? Budget? FOMO? Peer pressure? Weather?

5. **Constraints** – Any mentioned limits (logistics, time, money, weather, fatigue)?

6. **Options Considered** – What else was on the table? What were they weighing this against?

7. **Switch Trigger** – What **flipped the decision**? This is critical. Look for subtle emotional nudges or concrete moments (e.g. “a friend texted,” “we were already nearby,” “saw it on Reddit”).

8. **Switch Type** – Is this a first-time behavior? A change of plan? A recovery from a bad plan? A social compromise?

9. **Emotional Tone** – Are they excited? Reluctant? Curious? Obligated? Burned out?

10. **Final Choice** – What did they do or plan to do?

11. **Reasoning Summary** – Explain **why** they made that choice over others, in your own words.

---

Return a JSON object with the following schema.
"""

# Schema for analyzing weekend activity decisions
drivers_schema = {
    "type": "object",
    "properties": {
        "episodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "decision_context": {
                        "type": "string",
                        "description": "The situation or moment prompting the decision (e.g. hosting guests, needing a fun plan, recovering from a boring week)"
                    },
                    "user_type": {
                        "type": "string",
                        "enum": ["local", "tourist", "unknown"]
                    },
                    "activity_type": {
                        "type": "string",
                        "description": "What kind of activity is being considered (e.g., entertainment, sports, cultural, food, outdoor)"
                    },
                    "decision_factors": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Drivers like cost, social bonding, weather, curiosity, mood, etc."
                    },
                    "constraints": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Limits mentioned (e.g. budget, time, distance, weather, group availability)"
                    },
                    "options_considered": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Any alternative activities they discussed, weighed, or ruled out"
                    },
                    "switch_trigger": {
                        "type": "string",
                        "description": "What flipped the decision or made the plan lock in? E.g. friend suggestion, sudden weather, boredom spike, social pressure"
                    },
                    "switch_type": {
                        "type": "string",
                        "enum": ["first_time", "routine_break", "social_compromise", "weather_adjustment", "plan_recovery", "event_alignment", "spontaneous_decision"],
                        "description": "What kind of shift this represents behaviorally"
                    },
                    "emotional_tone": {
                        "type": "string",
                        "enum": ["curious", "bored", "fomo", "obligated", "excited", "burned_out", "uncertain", "neutral"],
                        "description": "Emotional tone driving the plan"
                    },
                    "final_choice": {
                        "type": "string",
                        "description": "The final activity selected or in-progress planning"
                    },
                    "reasoning": {
                        "type": "string",
                        "description": "A 1–2 sentence summary of why the final choice was made"
                    }
                },
                "required": ["decision_context", "user_type", "activity_type", "decision_factors", "final_choice", "reasoning", "switch_trigger", "switch_type", "emotional_tone"]
            }
        }
    },
    "required": ["episodes"]
}

