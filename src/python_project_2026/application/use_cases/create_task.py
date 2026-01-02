"""タスク作成ユースケース"""

from ...domain.entities.task import Task
from ...domain.repositories.task_repository import TaskRepository
from ...domain.value_objects.task_id import TaskId
from ...domain.value_objects.task_priority import TaskPriority


class CreateTaskUseCase:
    """タスクを作成するユースケース"""

    def __init__(self, task_repository: TaskRepository) -> None:
        """ユースケースを初期化

        Args:
            task_repository: タスクリポジトリ
        """
        self._task_repository = task_repository

    async def execute(self, title: str, description: str, priority: TaskPriority) -> TaskId:
        """タスクを作成する

        Args:
            title: タスクタイトル
            description: タスク説明
            priority: 優先度

        Returns:
            TaskId: 作成されたタスクのID

        Raises:
            ValueError: 無効な入力の場合
        """
        # 新しいTaskIdを生成
        task_id = TaskId.generate()

        # Taskエンティティを作成
        task = Task.create(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
        )

        # リポジトリに保存
        await self._task_repository.save(task)

        return task_id
