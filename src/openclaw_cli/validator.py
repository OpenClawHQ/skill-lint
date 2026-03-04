"""Plugin validation logic for the validate command."""

import sys
from pathlib import Path
from typing import Tuple

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from rich.console import Console
from rich.table import Table

console = Console()


REQUIRED_FILES = [
    "pyproject.toml",
]

REQUIRED_DIRS = [
    "src",
    "tests",
]


def validate_plugin(plugin_path: str = ".") -> bool:
    """
    Validate a plugin structure and configuration.

    Args:
        plugin_path: Path to the plugin directory (defaults to current directory)

    Returns:
        bool: True if validation passes, False otherwise
    """
    path = Path(plugin_path).resolve()

    if not path.is_dir():
        console.print(f"[red]✗[/red] Path '{plugin_path}' is not a directory.")
        return False

    console.print(f"[cyan]Validating plugin at:[/cyan] {path}\n")

    results = []

    # Check required files
    console.print("[blue]Checking files...[/blue]")
    for filename in REQUIRED_FILES:
        file_path = path / filename
        exists = file_path.exists()
        status = "[green]✓[/green]" if exists else "[red]✗[/red]"
        console.print(f"  {status} {filename}")
        results.append(exists)

    # Check required directories
    console.print("\n[blue]Checking directories...[/blue]")
    for dirname in REQUIRED_DIRS:
        dir_path = path / dirname
        exists = dir_path.is_dir()
        status = "[green]✓[/green]" if exists else "[red]✗[/red]"
        console.print(f"  {status} {dirname}/")
        results.append(exists)

    # Validate pyproject.toml
    console.print("\n[blue]Validating configuration...[/blue]")
    pyproject_path = path / "pyproject.toml"
    if pyproject_path.exists():
        try:
            with open(pyproject_path, "rb") as f:
                config = tomllib.load(f)
            if "project" in config:
                name = config.get("project", {}).get("name")
                version = config.get("project", {}).get("version")
                console.print(f"  [green]✓[/green] pyproject.toml is valid")
                console.print(f"    Project: {name} (v{version})")
                results.append(True)
            else:
                console.print(f"  [red]✗[/red] pyproject.toml missing [project] section")
                results.append(False)
        except Exception as e:
            console.print(f"  [red]✗[/red] pyproject.toml parsing failed: {e}")
            results.append(False)
    else:
        results.append(False)

    # Check source structure
    console.print("\n[blue]Checking source structure...[/blue]")
    src_dir = path / "src"
    if src_dir.exists():
        src_packages = [
            d
            for d in src_dir.iterdir()
            if d.is_dir() and not d.name.startswith("_")
        ]
        if src_packages:
            for pkg in src_packages:
                init_file = pkg / "__init__.py"
                if init_file.exists():
                    console.print(f"  [green]✓[/green] {pkg.name}/__init__.py found")
                    results.append(True)
                else:
                    console.print(f"  [yellow]![/yellow] {pkg.name}/__init__.py missing")
                    results.append(False)
        else:
            console.print(f"  [yellow]![/yellow] No packages found in src/")

    # Check test structure
    console.print("\n[blue]Checking test structure...[/blue]")
    tests_dir = path / "tests"
    if tests_dir.exists():
        test_files = list(tests_dir.glob("test_*.py"))
        if test_files:
            console.print(f"  [green]✓[/green] Found {len(test_files)} test file(s)")
            results.append(True)
        else:
            console.print(f"  [yellow]![/yellow] No test files found (test_*.py)")
            results.append(False)

    # Try importing the plugin
    console.print("\n[blue]Checking imports...[/blue]")
    import_ok = _check_imports(path)
    if import_ok:
        console.print(f"  [green]✓[/green] Plugin imports successful")
        results.append(True)
    else:
        console.print(f"  [yellow]![/yellow] Plugin imports failed (check your code)")
        results.append(False)

    # Summary
    console.print()
    passed = sum(results)
    total = len(results)
    if all(results):
        console.print(f"[green]✓ Validation passed! ({passed}/{total} checks)[/green]\n")
        return True
    else:
        console.print(
            f"[yellow]⚠ Validation found issues ({passed}/{total} checks)[/yellow]\n"
        )
        return False


def _check_imports(plugin_path: Path) -> bool:
    """Try to import the plugin package."""
    try:
        src_dir = plugin_path / "src"
        if not src_dir.exists():
            return False

        # Find first package
        packages = [d for d in src_dir.iterdir() if d.is_dir() and (d / "__init__.py").exists()]
        if not packages:
            return False

        # Try to add src to path and import
        sys.path.insert(0, str(src_dir))
        try:
            __import__(packages[0].name)
            return True
        except ImportError:
            return False
        finally:
            sys.path.pop(0)

    except Exception:
        return False
