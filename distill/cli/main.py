import json

import typer
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

app = typer.Typer(
    name="distill",
    help="Consume long-form content intelligently — YouTube, podcasts, books.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def process(
    url: str = typer.Argument(help="YouTube URL to process"),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        envvar="ANTHROPIC_API_KEY",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
    ),
    model: str = typer.Option(
        "claude-sonnet-4-20250514",
        "--model",
        "-m",
        help="Claude model to use",
    ),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        help="Save output to file",
    ),
    fmt: str = typer.Option(
        "rich",
        "--format",
        "-f",
        help="Output format: rich, json, markdown",
    ),
):
    """Process a YouTube video into a structured, digestible breakdown."""
    if not api_key:
        console.print(
            "[red]Error:[/red] No API key. Set ANTHROPIC_API_KEY or use --api-key."
        )
        raise typer.Exit(1)

    from distill.core.analyze import analyze_transcript
    from distill.core.transcribe import (
        format_transcript_with_timestamps,
        get_transcript,
        get_video_duration,
    )

    # Step 1: Fetch transcript
    with console.status("[bold blue]Fetching transcript..."):
        try:
            segments, video_id = get_transcript(url)
        except Exception as e:
            console.print(f"[red]Error fetching transcript:[/red] {e}")
            raise typer.Exit(1)

    transcript_text = format_transcript_with_timestamps(segments)
    duration = get_video_duration(segments)
    word_count = len(transcript_text.split())
    token_estimate = int(word_count * 1.3)

    console.print(
        f"[green]✓[/green] Transcript fetched — "
        f"{len(segments):,} segments, ~{token_estimate:,} tokens"
    )

    # Step 2: Analyze with Claude
    with console.status("[bold blue]Analyzing with Claude..."):
        try:
            result = analyze_transcript(
                transcript_text=transcript_text,
                video_url=url,
                duration_seconds=duration,
                api_key=api_key,
                model=model,
            )
        except Exception as e:
            console.print(f"[red]Error during analysis:[/red] {e}")
            raise typer.Exit(1)

    console.print(
        f"[green]✓[/green] Analysis complete — "
        f"{result.total_sections} sections identified\n"
    )

    # Step 3: Output
    if fmt == "json":
        json_str = result.model_dump_json(indent=2)
        if output:
            with open(output, "w") as f:
                f.write(json_str)
            console.print(f"[green]✓[/green] Saved to {output}")
        else:
            console.print(json_str)
    elif fmt == "markdown":
        md = _render_markdown(result)
        if output:
            with open(output, "w") as f:
                f.write(md)
            console.print(f"[green]✓[/green] Saved to {output}")
        else:
            console.print(md)
    else:
        _render_rich(result)
        if output:
            with open(output, "w") as f:
                f.write(result.model_dump_json(indent=2))
            console.print(f"\n[green]✓[/green] JSON saved to {output}")


def _render_rich(result):
    """Render result with rich formatting in terminal."""
    from distill.core.models import DistillResult

    # Header panel
    console.print(
        Panel(
            f"[bold]{result.title}[/bold]\n\n"
            f"{result.overview}\n\n"
            f"[dim]{result.duration} • {result.total_sections} sections • "
            f"{result.source_url}[/dim]",
            title="[bold blue]distill[/bold blue]",
            border_style="blue",
        )
    )

    # Sections
    console.print("\n[bold underline]Sections[/bold underline]\n")
    for i, section in enumerate(result.sections, 1):
        console.print(
            f"  [bold cyan]{i}. {section.title}[/bold cyan]  "
            f"[dim]{section.timestamp.format()}[/dim]"
        )
        console.print(f"     {section.summary}")
        for point in section.key_points:
            console.print(f"     [green]•[/green] {point}")
        for quote in section.notable_quotes:
            console.print(f'     [yellow]"[/yellow][italic]{quote}[/italic][yellow]"[/yellow]')
        console.print()

    # Key Takeaways
    console.print("[bold underline]Key Takeaways[/bold underline]\n")
    for takeaway in result.key_takeaways:
        console.print(f"  [bold green]→[/bold green] {takeaway}")

    # Concept Map
    console.print("\n[bold underline]Concept Map[/bold underline]\n")
    tree = Tree("[bold]Topics[/bold]")
    for link in result.concept_map.links:
        tree.add(
            f"[cyan]{link.source}[/cyan] → [cyan]{link.target}[/cyan]  "
            f"[dim]({link.relationship})[/dim]"
        )
    console.print(tree)
    console.print()


def _render_markdown(result) -> str:
    """Render result as a markdown string."""
    lines = [
        f"# {result.title}",
        "",
        f"> {result.overview}",
        "",
        f"**Duration:** {result.duration} | "
        f"**Sections:** {result.total_sections} | "
        f"**Source:** {result.source_url}",
        "",
        "---",
        "",
        "## Sections",
        "",
    ]

    for i, section in enumerate(result.sections, 1):
        lines.append(f"### {i}. {section.title} ({section.timestamp.format()})")
        lines.append("")
        lines.append(section.summary)
        lines.append("")
        for point in section.key_points:
            lines.append(f"- {point}")
        lines.append("")
        if section.notable_quotes:
            for quote in section.notable_quotes:
                lines.append(f'> "{quote}"')
            lines.append("")

    lines.append("## Key Takeaways")
    lines.append("")
    for takeaway in result.key_takeaways:
        lines.append(f"- {takeaway}")
    lines.append("")

    lines.append("## Concept Map")
    lines.append("")
    for link in result.concept_map.links:
        lines.append(
            f"- **{link.source}** → **{link.target}** ({link.relationship})"
        )
    lines.append("")

    return "\n".join(lines)


def main():
    app()


if __name__ == "__main__":
    app()
