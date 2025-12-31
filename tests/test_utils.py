"""utils.pyのテスト"""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from python_project_2026.utils import ensure_directory, format_size, safe_get


class TestEnsureDirectory:
    """ensure_directory関数のテスト"""

    def test_create_new_directory(self) -> None:
        """新しいディレクトリの作成をテスト"""
        with TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "new_dir"
            result = ensure_directory(test_path)

            assert result == test_path
            assert test_path.exists()
            assert test_path.is_dir()

    def test_existing_directory(self) -> None:
        """既存ディレクトリの処理をテスト"""
        with TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir)
            result = ensure_directory(test_path)

            assert result == test_path
            assert test_path.exists()
            assert test_path.is_dir()


class TestFormatSize:
    """format_size関数のテスト"""

    @pytest.mark.parametrize(
        "size_bytes,expected",
        [
            (0, "0B"),
            (512, "512.0B"),
            (1024, "1.0KB"),
            (1536, "1.5KB"),
            (1048576, "1.0MB"),
            (1073741824, "1.0GB"),
            (1099511627776, "1.0TB"),
        ],
    )
    def test_format_size(self, size_bytes: int, expected: str) -> None:
        """様々なサイズの変換をテスト"""
        assert format_size(size_bytes) == expected


class TestSafeGet:
    """safe_get関数のテスト"""

    def test_existing_key(self) -> None:
        """存在するキーの取得をテスト"""
        data = {"key": "value"}
        assert safe_get(data, "key") == "value"

    def test_missing_key_with_default(self) -> None:
        """存在しないキーのデフォルト値取得をテスト"""
        data: dict[str, str] = {}
        assert safe_get(data, "missing", "default") == "default"

    def test_missing_key_without_default(self) -> None:
        """存在しないキーでデフォルト値なしの場合をテスト"""
        data: dict[str, str] = {}
        assert safe_get(data, "missing") is None
