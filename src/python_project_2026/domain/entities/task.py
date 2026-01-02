"""タスク Entity"""

from datetime import UTC, datetime

from ..value_objects.task_id import TaskId
from ..value_objects.task_priority import TaskPriority
from ..value_objects.task_status import TaskStatus


class Task:
    """タスクを表すエンティティ"""

    def __init__(
        self,
        task_id: TaskId,
        title: str,
        description: str,
        priority: TaskPriority,
        status: TaskStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        """タスクを初期化

        Args:
            task_id: タスクID
            title: タスクタイトル
            description: タスク説明
            priority: 優先度
            status: ステータス
            created_at: 作成日時
            updated_at: 更新日時
        """
        self._id = task_id
        self._title = title
        self._description = description
        self._priority = priority
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(
        cls,
        task_id: TaskId,
        title: str | None,
        description: str,
        priority: TaskPriority,
    ) -> "Task":
        """新しいタスクを作成

        Args:
            task_id: タスクID
            title: タスクタイトル
            description: タスク説明
            priority: 優先度

        Returns:
            Task: 作成されたタスク

        Raises:
            ValueError: タイトルが空の場合
        """
        if not title or title.strip() == "":
            raise ValueError("Title cannot be empty")

        now = datetime.now(UTC)
        return cls(
            task_id=task_id,
            title=title.strip(),
            description=description,
            priority=priority,
            status=TaskStatus.TODO,
            created_at=now,
            updated_at=now,
        )

    @property
    def id(self) -> TaskId:
        """タスクID"""
        return self._id

    @property
    def title(self) -> str:
        """タスクタイトル"""
        return self._title

    @property
    def description(self) -> str:
        """タスク説明"""
        return self._description

    @property
    def priority(self) -> TaskPriority:
        """優先度"""
        return self._priority

    @property
    def status(self) -> TaskStatus:
        """ステータス"""
        return self._status

    @property
    def created_at(self) -> datetime:
        """作成日時"""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """更新日時"""
        return self._updated_at

    def update_status(self, new_status: TaskStatus) -> None:
        """ステータスを更新

        Args:
            new_status: 新しいステータス

        Raises:
            ValueError: 無効な遷移の場合
        """
        if not self._status.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {self._status} to {new_status}")

        self._status = new_status
        self._updated_at = datetime.now(UTC)

    def update_title(self, new_title: str) -> None:
        """タイトルを更新

        Args:
            new_title: 新しいタイトル

        Raises:
            ValueError: タイトルが空の場合
        """
        if not new_title or new_title.strip() == "":
            raise ValueError("Title cannot be empty")

        self._title = new_title.strip()
        self._updated_at = datetime.now(UTC)

    def update_description(self, new_description: str) -> None:
        """説明を更新

        Args:
            new_description: 新しい説明
        """
        self._description = new_description
        self._updated_at = datetime.now(UTC)

    def update_priority(self, new_priority: TaskPriority) -> None:
        """優先度を更新

        Args:
            new_priority: 新しい優先度
        """
        self._priority = new_priority
        self._updated_at = datetime.now(UTC)

    def __eq__(self, other: object) -> bool:
        """等価比較（IDベース）"""
        if not isinstance(other, Task):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """ハッシュ値計算（IDベース）"""
        return hash(self._id)

    def __str__(self) -> str:
        """文字列表現"""
        return f"Task(id={self._id}, title='{self._title}', status={self._status}, priority={self._priority})"
