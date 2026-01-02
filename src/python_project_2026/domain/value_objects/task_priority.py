"""タスク優先度 ValueObject"""

from enum import Enum


class TaskPriority(Enum):
    """タスクの優先度を表すValueObject"""

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @classmethod
    def from_string(cls, priority_str: str) -> "TaskPriority":
        """文字列からTaskPriorityを作成

        Args:
            priority_str: 優先度文字列（大文字小文字不問）

        Returns:
            TaskPriority: 対応するTaskPriority

        Raises:
            ValueError: 無効な優先度文字列の場合
        """
        priority_upper = priority_str.upper()
        for priority in cls:
            if priority.name == priority_upper:
                return priority
        raise ValueError(f"Invalid task priority: {priority_str}")

    @classmethod
    def from_int(cls, priority_int: int) -> "TaskPriority":
        """整数からTaskPriorityを作成

        Args:
            priority_int: 優先度の整数値

        Returns:
            TaskPriority: 対応するTaskPriority

        Raises:
            ValueError: 無効な優先度値の場合
        """
        for priority in cls:
            if priority.value == priority_int:
                return priority
        raise ValueError(f"Invalid task priority: {priority_int}")

    def __str__(self) -> str:
        """文字列表現"""
        return self.name

    def __lt__(self, other: "TaskPriority") -> bool:
        """比較演算子: 小なり"""
        if not isinstance(other, TaskPriority):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other: "TaskPriority") -> bool:
        """比較演算子: 小なりイコール"""
        if not isinstance(other, TaskPriority):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other: "TaskPriority") -> bool:
        """比較演算子: 大なり"""
        if not isinstance(other, TaskPriority):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other: "TaskPriority") -> bool:
        """比較演算子: 大なりイコール"""
        if not isinstance(other, TaskPriority):
            return NotImplemented
        return self.value >= other.value
