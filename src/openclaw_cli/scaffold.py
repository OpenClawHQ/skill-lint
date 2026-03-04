"""Plugin scaffolding logic for the init command."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console

console = Console()


def create_plugin_scaffold(name: str, path: Optional[Path] = None) -> Path:
    """
    Create a new plugin scaffold with full project structure.

    Args:
        name: Plugin name (used for package naming)
        path: Parent directory path (defaults to current directory)

    Returns:
        Path to the created plugin directory

    Raises:
        ValueError: If plugin name is invalid or directory already exists
    """
    if not name or not name.replace("-", "").replace("_", "").isalnum():
        raise ValueError(
            f"Invalid plugin name '{name}'. Use alphanumeric characters, hyphens, or underscores."
        )

    parent_dir = Path(path or ".")
    plugin_dir = parent_dir / name
    package_name = name.replace("-", "_")

    if plugin_dir.exists():
        raise ValueError(f"Directory '{plugin_dir}' already exists.")

    try:
        # Create directory structure
        console.print(f"[blue]→[/blue] Creating plugin '{name}'...", end=" ")
        (plugin_dir / "src" / package_name).mkdir(parents=True)
        (plugin_dir / "tests").mkdir(parents=True)
        console.print("[green]✓[/green]")

        # Create Python files
        console.print(f"[blue]→[/blue] Generating files...", end=" ")

        _create_init_py(plugin_dir, package_name)
        _create_plugin_py(plugin_dir, package_name)
        _create_config_py(plugin_dir, package_name)
        _create_test_py(plugin_dir, package_name)
        _create_pyproject_toml(plugin_dir, name)
        _create_readme_md(plugin_dir, name)
        _create_license(plugin_dir)

        console.print("[green]✓[/green]")

        console.print(f"[green]✓ Plugin '{name}' created successfully![/green]")
        console.print(f"\n[cyan]Next steps:[/cyan]")
        console.print(f"  cd {name}")
        console.print(f"  openclaw validate    # Check your plugin")
        console.print(f"  openclaw test        # Run tests")
        console.print(f"  openclaw dev         # Start development mode\n")

        return plugin_dir

    except Exception as e:
        # Clean up on failure
        if plugin_dir.exists():
            shutil.rmtree(plugin_dir)
        raise RuntimeError(f"Failed to create plugin scaffold: {e}") from e


def _create_init_py(plugin_dir: Path, package_name: str) -> None:
    """Create __init__.py for the plugin package."""
    content = f'''"""Plugin: {package_name}"""

from .plugin import {_to_class_name(package_name)}

__version__ = "0.1.0"
__all__ = ["{_to_class_name(package_name)}"]
'''
    (plugin_dir / "src" / package_name / "__init__.py").write_text(content)


def _create_plugin_py(plugin_dir: Path, package_name: str) -> None:
    """Create the main plugin.py file."""
    class_name = _to_class_name(package_name)
    content = f'''"""Main plugin implementation."""


class {class_name}:
    """
    {class_name} plugin for OpenClaw.

    A plugin that builds hands for AI that moves first.
    """

    def __init__(self):
        """Initialize the plugin."""
        self.name = "{package_name}"
        self.version = "0.1.0"

    def execute(self, **kwargs) -> dict:
        """
        Execute the plugin with the given inputs.

        Args:
            **kwargs: Plugin-specific arguments

        Returns:
            dict: Plugin execution result
        """
        return {{"status": "success", "message": "Plugin executed"}}

    def validate_config(self, config: dict) -> bool:
        """
        Validate plugin configuration.

        Args:
            config: Configuration dictionary

        Returns:
            bool: True if config is valid
        """
        return True
'''
    (plugin_dir / "src" / package_name / "plugin.py").write_text(content)


def _create_config_py(plugin_dir: Path, package_name: str) -> None:
    """Create the config.py file."""
    content = '''"""Plugin configuration schema."""

from typing import Any, Dict, Optional


class PluginConfig:
    """Configuration schema for the plugin."""

    def __init__(self, name: str, version: str = "0.1.0", **kwargs):
        """
        Initialize plugin configuration.

        Args:
            name: Plugin name
            version: Plugin version
            **kwargs: Additional configuration options
        """
        self.name = name
        self.version = version
        self.extras = kwargs

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            **self.extras,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginConfig":
        """Create config from dictionary."""
        name = data.pop("name")
        version = data.pop("version", "0.1.0")
        return cls(name=name, version=version, **data)
'''
    (plugin_dir / "src" / package_name / "config.py").write_text(content)


def _create_test_py(plugin_dir: Path, package_name: str) -> None:
    """Create test_plugin.py."""
    class_name = _to_class_name(package_name)
    content = f'''"""Tests for {package_name} plugin."""

import pytest

from {package_name}.plugin import {class_name}


class Test{class_name}:
    """Test suite for {class_name}."""

    def test_initialization(self):
        """Test plugin initialization."""
        plugin = {class_name}()
        assert plugin.name == "{package_name}"
        assert plugin.version == "0.1.0"

    def test_execute(self):
        """Test plugin execution."""
        plugin = {class_name}()
        result = plugin.execute()
        assert result["status"] == "success"
        assert "message" in result

    def test_validate_config(self):
        """Test config validation."""
        plugin = {class_name}()
        assert plugin.validate_config({{}})
        assert plugin.validate_config({{"key": "value"}})
'''
    (plugin_dir / "tests" / "test_plugin.py").write_text(content)


def _create_pyproject_toml(plugin_dir: Path, name: str) -> None:
    """Create pyproject.toml for the plugin."""
    package_name = name.replace("-", "_")
    content = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
description = "An OpenClaw plugin: {name}"
readme = "README.md"
license = {{ text = "MIT" }}
authors = [
    {{ name = "Your Name", email = "your.email@example.com" }}
]
requires-python = ">=3.10"
dependencies = []

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
'''
    (plugin_dir / "pyproject.toml").write_text(content)


def _create_readme_md(plugin_dir: Path, name: str) -> None:
    """Create README.md for the plugin."""
    content = f"""# {name}

An OpenClaw plugin.

## Installation

```bash
pip install {name}
```

## Usage

```python
from {name.replace("-", "_")} import {_to_class_name(name.replace("-", "_"))}

plugin = {_to_class_name(name.replace("-", "_"))}()
result = plugin.execute()
```

## Development

Run tests:
```bash
openclaw test
```

Validate:
```bash
openclaw validate
```

Start development mode:
```bash
openclaw dev
```

## License

MIT License (see LICENSE file)

## Contributing

Built by the OpenClaw community. We move first.
"""
    (plugin_dir / "README.md").write_text(content)


def _create_license(plugin_dir: Path) -> None:
    """Create MIT LICENSE file."""
    year = datetime.now().year
    content = f"""MIT License

Copyright (c) {year} OpenClaw Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    (plugin_dir / "LICENSE").write_text(content)


def _to_class_name(snake_case: str) -> str:
    """Convert snake_case to ClassName."""
    return "".join(word.capitalize() for word in snake_case.split("_"))
