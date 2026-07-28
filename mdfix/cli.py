import typer
from pathlib import Path

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
    print(f"Scanning {path}")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    if ctx.invoked_subcommand is None:
        scan(Path("."))