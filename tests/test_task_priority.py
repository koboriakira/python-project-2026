"""TaskPriority ValueObjectのテスト"""

import pytest

from python_project_2026.domain.value_objects.task_priority import TaskPriority


class TestTaskPriority:
    """TaskPriority ValueObjectのテストクラス"""

    def test_create_valid_priority(self) -> None:
        """有効な優先度でValueObjectを作成できる"""
        priority = TaskPriority.MEDIUM
        assert priority.value == 2

    def test_all_priority_values(self) -> None:
        """すべての優先度値を正しく作成できる"""
        assert TaskPriority.LOW.value == 1
        assert TaskPriority.MEDIUM.value == 2
        assert TaskPriority.HIGH.value == 3

    def test_from_string_valid_values(self) -> None:
        """文字列からTaskPriorityを作成できる"""
        assert TaskPriority.from_string("LOW") == TaskPriority.LOW
        assert TaskPriority.from_string("MEDIUM") == TaskPriority.MEDIUM
        assert TaskPriority.from_string("HIGH") == TaskPriority.HIGH

    def test_from_string_case_insensitive(self) -> None:
        """大文字小文字を区別せずに文字列からTaskPriorityを作成できる"""
        assert TaskPriority.from_string("low") == TaskPriority.LOW
        assert TaskPriority.from_string("medium") == TaskPriority.MEDIUM
        assert TaskPriority.from_string("high") == TaskPriority.HIGH

    def test_from_string_invalid_value(self) -> None:
        """無効な文字列からTaskPriorityを作成しようとすると例外が発生する"""
        with pytest.raises(ValueError, match="Invalid task priority"):
            TaskPriority.from_string("INVALID")

    def test_from_int_valid_values(self) -> None:
        """整数からTaskPriorityを作成できる"""
        assert TaskPriority.from_int(1) == TaskPriority.LOW
        assert TaskPriority.from_int(2) == TaskPriority.MEDIUM
        assert TaskPriority.from_int(3) == TaskPriority.HIGH

    def test_from_int_invalid_value(self) -> None:
        """無効な整数からTaskPriorityを作成しようとすると例外が発生する"""
        with pytest.raises(ValueError, match="Invalid task priority"):
            TaskPriority.from_int(0)
        with pytest.raises(ValueError, match="Invalid task priority"):
            TaskPriority.from_int(4)

    def test_string_representation(self) -> None:
        """文字列表現が正しい"""
        assert str(TaskPriority.LOW) == "LOW"
        assert str(TaskPriority.MEDIUM) == "MEDIUM"
        assert str(TaskPriority.HIGH) == "HIGH"

    def test_comparison(self) -> None:
        """優先度の比較ができる"""
        assert TaskPriority.LOW < TaskPriority.MEDIUM
        assert TaskPriority.MEDIUM < TaskPriority.HIGH
        assert TaskPriority.HIGH > TaskPriority.LOW

    def test_equality(self) -> None:
        """同じ値のTaskPriorityは等価"""
        priority1 = TaskPriority.MEDIUM
        priority2 = TaskPriority.MEDIUM
        priority3 = TaskPriority.HIGH

        assert priority1 == priority2
        assert priority1 != priority3
