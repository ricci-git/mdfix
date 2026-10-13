from pathlib import Path
from typing import Annotated

import typer

from .diagnostics import Diagnostic

from .patcher import apply_fixes


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


# --- NEW LOGIC FOR FIXING ---

def run_fix_logic(target_path: Path, dry_run: bool = False) -> tuple[list[Path], dict[str, str]]:
    """
    Core logic for fixing markdown files.
    
    Args:
        target_path: File or directory to fix.
        dry_run: If True, calculates changes but does not write to disk.
        
    Returns:
        A tuple containing:
        - List of paths that WERE modified (or would be modified in dry-run).
        - Dictionary mapping absolute path strings to their NEW content.
    """
    rules = [Md001HeadingSkipRule()]
    linter = Linter(rules=rules)
    
    all_diags: list[Diagnostic] = []
    files_to_process: list[Path] = []
    
    if target_path.is_dir():
        markdown_files = scan_markdown_files(target_path)
        files_to_process = [mf.path for mf in markdown_files]
    else:
        files_to_process = [target_path]
        
    changed_files: list[Path] = []
    new_content_map: dict[str, str] = {}
    
    for file_path in files_to_process:
        diags = linter.lint(file_path)
        if not diags:
            continue
            
        # Read original content
        original_content = file_path.read_text(encoding='utf-8')
        
        # Apply fixes
        fixed_content = apply_fixes(original_content, diags)
        
        # Check if anything actually changed
        if fixed_content != original_content:
            abs_path_str = str(file_path.resolve())
            new_content_map[abs_path_str] = fixed_content
            changed_files.append(file_path)
            
            if not dry_run:
                file_path.write_text(fixed_content, encoding='utf-8')
                
    return changed_files, new_content_map


@app.command()
def fix(
    path: Annotated[Path, typer.Argument(help="File or directory to fix")] = DEFAULT_SCAN_PATH,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Show what would be changed without writing files")] = False,
):
    """Automatically fix common Markdown issues."""
    
    changed_files, new_content_map = run_fix_logic(path, dry_run=dry_run)
    
    if not changed_files:
        typer.echo(typer.style("No fixable issues found.", fg="green"))
        raise typer.Exit(code=0)
        
    action_word = "Would modify" if dry_run else "Modified"
    typer.echo(typer.style(f"{action_word} {len(changed_files)} file(s):", fg="yellow"))
    
    for file_path in changed_files:
        abs_path_str = str(file_path.resolve())
        old_content = file_path.read_text(encoding='utf-8') # Re-read for diff display if needed, or store in map
        new_content = new_content_map[abs_path_str]
        
        # Simple summary output
        typer.echo(f"- {file_path}")
        
        # Optional: Show unified diff here using difflib if desired for MVP
        # import difflib
        # diff = difflib.unified_diff(old_content.splitlines(), new_content.splitlines(), lineterm='')
        # for line in diff:
        #     typer.echo(line)

    if dry_run:
        typer.echo(typer.style("\n(DRY RUN: Files were NOT written to disk)", fg="cyan"))
        
    raise typer.Exit(code=0)


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
