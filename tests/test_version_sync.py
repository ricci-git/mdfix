import re
from pathlib import Path
from mdfix.version import __version__

def test_pyproject_toml_matches_module_version():
    """
    Verify that the version in pyproject.toml matches mdfix.version.__version__.
    This ensures package metadata is consistent with CLI output.
    """
    # Read pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")
    
    # Extract version using regex (simple approach for static check)
    # Looking for: version = "x.y.z" OR dynamic version config
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    
    if match:
        toml_version = match.group(1)
        assert toml_version == __version__, (
            f"Version mismatch! pyproject.toml has '{toml_version}', "
            f"but mdfix/version.py has '{__version__}'"
        )
    else:
        # If no static version found, assume it's dynamic and check configuration
        # For this task, we will enforce STATIC synchronization first as it's simpler 
        # and less prone to build-system quirks in early stages.
        raise AssertionError("No static 'version' field found in pyproject.toml. "
                             "Please ensure version is explicitly set or dynamic config is verified.")
