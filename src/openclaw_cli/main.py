"""OpenClaw CLI main entry point with Typer commands."""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from openclaw_cli.scaffold import create_plugin_scaffold
from openclaw_cli.validator import validate_plugin

app = typer.Typer(
    name="openclaw",
    help="The developer toolkit for building OpenClaw plugins.",
    no_args_is_help=True,
)

console = Console()


@app.command()
def init(
    name: str = typer.Argument(..., help="Name of the plugin to create"),
    path: Optional[str] = typer.Option(
        None, "--path", "-p", help="Parent directory for the plugin (defaults to current)"
    ),
) -> None:
    """
    Scaffold a new OpenClaw plugin.

    Creates a complete plugin project structure with boilerplate code,
    tests, and configuration.

    Example:
        openclaw init my-awesome-plugin
    """
    try:
        plugin_dir = create_plugin_scaffold(name, Path(path) if path else None)
        typer.echo("")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def validate(
    path: str = typer.Argument(
        ".", help="Path to the plugin directory (defaults to current directory)"
    ),
) -> None:
    """
    Validate an OpenClaw plugin structure and configuration.

    Checks:
    - Required files exist (pyproject.toml, src/, tests/)
    - Plugin configuration is valid
    - Package structure is correct
    - Imports can be resolved

    Example:
        openclaw validate
        openclaw validate ./my-plugin
    """
    try:
        if not validate_plugin(path):
            raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Validation error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def test(
    path: str = typer.Argument(
        ".",
        help="Path to the plugin directory (defaults to current directory)",
    ),
    args: str = typer.Option(
        "",
        "--args",
        "-a",
        help="Additional arguments to pass to pytest (e.g., '-v', '--cov')",
    ),
) -> None:
    """
    Run plugin tests with pytest.

    Runs pytest with OpenClaw-specific settings and reporting.

    Example:
        openclaw test
        openclaw test ./my-plugin
        openclaw test --args "-v --cov"
    """
    plugin_path = Path(path).resolve()

    if not plugin_path.is_dir():
        console.print(f"[red]Error:[/red] Path '{path}' is not a directory.")
        raise typer.Exit(1)

    tests_dir = plugin_path / "tests"
    if not tests_dir.exists():
        console.print(f"[red]Error:[/red] No tests directory found at '{path}/tests'")
        raise typer.Exit(1)

    # Build pytest command
    cmd = ["python", "-m", "pytest", str(tests_dir)]
    if args:
        cmd.extend(args.split())

    console.print(f"[cyan]Running tests in:[/cyan] {plugin_path}")
    console.print(f"[cyan]Command:[/cyan] {' '.join(cmd)}\n")

    try:
        result = subprocess.run(cmd, cwd=str(plugin_path))
        raise typer.Exit(result.returncode)
    except FileNotFoundError:
        console.print(
            "[red]Error:[/red] pytest not found. Install it with: pip install pytest"
        )
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error running tests:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def dev(
    path: str = typer.Argument(
        ".",
        help="Path to the plugin directory (defaults to current directory)",
    ),
) -> None:
    """
    Start local development mode with hot-reload.

    Watches source files and automatically reloads the plugin
    in development mode for rapid iteration.

    Example:
        openclaw dev
        openclaw dev ./my-plugin
    """
    plugin_path = Path(path).resolve()

    if not plugin_path.is_dir():
        console.print(f"[red]Error:[/red] Path '{path}' is not a directory.")
        raise typer.Exit(1)

    src_dir = plugin_path / "src"
    if not src_dir.exists():
        console.print(f"[red]Error:[/red] No src directory found at '{path}/src'")
        raise typer.Exit(1)

    console.print(f"[cyan]Starting development mode:[/cyan] {plugin_path}")
    console.print(f"[cyan]Watching:[/cyan] {src_dir}\n")

    # Check if watchfiles is installed
    try:
        import watchfiles
    except ImportError:
        console.print(
            "[yellow]Note:[/yellow] watchfiles not found. Install for auto-reload:"
        )
        console.print("  pip install watchfiles\n")

    # Find the plugin package
    packages = [d for d in src_dir.iterdir() if d.is_dir() and (d / "__init__.py").exists()]

    if not packages:
        console.print("[red]Error:[/red] No packages found in src/")
        raise typer.Exit(1)

    package_name = packages[0].name

    try:
        # Try using watchfiles if available
        try:
            import watchfiles

            console.print(f"[green]✓[/green] Watching for changes...\n")
            console.print("[cyan]Tips:[/cyan]")
            console.print("  - Edit files in src/ to see changes")
            console.print("  - Run 'openclaw test' to verify")
            console.print("  - Press Ctrl+C to exit\n")

            def on_change(changes):
                console.print(
                    f"[green]→[/green] Files changed, reloading plugin '{package_name}'..."
                )
                # Dynamically reload the module
                try:
                    import importlib

                    if package_name in sys.modules:
                        importlib.reload(sys.modules[package_name])
                    console.print("[green]✓ Plugin reloaded[/green]\n")
                except Exception as e:
                    console.print(f"[red]Reload failed:[/red] {e}\n")

            sys.path.insert(0, str(src_dir))
            watchfiles.run_process(
                str(src_dir),
                callback=on_change,
                watch_filter=watchfiles.DefaultDirFilter(),
            )

        except ImportError:
            # Fallback: simple loop with basic file watching
            import time

            console.print(f"[green]✓[/green] Dev mode running (without auto-reload)\n")
            console.print("[cyan]Tips:[/cyan]")
            console.print("  - Edit files in src/ manually")
            console.print("  - Run 'openclaw test' to verify")
            console.print("  - Press Ctrl+C to exit\n")

            last_mtime = {}
            while True:
                for py_file in src_dir.rglob("*.py"):
                    mtime = py_file.stat().st_mtime
                    if py_file in last_mtime and last_mtime[py_file] != mtime:
                        console.print(
                            f"[green]→[/green] {py_file.relative_to(src_dir)} changed"
                        )
                    last_mtime[py_file] = mtime
                time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Development mode stopped.[/yellow]")
        raise typer.Exit(0)
    except Exception as e:
        console.print(f"[red]Error in dev mode:[/red] {e}")
        raise typer.Exit(1)


def version_callback(value: bool) -> None:
    """Display version and exit."""
    if value:
        from openclaw_cli import __version__

        console.print(f"openclaw-cli version {__version__}")
        raise typer.Exit(0)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        is_eager=True,
        callback=version_callback,
    ),
) -> None:
    """OpenClaw CLI — developer toolkit for building OpenClaw plugins."""
    pass


if __name__ == "__main__":
    app()
