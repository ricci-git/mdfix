from pathlib import Path

import typer

from .scanner import scan_markdown_files
from .version import __version__

app = typer.Typer(
    no_args_is_help=False,
    add_completion=False,
)


@app.command()
def version():
    """Show version."""
    print(f"mdfix {__version__}")


@app.command()
def scan(
    path: Path = typer.Argument(Path(".")),
):
    """Scan markdown files."""

    files = scan_markdown_files(path)

    print(f"Scanning: {path}")
    print()

    if not files:
        print("No markdown files found.")
        return

    print("Markdown files found:")

    for file in files:
        print(f"- {file.path} ({file.size} bytes)")

    print()
    print(f"Total: {len(files)} files")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    if ctx.invoked_subcommand is None:
        scan(Path("."))