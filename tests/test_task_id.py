"""TaskId ValueObjectのテスト"""

import pytest

from python_project_2026.domain.value_objects.task_id import TaskId


class TestTaskId:
    """TaskId ValueObjectのテストクラス"""

    def test_create_new_task_id(self) -> None:
        """新しいTaskIdを生成できる"""
        task_id = TaskId.generate()
        assert isinstance(task_id.value, str)
        assert len(task_id.value) == 36  # UUID4の文字列長

    def test_create_from_string(self) -> None:
        """文字列からTaskIdを作成できる"""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        task_id = TaskId(uuid_str)
        assert task_id.value == uuid_str

    def test_create_from_invalid_string(self) -> None:
        """無効な文字列からTaskIdを作成しようとすると例外が発生する"""
        with pytest.raises(ValueError, match="Invalid UUID format"):
            TaskId("invalid-uuid")

    def test_equality(self) -> None:
        """同じ値のTaskIdは等価"""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        task_id1 = TaskId(uuid_str)
        task_id2 = TaskId(uuid_str)
        task_id3 = TaskId.generate()

        assert task_id1 == task_id2
        assert task_id1 != task_id3

    def test_string_representation(self) -> None:
        """文字列表現が正しい"""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        task_id = TaskId(uuid_str)
        assert str(task_id) == uuid_str

    def test_hash_support(self) -> None:
        """ハッシュ化をサポートしている"""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        task_id1 = TaskId(uuid_str)
        task_id2 = TaskId(uuid_str)

        # 同じ値は同じハッシュ値
        assert hash(task_id1) == hash(task_id2)

        # セットに使用できる
        task_ids = {task_id1, task_id2}
        assert len(task_ids) == 1

    def test_generate_unique_ids(self) -> None:
        """generate()は毎回ユニークなIDを生成する"""
        ids = [TaskId.generate() for _ in range(100)]
        unique_ids = set(ids)
        assert len(unique_ids) == 100  # すべてユニーク
