# distill

Consume long-form content intelligently. YouTube videos, podcasts, books — broken down into structured, digestible sections without losing the important details.

No more choosing between watching a 3-hour podcast or reading a 5-bullet summary that misses everything. Distill gives you the full information architecture: sections, key points, verbatim quotes, concept maps, and timestamps.

## How It Works

Paste a YouTube URL → get a structured breakdown:

- **Sections** with timestamps and one-line summaries
- **Key points** that capture substance, not fluff
- **Notable quotes** pulled verbatim from the transcript
- **Concept map** showing how topics connect
- **Key takeaways** — the insights that actually matter

## Install

```bash
pip install distill-ai
```

Or clone and install locally:

```bash
git clone https://github.com/ArastuK/distill.git
cd distill
pip install -e .
```

## Usage

### Pipe into any LLM (no API key needed)

The easiest way — pipe directly into Claude Code, Codex, or any LLM tool you already use:

```bash
distill fetch "https://youtube.com/watch?v=..." | claude
distill fetch "https://youtube.com/watch?v=..." | codex
```

The analysis prompt is baked in. No extra typing needed.

Use `--raw` if you just want the transcript:

```bash
distill fetch "https://youtube.com/watch?v=..." --raw > transcript.txt
```

### Standalone (BYOK)

Process a video end-to-end with your own Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-key-here"

# Rich terminal output (default)
distill process "https://youtube.com/watch?v=..."

# Markdown
distill process "https://youtube.com/watch?v=..." --format markdown

# JSON (for programmatic use)
distill process "https://youtube.com/watch?v=..." --format json

# Save to file
distill process "https://youtube.com/watch?v=..." --format markdown -o notes.md
```

### Choose your model

```bash
distill process "https://youtube.com/watch?v=..." -m claude-opus-4-20250514
```

## What You Get

For a 12-minute TED talk, distill produces something like:

```
┌─────────────────────────────── distill ───────────────────────────────┐
│ How to Stay Calm When You Know You'll Be Stressed — Daniel Levitin   │
│                                                                       │
│ Neuroscientist Daniel Levitin introduces the "pre-mortem" — a         │
│ strategy for anticipating failures before they happen, applied to     │
│ everyday life and high-stakes medical decisions.                      │
│                                                                       │
│ 12m • 7 sections • youtube.com/watch?v=8jPQjjsBbIc                   │
└───────────────────────────────────────────────────────────────────────┘

Sections

  1. The Locked-Out Story  0:13 - 2:58
     Breaking into his own house in -40° Montreal winter...
     • Cortisol from stress clouds thinking without you realizing
     • Led to cascade: broken window → forgot passport → lost seat
     "I didn't know it was cloudy because my thinking was cloudy."

  2. The Pre-Mortem Concept  2:59 - 3:58
     ...
```

## Token Estimates

| Content | Words | Tokens | Cost (Sonnet) |
|---|---|---|---|
| 12 min TED talk | ~2,500 | ~3,200 | ~$0.02 |
| 1 hour podcast | ~9,000 | ~12,000 | ~$0.05 |
| 3-4 hour podcast | ~36,000 | ~47,000 | ~$0.20 |

## Use It As a Library

```python
from distill.core.transcribe import get_transcript, format_transcript_with_timestamps
from distill.core.analyze import analyze_transcript

segments, video_id = get_transcript("https://youtube.com/watch?v=...")
transcript = format_transcript_with_timestamps(segments)

result = analyze_transcript(
    transcript_text=transcript,
    video_url="https://youtube.com/watch?v=...",
    duration_seconds=3600,
    api_key="your-key",
)

print(result.model_dump_json(indent=2))
```

## Roadmap

- [ ] PDF / book support
- [ ] Podcast RSS feed support
- [ ] Interactive concept map visualization
- [ ] MCP server (use distill as a tool inside Claude Code)
- [ ] Web UI
- [ ] Cross-content knowledge graph

## Contributing

PRs welcome. The architecture is modular — input sources, LLM providers, and output formats are all independent:

```
distill/
├── core/
│   ├── models.py       ← Pydantic data models
│   ├── transcribe.py   ← YouTube transcript fetching
│   └── analyze.py      ← LLM analysis pipeline
└── cli/
    └── main.py         ← Typer CLI
```

Adding a new input source? Add a module to `core/`. Adding a new output format? Add a renderer in `cli/main.py`.

## License

MIT
