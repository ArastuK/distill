import re

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def get_transcript(url: str) -> tuple[list[dict], str]:
    """Fetch transcript from YouTube.

    Returns (transcript_segments, video_id).
    """
    video_id = extract_video_id(url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript, video_id


def format_transcript_with_timestamps(segments: list[dict]) -> str:
    """Format transcript segments into timestamped text."""
    lines = []
    for seg in segments:
        start = seg["start"]
        h = int(start // 3600)
        m = int((start % 3600) // 60)
        s = int(start % 60)
        if h > 0:
            ts = f"[{h}:{m:02d}:{s:02d}]"
        else:
            ts = f"[{m}:{s:02d}]"
        lines.append(f"{ts} {seg['text']}")
    return "\n".join(lines)


def get_video_duration(segments: list[dict]) -> float:
    """Get total duration in seconds from transcript segments."""
    if not segments:
        return 0
    last = segments[-1]
    return last["start"] + last.get("duration", 0)
