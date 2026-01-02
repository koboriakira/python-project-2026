"""CreateTaskUseCaseのテスト"""

import pytest

from python_project_2026.application.use_cases.create_task import CreateTaskUseCase
from python_project_2026.domain.value_objects.task_id import TaskId
from python_project_2026.domain.value_objects.task_priority import TaskPriority
from python_project_2026.domain.value_objects.task_status import TaskStatus
from python_project_2026.infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository


class TestCreateTaskUseCase:
    """CreateTaskUseCaseのテストクラス"""

    def setup_method(self) -> None:
        """各テスト前の初期化"""
        self.repository = InMemoryTaskRepository()
        self.use_case = CreateTaskUseCase(self.repository)

    @pytest.mark.asyncio
    async def test_create_task_success(self) -> None:
        """タスクの作成が成功する"""
        title = "新しいタスク"
        description = "これは新しいタスクです"
        priority = TaskPriority.HIGH

        task_id = await self.use_case.execute(title, description, priority)

        # タスクIDが生成される
        assert isinstance(task_id, TaskId)

        # リポジトリに保存される
        saved_task = await self.repository.find_by_id(task_id)
        assert saved_task is not None
        assert saved_task.title == title
        assert saved_task.description == description
        assert saved_task.priority == priority
        assert saved_task.status == TaskStatus.TODO

    @pytest.mark.asyncio
    async def test_create_task_with_empty_description(self) -> None:
        """説明が空でもタスクを作成できる"""
        title = "シンプルなタスク"
        description = ""
        priority = TaskPriority.LOW

        task_id = await self.use_case.execute(title, description, priority)

        saved_task = await self.repository.find_by_id(task_id)
        assert saved_task is not None
        assert saved_task.description == ""

    @pytest.mark.asyncio
    async def test_create_task_with_invalid_title(self) -> None:
        """無効なタイトルでタスク作成しようとすると例外が発生する"""
        description = "説明"
        priority = TaskPriority.MEDIUM

        with pytest.raises(ValueError, match="Title cannot be empty"):
            await self.use_case.execute("", description, priority)

        with pytest.raises(ValueError, match="Title cannot be empty"):
            await self.use_case.execute("   ", description, priority)
