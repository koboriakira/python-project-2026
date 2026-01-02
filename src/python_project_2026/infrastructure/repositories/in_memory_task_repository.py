"""インメモリタスクリポジトリ実装"""

from ...domain.entities.task import Task
from ...domain.repositories.task_repository import TaskRepository
from ...domain.value_objects.task_id import TaskId
from ...domain.value_objects.task_priority import TaskPriority
from ...domain.value_objects.task_status import TaskStatus


class InMemoryTaskRepository(TaskRepository):
    """インメモリでタスクを管理するRepository実装"""

    def __init__(self) -> None:
        """リポジトリを初期化"""
        self._tasks: dict[TaskId, Task] = {}

    async def save(self, task: Task) -> None:
        """タスクを保存

        Args:
            task: 保存するタスク
        """
        self._tasks[task.id] = task

    async def find_by_id(self, task_id: TaskId) -> Task | None:
        """IDでタスクを検索

        Args:
            task_id: 検索するタスクID

        Returns:
            Task: 見つかったタスク、見つからない場合はNone
        """
        return self._tasks.get(task_id)

    async def find_all(self) -> list[Task]:
        """すべてのタスクを取得

        Returns:
            list[Task]: すべてのタスク一覧
        """
        return list(self._tasks.values())

    async def find_by_status(self, status: TaskStatus) -> list[Task]:
        """ステータスでタスクを検索

        Args:
            status: 検索するステータス

        Returns:
            list[Task]: 該当するタスク一覧
        """
        return [task for task in self._tasks.values() if task.status == status]

    async def find_by_priority(self, priority: TaskPriority) -> list[Task]:
        """優先度でタスクを検索

        Args:
            priority: 検索する優先度

        Returns:
            list[Task]: 該当するタスク一覧
        """
        return [task for task in self._tasks.values() if task.priority == priority]

    async def delete(self, task_id: TaskId) -> bool:
        """タスクを削除

        Args:
            task_id: 削除するタスクID

        Returns:
            bool: 削除に成功した場合True、該当するタスクが存在しない場合False
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
