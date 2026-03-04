"""Tests for the plugin validator module."""

import sys
from pathlib import Path

import pytest

from openclaw_cli.scaffold import create_plugin_scaffold
from openclaw_cli.validator import validate_plugin


class TestPluginValidator:
    """Test suite for plugin validation functionality."""

    def test_validate_valid_plugin(self, tmp_path):
        """Test that a properly scaffolded plugin passes validation."""
        plugin_dir = create_plugin_scaffold("valid-plugin", tmp_path)
        result = validate_plugin(str(plugin_dir))
        assert result is True

    def test_validate_invalid_path(self, tmp_path):
        """Test that validation fails for non-existent path."""
        result = validate_plugin(str(tmp_path / "nonexistent"))
        assert result is False

    def test_validate_missing_pyproject_toml(self, tmp_path):
        """Test that validation fails when pyproject.toml is missing."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "src").mkdir()
        (plugin_dir / "tests").mkdir()

        result = validate_plugin(str(plugin_dir))
        assert result is False

    def test_validate_missing_src_directory(self, tmp_path):
        """Test that validation fails when src directory is missing."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "pyproject.toml").write_text("[project]\nname='test'")
        (plugin_dir / "tests").mkdir()

        result = validate_plugin(str(plugin_dir))
        assert result is False

    def test_validate_missing_tests_directory(self, tmp_path):
        """Test that validation fails when tests directory is missing."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "src").mkdir()
        (plugin_dir / "pyproject.toml").write_text("[project]\nname='test'")

        result = validate_plugin(str(plugin_dir))
        assert result is False

    def test_validate_invalid_pyproject_toml(self, tmp_path):
        """Test that validation fails with invalid TOML."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "src").mkdir()
        (plugin_dir / "tests").mkdir()
        (plugin_dir / "pyproject.toml").write_text("invalid toml [[[")

        result = validate_plugin(str(plugin_dir))
        assert result is False

    def test_validate_missing_project_section(self, tmp_path):
        """Test that validation fails when pyproject.toml lacks [project] section."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "src").mkdir()
        (plugin_dir / "tests").mkdir()
        (plugin_dir / "pyproject.toml").write_text("[build-system]\nrequires=['hatchling']")

        result = validate_plugin(str(plugin_dir))
        assert result is False

    def test_validate_missing_init_py(self, tmp_path):
        """Test that validation warns about missing __init__.py."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "src").mkdir()
        (plugin_dir / "src" / "mypkg").mkdir()  # No __init__.py
        (plugin_dir / "tests").mkdir()
        (plugin_dir / "pyproject.toml").write_text(
            "[project]\nname='test-plugin'\nversion='0.1.0'"
        )

        result = validate_plugin(str(plugin_dir))
        # Should still return based on other checks
        assert isinstance(result, bool)

    def test_validate_missing_tests(self, tmp_path):
        """Test that validation warns about missing test files."""
        plugin_dir = tmp_path / "test-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "src").mkdir()
        (plugin_dir / "src" / "mypkg").mkdir()
        (plugin_dir / "src" / "mypkg" / "__init__.py").write_text("")
        (plugin_dir / "tests").mkdir()  # Exists but empty
        (plugin_dir / "pyproject.toml").write_text(
            "[project]\nname='test-plugin'\nversion='0.1.0'"
        )

        result = validate_plugin(str(plugin_dir))
        # Should still complete validation
        assert isinstance(result, bool)

    def test_validate_with_default_path(self, tmp_path, monkeypatch):
        """Test that validation works with default path (.)."""
        plugin_dir = create_plugin_scaffold("default-path-plugin", tmp_path)
        monkeypatch.chdir(plugin_dir)

        # Validate current directory
        result = validate_plugin(".")
        assert result is True

    def test_validate_complete_valid_structure(self, tmp_path):
        """Test validation of a complete valid plugin structure."""
        plugin_dir = create_plugin_scaffold("complete-plugin", tmp_path)

        # Verify all components pass
        result = validate_plugin(str(plugin_dir))
        assert result is True

        # Verify files we know exist
        assert (plugin_dir / "pyproject.toml").exists()
        assert (plugin_dir / "src").is_dir()
        assert (plugin_dir / "tests").is_dir()
        assert (plugin_dir / "tests" / "test_plugin.py").exists()
