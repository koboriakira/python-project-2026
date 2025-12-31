"""main.pyのテスト"""

from typer.testing import CliRunner

from python_project_2026 import __version__
from python_project_2026.main import app


class TestCLI:
    """CLIアプリケーションのテスト"""

    def setup_method(self) -> None:
        """テスト用のCLIランナーをセットアップ"""
        self.runner = CliRunner()

    def test_hello_default(self) -> None:
        """デフォルトの挨拶をテスト"""
        result = self.runner.invoke(app, ["hello"])
        assert result.exit_code == 0
        assert "こんにちは、World!" in result.stdout

    def test_hello_with_name(self) -> None:
        """名前を指定した挨拶をテスト"""
        result = self.runner.invoke(app, ["hello", "--name", "テスト"])
        assert result.exit_code == 0
        assert "こんにちは、テスト!" in result.stdout

    def test_version(self) -> None:
        """バージョン表示をテスト"""
        result = self.runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert __version__ in result.stdout
