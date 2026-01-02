"""TaskStatus ValueObjectのテスト"""

import pytest

from python_project_2026.domain.value_objects.task_status import TaskStatus


class TestTaskStatus:
    """TaskStatus ValueObjectのテストクラス"""

    def test_create_valid_status(self) -> None:
        """有効なステータスでValueObjectを作成できる"""
        status = TaskStatus.TODO
        assert status.value == "TODO"

    def test_all_status_values(self) -> None:
        """すべてのステータス値を正しく作成できる"""
        assert TaskStatus.TODO.value == "TODO"
        assert TaskStatus.IN_PROGRESS.value == "IN_PROGRESS"
        assert TaskStatus.DONE.value == "DONE"

    def test_from_string_valid_values(self) -> None:
        """文字列からTaskStatusを作成できる"""
        assert TaskStatus.from_string("TODO") == TaskStatus.TODO
        assert TaskStatus.from_string("IN_PROGRESS") == TaskStatus.IN_PROGRESS
        assert TaskStatus.from_string("DONE") == TaskStatus.DONE

    def test_from_string_case_insensitive(self) -> None:
        """大文字小文字を区別せずに文字列からTaskStatusを作成できる"""
        assert TaskStatus.from_string("todo") == TaskStatus.TODO
        assert TaskStatus.from_string("in_progress") == TaskStatus.IN_PROGRESS
        assert TaskStatus.from_string("done") == TaskStatus.DONE

    def test_from_string_invalid_value(self) -> None:
        """無効な文字列からTaskStatusを作成しようとすると例外が発生する"""
        with pytest.raises(ValueError, match="Invalid task status"):
            TaskStatus.from_string("INVALID")

    def test_string_representation(self) -> None:
        """文字列表現が正しい"""
        assert str(TaskStatus.TODO) == "TODO"
        assert str(TaskStatus.IN_PROGRESS) == "IN_PROGRESS"
        assert str(TaskStatus.DONE) == "DONE"

    def test_equality(self) -> None:
        """同じ値のTaskStatusは等価"""
        status1 = TaskStatus.TODO
        status2 = TaskStatus.TODO
        status3 = TaskStatus.DONE

        assert status1 == status2
        assert status1 != status3

    def test_can_transition_to(self) -> None:
        """ステータス遷移可能性をチェックできる"""
        # TODO -> IN_PROGRESS, DONE
        assert TaskStatus.TODO.can_transition_to(TaskStatus.IN_PROGRESS)
        assert TaskStatus.TODO.can_transition_to(TaskStatus.DONE)
        assert not TaskStatus.TODO.can_transition_to(TaskStatus.TODO)

        # IN_PROGRESS -> DONE, TODO
        assert TaskStatus.IN_PROGRESS.can_transition_to(TaskStatus.DONE)
        assert TaskStatus.IN_PROGRESS.can_transition_to(TaskStatus.TODO)
        assert not TaskStatus.IN_PROGRESS.can_transition_to(TaskStatus.IN_PROGRESS)

        # DONE -> TODO, IN_PROGRESS
        assert TaskStatus.DONE.can_transition_to(TaskStatus.TODO)
        assert TaskStatus.DONE.can_transition_to(TaskStatus.IN_PROGRESS)
        assert not TaskStatus.DONE.can_transition_to(TaskStatus.DONE)
