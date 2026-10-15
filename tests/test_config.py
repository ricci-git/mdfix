from pathlib import Path

from mdfix.config import load_config
from mdfix.rules.registry import filter_rules, get_all_rules


def test_load_config_from_pyproject(tmp_path: Path):
    """
    Verify that configuration is loaded from pyproject.toml correctly.
    """
    # Create a temporary pyproject.toml
    config_file = tmp_path / "pyproject.toml"
    config_content = """
[tool.mdfix]
disable = ["MD055", "MD009"]
"""
    config_file.write_text(config_content)
    
    # Load config pointing to this directory
    cfg = load_config(tmp_path)
    
    assert cfg.disable == ["MD055", "MD009"]
    assert cfg.enable_only is None # Default value

def test_filter_rules_applies_disable():
    """
    Verify that filter_rules respects the disabled rules list.
    """
    all_rules = get_all_rules()
    disabled_ids = {"MD055", "MD009"}
    
    filtered = filter_rules(all_rules, disabled_ids)
    
    rule_ids = {r.id for r in filtered}
    
    assert "MD001" in rule_ids
    assert "MD047" in rule_ids
    assert "MD055" not in rule_ids
    assert "MD009" not in rule_ids
