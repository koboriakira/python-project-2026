"""挨拶APIルーター"""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter()


class HelloResponse(BaseModel):
    """挨拶レスポンス"""

    message: str = Field(..., description="挨拶メッセージ")
    name: str = Field(..., description="挨拶した相手の名前")


class VersionResponse(BaseModel):
    """バージョン情報レスポンス"""

    version: str = Field(..., description="アプリケーションのバージョン")
    python_version: str = Field(..., description="Pythonのバージョン")


@router.get("/hello", response_model=HelloResponse)
async def hello(
    name: str = Query("World", description="挨拶する相手の名前"),
) -> HelloResponse:
    """挨拶メッセージを返します

    Args:
        name: 挨拶する相手の名前

    Returns:
        挨拶メッセージ
    """
    return HelloResponse(message=f"こんにちは、{name}!", name=name)


@router.get("/version", response_model=VersionResponse)
async def version() -> VersionResponse:
    """バージョン情報を返します

    Returns:
        アプリケーションとPythonのバージョン情報
    """
    import sys

    from python_project_2026 import __version__

    return VersionResponse(
        version=__version__,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    )
