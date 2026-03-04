<p align="center">
  <img src="assets/distill-owl.png" alt="distill mascot" width="400">
</p>

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

Tested on a **2h 24m Huberman Lab podcast** with Dr. David Eagleman (neuroplasticity, time perception, dreams, polarization):

```
┌─────────────────────────────────── distill ──────────────────────────────────┐
│ Huberman Lab: Dr. David Eagleman — Brain Plasticity, Time Perception,        │
│ Dreams & Polarization                                                        │
│                                                                              │
│ Neuroscientist David Eagleman joins Andrew Huberman for a wide-ranging       │
│ conversation on how the brain rewires itself, why time seems to speed up     │
│ as we age, the surprising reason we dream, and what neuroscience reveals     │
│ about political polarization.                                                │
│                                                                              │
│ 2h 24m • 11 sections • youtube.com/watch?v=lEULFeUVYf0                      │
└──────────────────────────────────────────────────────────────────────────────┘

Sections

  1. Neuroplasticity Fundamentals  0:00 - 5:43
     Mother nature's big trick: dropping humans into the world with a
     half-baked brain that the environment wires up.
     • DNA is only half the secret of life — experience wires the other half
     • 86 billion neurons constantly plugging and unplugging connections
     "They burst into the Eagle and Child pub and said, 'We've discovered
      the secret to life.' But that was really half the secret of life."

  2. The Cortex as a One-Trick Pony  5:43 - 11:07
     The outer 3mm of wrinkly brain is the same circuitry everywhere —
     defined by what you plug into it.
     • Mriganka Sur's MIT experiment: optic nerve into auditory cortex → vision
     • Blind people's visual cortex taken over by hearing and touch
     "The cortex is a one-trick pony. The reason it looks the same
      everywhere is because it is the same."

  3. Extending Plasticity — Seek Novelty  17:49 - 38:06
     ...

  Key Takeaways

  → Seek novelty relentlessly — once you're good at something, it stops
    driving plasticity. The agitation of learning IS the signal.
  → Memory density = time perception — novel experiences create more
    memories, which your brain interprets as more time elapsed.
  → Dreams defend visual cortex from takeover by other senses during
    nightly darkness. Only theory with cross-species predictions.

  Concept Map

  Topics
  ├── Neuroplasticity → Seeking novelty (extends plasticity in adults)
  ├── Neuroplasticity → Dreams (REM defends visual cortex)
  ├── Memory density → Time perception (more memories = feels longer)
  ├── Future self → Ulysses contracts (constrain future behavior)
  └── In-group/out-group → Polarization (empathy modulated by labels)
```

### How comprehensive is it?

We compared the output against the full transcript to measure coverage:

| Dimension | Score | Method |
|---|---|---|
| Topic coverage | 82% | 40 of ~50 significant topics captured |
| Quote fidelity | 90% | 9 of 10 quotes verified verbatim |
| Timestamp accuracy | 85% | Section boundaries within 2-5 min |
| Key entity coverage | 78% | 18 of 23 named people/researchers |
| Runtime coverage | 96% | 11 sections spanning full episode |
| **Overall** | **~83%** | |

What got missed? Mostly anecdotal color — Pixar's best animators being aphantasic, a capuchin monkey losing it because the other monkey got a grape, Eagleman's father learning 8 languages via girlfriends. The intellectual throughlines are fully captured; the storytelling flavor is where the remaining 17% lives.

## Token Estimates

| Content | Words | Tokens | Cost (Sonnet) |
|---|---|---|---|
| 12 min TED talk | ~2,500 | ~3,200 | ~$0.02 |
| 1 hour podcast | ~9,000 | ~12,000 | ~$0.05 |
| 2.5 hour podcast | ~33,000 | ~43,000 | ~$0.18 |
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
