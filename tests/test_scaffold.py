"""Tests for the plugin scaffold module."""

import sys
from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from openclaw_cli.scaffold import create_plugin_scaffold


class TestPluginScaffold:
    """Test suite for plugin scaffolding functionality."""

    def test_create_plugin_creates_directory(self, tmp_path):
        """Test that create_plugin_scaffold creates the plugin directory."""
        plugin_dir = create_plugin_scaffold("test-plugin", tmp_path)
        assert plugin_dir.exists()
        assert plugin_dir.name == "test-plugin"

    def test_create_plugin_directory_structure(self, tmp_path):
        """Test that all required directories are created."""
        plugin_dir = create_plugin_scaffold("test-plugin", tmp_path)
        assert (plugin_dir / "src").exists()
        assert (plugin_dir / "src" / "test_plugin").exists()
        assert (plugin_dir / "tests").exists()

    def test_create_plugin_required_files(self, tmp_path):
        """Test that all required files are created."""
        plugin_dir = create_plugin_scaffold("test-plugin", tmp_path)
        assert (plugin_dir / "pyproject.toml").exists()
        assert (plugin_dir / "README.md").exists()
        assert (plugin_dir / "LICENSE").exists()

    def test_create_plugin_source_files(self, tmp_path):
        """Test that source files are created with correct content."""
        plugin_dir = create_plugin_scaffold("test-plugin", tmp_path)
        src_dir = plugin_dir / "src" / "test_plugin"

        # Check __init__.py
        init_file = src_dir / "__init__.py"
        assert init_file.exists()
        content = init_file.read_text()
        assert "TestPlugin" in content
        assert "__version__" in content

        # Check plugin.py
        plugin_file = src_dir / "plugin.py"
        assert plugin_file.exists()
        content = plugin_file.read_text()
        assert "class TestPlugin" in content
        assert "def execute" in content
        assert "def validate_config" in content

        # Check config.py
        config_file = src_dir / "config.py"
        assert config_file.exists()
        content = config_file.read_text()
        assert "class PluginConfig" in content

    def test_create_plugin_test_files(self, tmp_path):
        """Test that test files are created."""
        plugin_dir = create_plugin_scaffold("test-plugin", tmp_path)
        test_file = plugin_dir / "tests" / "test_plugin.py"
        assert test_file.exists()
        content = test_file.read_text()
        assert "class TestTestPlugin" in content
        assert "def test_initialization" in content
        assert "def test_execute" in content

    def test_create_plugin_pyproject_toml_valid(self, tmp_path):
        """Test that pyproject.toml is valid."""
        plugin_dir = create_plugin_scaffold("test-plugin", tmp_path)
        pyproject_file = plugin_dir / "pyproject.toml"
        assert pyproject_file.exists()

        with open(pyproject_file, "rb") as f:
            config = tomllib.load(f)

        assert "project" in config
        assert config["project"]["name"] == "test-plugin"
        assert config["project"]["version"] == "0.1.0"

    def test_create_plugin_readme_content(self, tmp_path):
        """Test that README.md has expected content."""
        plugin_dir = create_plugin_scaffold("my-awesome-plugin", tmp_path)
        readme = plugin_dir / "README.md"
        assert readme.exists()
        content = readme.read_text()
        assert "my-awesome-plugin" in content
        assert "OpenClaw" in content

    def test_create_plugin_with_underscores(self, tmp_path):
        """Test plugin name conversion from hyphens to underscores."""
        plugin_dir = create_plugin_scaffold("my-plugin-name", tmp_path)
        # Package should use underscores
        assert (plugin_dir / "src" / "my_plugin_name").exists()
        assert (plugin_dir / "src" / "my_plugin_name" / "__init__.py").exists()

    def test_create_plugin_license_copyright(self, tmp_path):
        """Test that LICENSE contains proper copyright."""
        plugin_dir = create_plugin_scaffold("test-plugin", tmp_path)
        license_file = plugin_dir / "LICENSE"
        assert license_file.exists()
        content = license_file.read_text()
        assert "MIT License" in content
        assert "OpenClaw" in content

    def test_invalid_plugin_name_raises_error(self, tmp_path):
        """Test that invalid plugin names raise ValueError."""
        with pytest.raises(ValueError):
            create_plugin_scaffold("!invalid@name", tmp_path)

    def test_existing_directory_raises_error(self, tmp_path):
        """Test that creating in existing directory raises error."""
        # First creation succeeds
        create_plugin_scaffold("test-plugin", tmp_path)
        # Second creation should fail
        with pytest.raises(ValueError):
            create_plugin_scaffold("test-plugin", tmp_path)

    def test_plugin_package_is_importable(self, tmp_path):
        """Test that the generated plugin can be imported."""
        plugin_dir = create_plugin_scaffold("test-plugin", tmp_path)
        src_dir = plugin_dir / "src"

        # Add to path and import
        sys.path.insert(0, str(src_dir))
        try:
            import test_plugin
            from test_plugin.plugin import TestPlugin

            # Test that the plugin works
            plugin = TestPlugin()
            assert plugin.name == "test_plugin"
            assert plugin.version == "0.1.0"

            result = plugin.execute()
            assert result["status"] == "success"
        finally:
            sys.path.remove(str(src_dir))
            if "test_plugin" in sys.modules:
                del sys.modules["test_plugin"]
            if "test_plugin.plugin" in sys.modules:
                del sys.modules["test_plugin.plugin"]
            if "test_plugin.config" in sys.modules:
                del sys.modules["test_plugin.config"]

    def test_generated_tests_are_valid_pytest(self, tmp_path):
        """Test that generated test file is valid pytest."""
        plugin_dir = create_plugin_scaffold("mytest-plugin", tmp_path)
        test_file = plugin_dir / "tests" / "test_plugin.py"

        # Verify pytest can parse it
        import ast

        content = test_file.read_text()
        try:
            ast.parse(content)
        except SyntaxError as e:
            pytest.fail(f"Generated test file has syntax error: {e}")
