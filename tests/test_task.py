"""Task Entityのテスト"""

from datetime import datetime

import pytest

from python_project_2026.domain.entities.task import Task
from python_project_2026.domain.value_objects.task_id import TaskId
from python_project_2026.domain.value_objects.task_priority import TaskPriority
from python_project_2026.domain.value_objects.task_status import TaskStatus


class TestTask:
    """Task Entityのテストクラス"""

    def test_create_task(self) -> None:
        """タスクを作成できる"""
        task_id = TaskId.generate()
        title = "サンプルタスク"
        description = "これはテストタスクです"
        priority = TaskPriority.MEDIUM

        task = Task.create(task_id, title, description, priority)

        assert task.id == task_id
        assert task.title == title
        assert task.description == description
        assert task.priority == priority
        assert task.status == TaskStatus.TODO
        assert isinstance(task.created_at, datetime)
        assert task.updated_at == task.created_at

    def test_create_task_with_empty_description(self) -> None:
        """説明が空でもタスクを作成できる"""
        task_id = TaskId.generate()
        title = "サンプルタスク"
        priority = TaskPriority.LOW

        task = Task.create(task_id, title, "", priority)

        assert task.description == ""

    def test_create_task_with_invalid_title(self) -> None:
        """無効なタイトルでタスクを作成しようとすると例外が発生する"""
        task_id = TaskId.generate()
        priority = TaskPriority.LOW

        # 空文字列
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task.create(task_id, "", "説明", priority)

        # Noneチェック
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task.create(task_id, None, "説明", priority)  # type: ignore

    def test_update_status(self) -> None:
        """ステータスを更新できる"""
        task = Task.create(TaskId.generate(), "タスク", "説明", TaskPriority.MEDIUM)
        original_created_at = task.created_at
        original_updated_at = task.updated_at

        # 少し待つ（更新時間の差を確認するため）
        import time

        time.sleep(0.01)

        task.update_status(TaskStatus.IN_PROGRESS)

        assert task.status == TaskStatus.IN_PROGRESS
        assert task.created_at == original_created_at  # 作成日は不変
        assert task.updated_at > original_updated_at  # 更新日は変更される

    def test_update_status_with_invalid_transition(self) -> None:
        """無効な遷移でステータスを更新しようとすると例外が発生する"""
        task = Task.create(TaskId.generate(), "タスク", "説明", TaskPriority.MEDIUM)

        # 同じステータスへの遷移は不可
        with pytest.raises(ValueError, match="Cannot transition from TODO to TODO"):
            task.update_status(TaskStatus.TODO)

    def test_update_title(self) -> None:
        """タイトルを更新できる"""
        task = Task.create(TaskId.generate(), "元のタイトル", "説明", TaskPriority.MEDIUM)

        new_title = "新しいタイトル"
        task.update_title(new_title)

        assert task.title == new_title

    def test_update_title_with_invalid_value(self) -> None:
        """無効なタイトルで更新しようとすると例外が発生する"""
        task = Task.create(TaskId.generate(), "元のタイトル", "説明", TaskPriority.MEDIUM)

        with pytest.raises(ValueError, match="Title cannot be empty"):
            task.update_title("")

    def test_update_description(self) -> None:
        """説明を更新できる"""
        task = Task.create(TaskId.generate(), "タイトル", "元の説明", TaskPriority.MEDIUM)

        new_description = "新しい説明"
        task.update_description(new_description)

        assert task.description == new_description

    def test_update_priority(self) -> None:
        """優先度を更新できる"""
        task = Task.create(TaskId.generate(), "タイトル", "説明", TaskPriority.LOW)

        task.update_priority(TaskPriority.HIGH)

        assert task.priority == TaskPriority.HIGH

    def test_equality(self) -> None:
        """同じIDのタスクは等価"""
        task_id = TaskId.generate()
        task1 = Task.create(task_id, "タスク1", "説明1", TaskPriority.LOW)
        task2 = Task.create(task_id, "タスク2", "説明2", TaskPriority.HIGH)
        task3 = Task.create(TaskId.generate(), "タスク3", "説明3", TaskPriority.MEDIUM)

        assert task1 == task2  # 同じIDなので等価
        assert task1 != task3  # 異なるIDなので非等価

    def test_hash_support(self) -> None:
        """ハッシュ化をサポートしている"""
        task_id = TaskId.generate()
        task1 = Task.create(task_id, "タスク1", "説明1", TaskPriority.LOW)
        task2 = Task.create(task_id, "タスク2", "説明2", TaskPriority.HIGH)

        # 同じIDは同じハッシュ値
        assert hash(task1) == hash(task2)

        # セットに使用できる
        tasks = {task1, task2}
        assert len(tasks) == 1

    def test_string_representation(self) -> None:
        """文字列表現が適切"""
        task = Task.create(TaskId.generate(), "サンプルタスク", "説明", TaskPriority.MEDIUM)

        str_repr = str(task)
        assert "サンプルタスク" in str_repr
        assert "MEDIUM" in str_repr
        assert "TODO" in str_repr
