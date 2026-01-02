"""タスク管理CLI"""

import typer
from rich.console import Console
from rich.table import Table

from ...application.use_cases.create_task import CreateTaskUseCase
from ...domain.value_objects.task_priority import TaskPriority
from ...domain.value_objects.task_status import TaskStatus
from ...infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository

# DI Container (簡易実装)
_repository = InMemoryTaskRepository()
_create_task_use_case = CreateTaskUseCase(_repository)

console = Console()

task_app = typer.Typer(
    name="task",
    help="タスク管理機能",
    no_args_is_help=True,
)


@task_app.command("create")
async def create_task(
    title: str = typer.Argument(..., help="タスクのタイトル"),
    description: str = typer.Option("", "--desc", "-d", help="タスクの説明"),
    priority: str = typer.Option("MEDIUM", "--priority", "-p", help="優先度 (LOW/MEDIUM/HIGH)"),
) -> None:
    """新しいタスクを作成します"""
    try:
        task_priority = TaskPriority.from_string(priority)
        task_id = await _create_task_use_case.execute(title, description, task_priority)

        console.print("✅ タスクを作成しました", style="bold green")
        console.print(f"   ID: {task_id}")
        console.print(f"   タイトル: {title}")
        console.print(f"   優先度: {priority}")

    except ValueError as e:
        console.print(f"❌ エラー: {e}", style="bold red")
        raise typer.Exit(1)


@task_app.command("list")
async def list_tasks(
    status: str | None = typer.Option(None, "--status", "-s", help="ステータスで絞り込み (TODO/IN_PROGRESS/DONE)"),
    priority: str | None = typer.Option(None, "--priority", "-p", help="優先度で絞り込み (LOW/MEDIUM/HIGH)"),
) -> None:
    """タスク一覧を表示します"""
    try:
        tasks = await _repository.find_all()

        # フィルタリング
        if status:
            task_status = TaskStatus.from_string(status)
            tasks = [t for t in tasks if t.status == task_status]

        if priority:
            task_priority = TaskPriority.from_string(priority)
            tasks = [t for t in tasks if t.priority == task_priority]

        if not tasks:
            console.print("📝 タスクが見つかりません", style="yellow")
            return

        # テーブル表示
        table = Table(
            title=f"📋 タスク一覧 ({len(tasks)}件)",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("ID", style="dim", width=12)
        table.add_column("タイトル", min_width=20)
        table.add_column("ステータス", justify="center")
        table.add_column("優先度", justify="center")
        table.add_column("作成日", justify="center")

        for task in tasks:
            status_style = {
                TaskStatus.TODO: "yellow",
                TaskStatus.IN_PROGRESS: "blue",
                TaskStatus.DONE: "green",
            }.get(task.status, "white")

            priority_style = {
                TaskPriority.LOW: "green",
                TaskPriority.MEDIUM: "yellow",
                TaskPriority.HIGH: "red",
            }.get(task.priority, "white")

            table.add_row(
                str(task.id)[:8] + "...",
                task.title,
                f"[{status_style}]{task.status}[/{status_style}]",
                f"[{priority_style}]{task.priority}[/{priority_style}]",
                task.created_at.strftime("%Y-%m-%d"),
            )

        console.print(table)

    except ValueError as e:
        console.print(f"❌ エラー: {e}", style="bold red")
        raise typer.Exit(1)


@task_app.command("show")
async def show_task(task_id: str = typer.Argument(..., help="表示するタスクのID")) -> None:
    """指定したタスクの詳細を表示します"""
    try:
        from ...domain.value_objects.task_id import TaskId

        task = await _repository.find_by_id(TaskId(task_id))

        if not task:
            console.print(f"❌ タスクが見つかりません: {task_id}", style="bold red")
            raise typer.Exit(1)

        console.print("\n📋 [bold]タスク詳細[/bold]")
        console.print(f"   ID: {task.id}")
        console.print(f"   タイトル: {task.title}")
        console.print(f"   説明: {task.description or '(なし)'}")
        console.print(f"   ステータス: {task.status}")
        console.print(f"   優先度: {task.priority}")
        console.print(f"   作成日: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        console.print(f"   更新日: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

    except ValueError:
        console.print(f"❌ 無効なタスクID: {task_id}", style="bold red")
        raise typer.Exit(1)
