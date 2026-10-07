import re
from pathlib import Path


def test_pyproject_toml_matches_module_version():
    """
    Verify that the version in pyproject.toml matches mdfix/__init__.py or version.py.
    Specifically looks for __version__ = "x.y.z" to handle standard Python packaging conventions.
    """
    project_root = Path(__file__).parent.parent
    
    # 1. Read version from mdfix/version.py
    # Note: Based on your cat output, the variable is __version__
    version_file_path = project_root / "mdfix" / "version.py"
    assert version_file_path.exists(), f"Version file not found at {version_file_path}"
    
    source_code = version_file_path.read_text(encoding="utf-8")
    
    # Regex to find: __version__ = "0.8.3"
    # It allows for optional whitespace around equals sign
    match_ver = re.search(r'^\s*__version__\s*=\s*"([^"]+)"', source_code, re.MULTILINE)
    
    assert match_ver is not None, (
        f"Could not find '__version__' assignment in {version_file_path}. "
        f"Content preview:\n{source_code[:200]}"
    )
    module_version = match_ver.group(1)
    
    # 2. Read version from pyproject.toml
    pyproject_path = project_root / "pyproject.toml"
    assert pyproject_path.exists(), f"pyproject.toml not found at {pyproject_path}"
    
    content_toml = pyproject_path.read_text(encoding="utf-8")
    
    # Regex to find: version = "0.8.3" inside [project] section
    # We assume it's unique enough in the file structure we have now.
    match_toml = re.search(r'^\s*version\s*=\s*"([^"]+)"', content_toml, re.MULTILINE)
    
    assert match_toml is not None, (
        f"Could not find 'version' field in pyproject.toml. "
        f"Content preview:\n{content_toml[:200]}"
    )
    toml_version = match_toml.group(1)
    
    # 3. Compare
    assert toml_version == module_version, (
        f"Version mismatch! pyproject.toml has '{toml_version}', "
        f"but mdfix/version.py has '{module_version}'"
    )
