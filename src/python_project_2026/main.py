"""メインアプリケーション"""

import typer
from rich.console import Console
from rich.panel import Panel

from . import __version__

app = typer.Typer(
    name="python-project-2026",
    help="2026年の最新Python開発テンプレート",
    add_completion=False,
)
console = Console()


@app.command()
def hello(name: str = typer.Option("World", help="挨拶する相手の名前")) -> None:
    """挨拶を表示します"""
    console.print(
        Panel(
            f"[bold green]こんにちは、{name}![/bold green]",
            title="Python Project 2026",
            border_style="blue",
        )
    )


@app.command()
def version() -> None:
    """バージョン情報を表示します"""
    console.print(f"Python Project 2026 version: [bold]{__version__}[/bold]")


if __name__ == "__main__":
    app()
