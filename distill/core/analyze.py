import json

import anthropic

from .models import DistillResult

SYSTEM_PROMPT = """You are a content analysis expert. Your job is to break down long-form content into structured, digestible sections that preserve all important details. Be thorough — don't dumb things down. Capture the substance."""

ANALYSIS_PROMPT = """Analyze this transcript and produce a structured breakdown.

TRANSCRIPT:
{transcript}

Return a JSON object with this exact schema:
{{
    "title": "descriptive title for this content",
    "overview": "2-3 sentence overview of the entire content",
    "sections": [
        {{
            "title": "section title",
            "summary": "one-line summary of this section",
            "key_points": ["substantive point 1", "substantive point 2"],
            "notable_quotes": ["exact quote from transcript"],
            "timestamp": {{"start": 0.0, "end": 120.0}}
        }}
    ],
    "concept_map": {{
        "topics": ["topic1", "topic2"],
        "links": [
            {{"source": "topic1", "target": "topic2", "relationship": "how they connect"}}
        ]
    }},
    "key_takeaways": ["takeaway 1", "takeaway 2"]
}}

Rules:
- Identify natural topic boundaries for sections (aim for 5-15 sections depending on content length)
- Timestamps must correspond to the [MM:SS] or [H:MM:SS] markers in the transcript
- Notable quotes should be verbatim from the transcript — pick the most insight-dense ones
- Key points should capture substance, not fluff — be specific
- Concept map should show how major topics relate to each other (8-15 topics)
- Key takeaways: the 5-10 most important insights from the entire content

Return ONLY valid JSON, no other text."""


def analyze_transcript(
    transcript_text: str,
    video_url: str,
    duration_seconds: float,
    api_key: str,
    model: str = "claude-sonnet-4-20250514",
) -> DistillResult:
    """Analyze a transcript and produce a structured breakdown."""
    client = anthropic.Anthropic(api_key=api_key)

    # Format duration for display
    h = int(duration_seconds // 3600)
    m = int((duration_seconds % 3600) // 60)
    duration_str = f"{h}h {m}m" if h > 0 else f"{m}m"

    message = client.messages.create(
        model=model,
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": ANALYSIS_PROMPT.format(transcript=transcript_text),
            }
        ],
    )

    response_text = message.content[0].text

    # Parse JSON — handle markdown code blocks
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    data = json.loads(response_text.strip())

    return DistillResult(
        title=data["title"],
        source_url=video_url,
        duration=duration_str,
        total_sections=len(data["sections"]),
        overview=data["overview"],
        sections=data["sections"],
        concept_map=data["concept_map"],
        key_takeaways=data["key_takeaways"],
    )
