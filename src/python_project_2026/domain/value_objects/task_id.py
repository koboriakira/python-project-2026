"""タスクID ValueObject"""

from uuid import UUID, uuid4


class TaskId:
    """タスクの一意識別子を表すValueObject"""

    def __init__(self, value: str) -> None:
        """TaskIdを初期化

        Args:
            value: UUID文字列

        Raises:
            ValueError: 無効なUUID形式の場合
        """
        try:
            # UUID形式の妥当性をチェック
            UUID(value)
            self._value = value
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {value}") from e

    @classmethod
    def generate(cls) -> "TaskId":
        """新しいTaskIdを生成

        Returns:
            TaskId: 新しく生成されたTaskId
        """
        return cls(str(uuid4()))

    @property
    def value(self) -> str:
        """UUID文字列を取得"""
        return self._value

    def __str__(self) -> str:
        """文字列表現"""
        return self._value

    def __eq__(self, other: object) -> bool:
        """等価比較"""
        if not isinstance(other, TaskId):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """ハッシュ値計算"""
        return hash(self._value)
