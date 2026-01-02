"""FastAPI APIテスト"""

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
        """ルートエンドポイントのテスト"""
        response = client.get("/")
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

    def test_openapi_docs_accessible(self, client: TestClient) -> None:
        """OpenAPIドキュメントにアクセス可能かテスト"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json_accessible(self, client: TestClient) -> None:
        """OpenAPI JSONスキーマにアクセス可能かテスト"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "Python Project 2026 API"
        assert data["info"]["version"] == __version__
