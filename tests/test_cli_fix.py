from pathlib import Path

from mdfix.cli import run_fix_logic


def test_run_fix_logic_dry_run_does_not_modify_file(tmp_path: Path):
    """
    Verify that dry-run mode returns an empty map of changes when no fixes are applicable.
    Since MD001 currently has no auto-fix suggestion, nothing should change.
    """
    md_file = tmp_path / "bad.md"
    content = "# Title\n### Subtitle\n"
    md_file.write_text(content)

    # Run fix logic in dry-run mode
    changed_files, new_content_map = run_fix_logic(md_file, dry_run=True)

    # Assertions
    # 1. No files were marked as changed because there were no valid suggestions
    assert len(changed_files) == 0
    
    # 2. The map of new contents is empty because no modifications occurred
    assert new_content_map == {}
    
    # 3. Crucially: the file on disk remains EXACTLY as it was
    assert md_file.read_text() == content


def test_run_fix_logic_writes_to_disk_when_not_dry_run(tmp_path: Path):
    """
    Verify that non-dry-run mode behaves correctly when there are no fixes to apply.
    """
    md_file = tmp_path / "bad.md"
    content = "# Title\n### Subtitle\n"
    md_file.write_text(content)

    changed_files, _ = run_fix_logic(md_file, dry_run=False)

    # File should remain unchanged as MD001 provides no auto-fix suggestion currently
    assert md_file.read_text() == content
    assert len(changed_files) == 0
