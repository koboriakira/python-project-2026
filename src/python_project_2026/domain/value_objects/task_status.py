"""タスクステータス ValueObject"""

from enum import Enum


class TaskStatus(Enum):
    """タスクのステータスを表すValueObject"""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

    @classmethod
    def from_string(cls, status_str: str) -> "TaskStatus":
        """文字列からTaskStatusを作成

        Args:
            status_str: ステータス文字列（大文字小文字不問）

        Returns:
            TaskStatus: 対応するTaskStatus

        Raises:
            ValueError: 無効なステータス文字列の場合
        """
        status_upper = status_str.upper()
        for status in cls:
            if status.value == status_upper:
                return status
        raise ValueError(f"Invalid task status: {status_str}")

    def can_transition_to(self, target_status: "TaskStatus") -> bool:
        """指定したステータスに遷移可能かチェック

        Args:
            target_status: 遷移先ステータス

        Returns:
            bool: 遷移可能な場合True
        """
        # 同じステータスへの遷移は不可
        if self == target_status:
            return False

        # すべての状態から他の状態への遷移を許可
        return True

    def __str__(self) -> str:
        """文字列表現"""
        return self.value
