"""タスクリポジトリインターフェース"""

from abc import ABC, abstractmethod

from ..entities.task import Task
from ..value_objects.task_id import TaskId
from ..value_objects.task_priority import TaskPriority
from ..value_objects.task_status import TaskStatus


class TaskRepository(ABC):
    """タスクリポジトリのインターフェース"""

    @abstractmethod
    async def save(self, task: Task) -> None:
        """タスクを保存

        Args:
            task: 保存するタスク
        """

    @abstractmethod
    async def find_by_id(self, task_id: TaskId) -> Task | None:
        """IDでタスクを検索

        Args:
            task_id: 検索するタスクID

        Returns:
            Task: 見つかったタスク、見つからない場合はNone
        """

    @abstractmethod
    async def find_all(self) -> list[Task]:
        """すべてのタスクを取得

        Returns:
            list[Task]: すべてのタスク一覧
        """

    @abstractmethod
    async def find_by_status(self, status: TaskStatus) -> list[Task]:
        """ステータスでタスクを検索

        Args:
            status: 検索するステータス

        Returns:
            list[Task]: 該当するタスク一覧
        """

    @abstractmethod
    async def find_by_priority(self, priority: TaskPriority) -> list[Task]:
        """優先度でタスクを検索

        Args:
            priority: 検索する優先度

        Returns:
            list[Task]: 該当するタスク一覧
        """

    @abstractmethod
    async def delete(self, task_id: TaskId) -> bool:
        """タスクを削除

        Args:
            task_id: 削除するタスクID

        Returns:
            bool: 削除に成功した場合True、該当するタスクが存在しない場合False
        """
