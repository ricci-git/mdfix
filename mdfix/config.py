import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MdfixConfig:
    disable: list[str] = field(default_factory=list)
    enable_only: list[str] | None = None

def load_config(search_dir: Path) -> MdfixConfig:
    """
    Loads configuration from pyproject.toml searching upwards from search_dir.
    """
    current = search_dir.resolve()
    
    while True:
        candidate = current / "pyproject.toml"
        if candidate.exists():
            try:
                with open(candidate, "rb") as f:
                    data = tomllib.load(f)
                
                tool_section = data.get("tool", {})
                mdfix_section = tool_section.get("mdfix", {})
                
                return MdfixConfig(
                    disable=mdfix_section.get("disable", []),
                    enable_only=mdfix_section.get("enable_only"),
                )
            except (OSError, tomllib.TOMLDecodeError):
                # If file cannot be read or is invalid TOML, ignore and continue searching upwards
                break
        
        # Move up one directory
        parent = current.parent
        if parent == current:
            break # Reached root
        current = parent
        
    return MdfixConfig()
