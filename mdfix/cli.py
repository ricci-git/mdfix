from pathlib import Path
from typing import Annotated

import typer

from .diagnostics import Diagnostic

# Нові імпорти для лінтингу
from .linter import Linter
from .rules.md001_heading_skip import Md001HeadingSkipRule
from .scanner import scan_markdown_files

# ВИПРАВЛЕННЯ ТУТ:
from .version import __version__ as package_version

app = typer.Typer(
    no_args_is_help=False,
    add_completion=False,
)

@app.command()
def version():
    """Show version."""
    print(f"mdfix {package_version}")


DEFAULT_SCAN_PATH = Path(".")

@app.command()
def scan(
    path: Annotated[Path, typer.Argument()] = DEFAULT_SCAN_PATH,
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


# --- NEW LOGIC FOR LINTING ---

def run_lint_logic(target_path: Path) -> list[Diagnostic]:
    """
    Core logic for linting a single file or directory of markdown files.
    Separated from CLI output for easier testing.
    """
    rules = [Md001HeadingSkipRule()]
    linter = Linter(rules=rules)
    
    all_diagnostics: list[Diagnostic] = []
    
    if target_path.is_dir():
        # Scan recursively
        markdown_files = scan_markdown_files(target_path)
        paths_to_check = [mf.path for mf in markdown_files]
    else:
        # Single file
        paths_to_check = [target_path]
        
    for file_path in paths_to_check:
        diags = linter.lint(file_path)
        all_diagnostics.extend(diags)
        
    return all_diagnostics


@app.command()
def lint(
    path: Annotated[Path, typer.Argument(help="File or directory to lint")] = DEFAULT_SCAN_PATH,
):
    """Analyze Markdown files for common issues."""
    
    diagnostics = run_lint_logic(path)
    
    if not diagnostics:
        typer.echo(typer.style("No issues found.", fg="green"))
        raise typer.Exit(code=0)
    
    typer.echo(typer.style(f"Found {len(diagnostics)} issue(s):", fg="red"))
    
    for diag in diagnostics:
        location = f"{diag.file_path}:{diag.line_start}:{diag.col_start}"
        severity_color = "yellow" if diag.severity.value == "warning" else "red"
        
        message = (
            f"{typer.style(location, fg='blue')} "
            f"[{typer.style(diag.rule_id, fg=severity_color)}] "
            f"{diag.message}"
        )
        typer.echo(message)
        
    # Exit with non-zero code if errors/warnings found (standard for CI/CD tools)
    raise typer.Exit(code=1)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    if ctx.invoked_subcommand is None:
        scan(Path("."))
