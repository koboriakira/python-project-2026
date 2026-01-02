"""InMemoryTaskRepositoryのテスト"""

import pytest

from python_project_2026.domain.entities.task import Task
from python_project_2026.domain.value_objects.task_id import TaskId
from python_project_2026.domain.value_objects.task_priority import TaskPriority
from python_project_2026.domain.value_objects.task_status import TaskStatus
from python_project_2026.infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository


class TestInMemoryTaskRepository:
    """InMemoryTaskRepositoryのテストクラス"""

    def setup_method(self) -> None:
        """各テスト前の初期化"""
        self.repository = InMemoryTaskRepository()

    @pytest.mark.asyncio
    async def test_save_task(self) -> None:
        """タスクを保存できる"""
        task = Task.create(TaskId.generate(), "テストタスク", "説明", TaskPriority.MEDIUM)

        await self.repository.save(task)

        found_task = await self.repository.find_by_id(task.id)
        assert found_task is not None
        assert found_task.id == task.id
        assert found_task.title == task.title

    @pytest.mark.asyncio
    async def test_save_task_update_existing(self) -> None:
        """既存タスクの保存（更新）ができる"""
        task = Task.create(TaskId.generate(), "元のタスク", "説明", TaskPriority.LOW)

        # 最初の保存
        await self.repository.save(task)

        # タスクを更新
        task.update_title("更新されたタスク")
        task.update_status(TaskStatus.IN_PROGRESS)

        # 再保存
        await self.repository.save(task)

        # 確認
        found_task = await self.repository.find_by_id(task.id)
        assert found_task is not None
        assert found_task.title == "更新されたタスク"
        assert found_task.status == TaskStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self) -> None:
        """存在しないIDで検索するとNoneを返す"""
        task_id = TaskId.generate()

        found_task = await self.repository.find_by_id(task_id)
        assert found_task is None

    @pytest.mark.asyncio
    async def test_find_all_empty(self) -> None:
        """空のリポジトリからfind_allすると空リストを返す"""
        tasks = await self.repository.find_all()
        assert tasks == []

    @pytest.mark.asyncio
    async def test_find_all_multiple_tasks(self) -> None:
        """複数タスクを保存してfind_allで取得できる"""
        task1 = Task.create(TaskId.generate(), "タスク1", "説明1", TaskPriority.HIGH)
        task2 = Task.create(TaskId.generate(), "タスク2", "説明2", TaskPriority.LOW)
        task3 = Task.create(TaskId.generate(), "タスク3", "説明3", TaskPriority.MEDIUM)

        await self.repository.save(task1)
        await self.repository.save(task2)
        await self.repository.save(task3)

        tasks = await self.repository.find_all()
        assert len(tasks) == 3

        task_ids = {task.id for task in tasks}
        assert task1.id in task_ids
        assert task2.id in task_ids
        assert task3.id in task_ids

    @pytest.mark.asyncio
    async def test_find_by_status(self) -> None:
        """ステータスでタスクを検索できる"""
        task1 = Task.create(TaskId.generate(), "タスク1", "説明1", TaskPriority.HIGH)
        task2 = Task.create(TaskId.generate(), "タスク2", "説明2", TaskPriority.LOW)
        task3 = Task.create(TaskId.generate(), "タスク3", "説明3", TaskPriority.MEDIUM)

        # task2のステータスを変更
        task2.update_status(TaskStatus.IN_PROGRESS)

        await self.repository.save(task1)
        await self.repository.save(task2)
        await self.repository.save(task3)

        # TODOステータスで検索
        todo_tasks = await self.repository.find_by_status(TaskStatus.TODO)
        assert len(todo_tasks) == 2
        todo_task_ids = {task.id for task in todo_tasks}
        assert task1.id in todo_task_ids
        assert task3.id in todo_task_ids

        # IN_PROGRESSステータスで検索
        in_progress_tasks = await self.repository.find_by_status(TaskStatus.IN_PROGRESS)
        assert len(in_progress_tasks) == 1
        assert in_progress_tasks[0].id == task2.id

    @pytest.mark.asyncio
    async def test_find_by_priority(self) -> None:
        """優先度でタスクを検索できる"""
        task1 = Task.create(TaskId.generate(), "タスク1", "説明1", TaskPriority.HIGH)
        task2 = Task.create(TaskId.generate(), "タスク2", "説明2", TaskPriority.LOW)
        task3 = Task.create(TaskId.generate(), "タスク3", "説明3", TaskPriority.HIGH)

        await self.repository.save(task1)
        await self.repository.save(task2)
        await self.repository.save(task3)

        # HIGH優先度で検索
        high_tasks = await self.repository.find_by_priority(TaskPriority.HIGH)
        assert len(high_tasks) == 2
        high_task_ids = {task.id for task in high_tasks}
        assert task1.id in high_task_ids
        assert task3.id in high_task_ids

        # LOW優先度で検索
        low_tasks = await self.repository.find_by_priority(TaskPriority.LOW)
        assert len(low_tasks) == 1
        assert low_tasks[0].id == task2.id

    @pytest.mark.asyncio
    async def test_delete_existing_task(self) -> None:
        """存在するタスクを削除できる"""
        task = Task.create(TaskId.generate(), "削除予定タスク", "説明", TaskPriority.MEDIUM)

        await self.repository.save(task)

        # 削除実行
        result = await self.repository.delete(task.id)
        assert result is True

        # 削除後は検索できない
        found_task = await self.repository.find_by_id(task.id)
        assert found_task is None

    @pytest.mark.asyncio
    async def test_delete_non_existing_task(self) -> None:
        """存在しないタスクを削除しようとするとFalseを返す"""
        task_id = TaskId.generate()

        result = await self.repository.delete(task_id)
        assert result is False
