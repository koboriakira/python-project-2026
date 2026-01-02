"""FastAPIアプリケーション"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import __version__
from .routers import hello


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """アプリケーションライフサイクル管理"""
    # 起動時の処理
    print("🚀 FastAPIアプリケーション起動")
    yield
    # 終了時の処理
    print("👋 FastAPIアプリケーション終了")


# FastAPIアプリケーション作成
app = FastAPI(
    title="Python Project 2026 API",
    description="2026年の最新Python開発テンプレート - FastAPI版",
    version=__version__,
    lifespan=lifespan,
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root() -> JSONResponse:
    """ルートエンドポイント"""
    return JSONResponse(
        content={
            "message": "Python Project 2026 API",
            "version": __version__,
            "docs": "/docs",
            "redoc": "/redoc",
        }
    )


@app.get("/health", tags=["Health"])
async def health() -> JSONResponse:
    """ヘルスチェックエンドポイント"""
    return JSONResponse(content={"status": "healthy", "version": __version__})


# ルーターを登録
app.include_router(hello.router, prefix="/api", tags=["Hello"])
