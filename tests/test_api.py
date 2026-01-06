"""FastAPI APIテスト"""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from python_project_2026 import __version__
from python_project_2026.api import app


class TestAPI:
    """FastAPI APIテストクラス"""

    @pytest.fixture
    def client(self) -> TestClient:
        """TestClientフィクスチャ"""
        return TestClient(app)

    def test_root_endpoint(self, client: TestClient) -> None:
        """ルートエンドポイントのテスト (HTMLページ)"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "HTMX Demo" in response.text
        assert "Python Project 2026" in response.text

    def test_api_root_endpoint(self, client: TestClient) -> None:
        """APIルートエンドポイントのテスト"""
        response = client.get("/api/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Python Project 2026 API"
        assert data["version"] == __version__
        assert "docs" in data
        assert "redoc" in data

    def test_health_endpoint(self, client: TestClient) -> None:
        """ヘルスチェックエンドポイントのテスト"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == __version__

    def test_hello_endpoint_default(self, client: TestClient) -> None:
        """挨拶エンドポイントのテスト(デフォルト)"""
        response = client.get("/api/hello")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "こんにちは、World!"
        assert data["name"] == "World"

    def test_hello_endpoint_with_name(self, client: TestClient) -> None:
        """挨拶エンドポイントのテスト(名前指定)"""
        response = client.get("/api/hello?name=Alice")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "こんにちは、Alice!"
        assert data["name"] == "Alice"

    @pytest.mark.parametrize(
        "name,expected_message",
        [
            ("太郎", "こんにちは、太郎!"),
            ("花子", "こんにちは、花子!"),
            ("123", "こんにちは、123!"),
            ("", "こんにちは、!"),
        ],
    )
    def test_hello_endpoint_parametrized(self, client: TestClient, name: str, expected_message: str) -> None:
        """挨拶エンドポイントのパラメータ化テスト"""
        response = client.get(f"/api/hello?name={name}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == expected_message
        assert data["name"] == name

    def test_version_endpoint(self, client: TestClient) -> None:
        """バージョンエンドポイントのテスト"""
        response = client.get("/api/version")
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == __version__
        assert "python_version" in data
        # Pythonバージョン形式をチェック(例: "3.12.0")
        python_version = data["python_version"]
        parts = python_version.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)

    def test_openapi_docs_not_accessible_in_production(self, client: TestClient) -> None:
        """本番環境でOpenAPIドキュメントにアクセスできないことをテスト"""
        response = client.get("/docs")
        assert response.status_code == 404

    def test_openapi_json_not_accessible_in_production(self, client: TestClient) -> None:
        """本番環境でOpenAPI JSONスキーマにアクセスできないことをテスト"""
        response = client.get("/openapi.json")
        assert response.status_code == 404


class TestEnvironmentConfiguration:
    """環境設定のテストクラス"""

    def test_default_environment_is_production(self) -> None:
        """デフォルト環境が本番環境であることを確認"""
        # 環境変数をクリアして再インポート
        with patch.dict(os.environ, {}, clear=True):
            # モジュールを再読み込み
            import importlib

            from python_project_2026 import api

            importlib.reload(api)

            assert api.ENVIRONMENT == "production"
            assert api.IS_DEVELOPMENT is False

    def test_development_environment_detection(self) -> None:
        """開発環境の検出テスト"""
        test_cases = [
            ("development", True),
            ("dev", True),
            ("local", True),
            ("Development", True),  # 大文字小文字を区別しない
            ("DEV", True),
        ]

        for env_value, expected_is_dev in test_cases:
            with patch.dict(os.environ, {"ENVIRONMENT": env_value}, clear=True):
                import importlib

                from python_project_2026 import api

                importlib.reload(api)

                assert expected_is_dev == api.IS_DEVELOPMENT, f"Failed for ENVIRONMENT={env_value}"

    def test_production_environment_detection(self) -> None:
        """本番環境の検出テスト"""
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True):
            import importlib

            from python_project_2026 import api

            importlib.reload(api)

            assert api.ENVIRONMENT == "production"
            assert api.IS_DEVELOPMENT is False

    def test_debug_flag_enables_development_mode(self) -> None:
        """DEBUGフラグで開発モードが有効になることを確認"""
        test_cases = [
            ("true", True),
            ("True", True),
            ("1", True),
            ("yes", True),
            ("false", False),
            ("0", False),
            ("no", False),
        ]

        for debug_value, expected_is_dev in test_cases:
            with patch.dict(os.environ, {"DEBUG": debug_value, "ENVIRONMENT": "production"}, clear=True):
                import importlib

                from python_project_2026 import api

                importlib.reload(api)

                assert expected_is_dev == api.IS_DEVELOPMENT, f"Failed for DEBUG={debug_value}"

    def test_allowed_origins_parsing(self) -> None:
        """許可するオリジンのパースのテスト"""
        origins = "https://example.com,https://api.example.com,https://app.example.com"
        with patch.dict(os.environ, {"ALLOWED_ORIGINS": origins}, clear=True):
            import importlib

            from python_project_2026 import api

            importlib.reload(api)

            expected = ["https://example.com", "https://api.example.com", "https://app.example.com"]
            assert expected == api.ALLOWED_ORIGINS

    def test_empty_allowed_origins(self) -> None:
        """ALLOWED_ORIGINSが空の場合のテスト"""
        with patch.dict(os.environ, {}, clear=True):
            import importlib

            from python_project_2026 import api

            importlib.reload(api)

            assert api.ALLOWED_ORIGINS == []

    def test_api_root_endpoint_includes_environment(self) -> None:
        """APIルートエンドポイントに環境情報が含まれることを確認"""
        client = TestClient(app)
        response = client.get("/api/")
        assert response.status_code == 200
        data = response.json()
        assert "environment" in data
        assert data["environment"] in ["production", "development", "dev", "local"]

    def test_openapi_docs_accessible_in_development(self) -> None:
        """開発環境でOpenAPIドキュメントにアクセス可能であることをテスト"""
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True):
            import importlib

            from python_project_2026 import api

            importlib.reload(api)

            # 開発環境でアプリを再作成
            dev_client = TestClient(api.app)
            response = dev_client.get("/docs")
            assert response.status_code == 200

    def test_openapi_json_accessible_in_development(self) -> None:
        """開発環境でOpenAPI JSONスキーマにアクセス可能であることをテスト"""
        with patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True):
            import importlib

            from python_project_2026 import api

            importlib.reload(api)

            # 開発環境でアプリを再作成
            dev_client = TestClient(api.app)
            response = dev_client.get("/openapi.json")
            assert response.status_code == 200
            data = response.json()
            assert data["info"]["title"] == "Python Project 2026 API"
            assert "version" in data["info"]
