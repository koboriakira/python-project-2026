"""FastAPIアプリケーション"""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import __version__
from .routers import hello

# 環境設定
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # デフォルトは本番環境
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []

# 開発環境判定
IS_DEVELOPMENT = ENVIRONMENT.lower() in ("development", "dev", "local") or DEBUG


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """アプリケーションライフサイクル管理"""
    # 起動時の処理
    env_label = "開発環境" if IS_DEVELOPMENT else "本番環境"
    print(f"🚀 FastAPIアプリケーション起動 [{env_label}]")
    if IS_DEVELOPMENT:
        print("⚠️  開発モード: セキュリティ制限が緩和されています")
    yield
    # 終了時の処理
    print("👋 FastAPIアプリケーション終了")


# FastAPIアプリケーション作成
app = FastAPI(
    title="Python Project 2026 API",
    description="2026年の最新Python開発テンプレート - FastAPI版",
    version=__version__,
    lifespan=lifespan,
    # 本番環境ではドキュメントを無効化(オプション)
    docs_url="/docs" if IS_DEVELOPMENT else None,
    redoc_url="/redoc" if IS_DEVELOPMENT else None,
    openapi_url="/openapi.json" if IS_DEVELOPMENT else None,
)

# CORS設定(環境に応じて切り替え)
if IS_DEVELOPMENT:
    # 開発環境: すべてのオリジンを許可
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # 本番環境: 指定されたオリジンのみ許可
    if not ALLOWED_ORIGINS:
        # 環境変数が設定されていない場合のフォールバック
        print("⚠️  警告: ALLOWED_ORIGINSが設定されていません。CORSは無効化されます。")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Content-Type", "Authorization"],
    )


@app.get("/", tags=["Root"])
async def root() -> JSONResponse:
    """ルートエンドポイント"""
    return JSONResponse(
        content={
            "message": "Python Project 2026 API",
            "version": __version__,
            "environment": ENVIRONMENT,
            "docs": "/docs" if IS_DEVELOPMENT else None,
            "redoc": "/redoc" if IS_DEVELOPMENT else None,
        }
    )


@app.get("/health", tags=["Health"])
async def health() -> JSONResponse:
    """ヘルスチェックエンドポイント"""
    return JSONResponse(content={"status": "healthy", "version": __version__})


# ルーターを登録
app.include_router(hello.router, prefix="/api", tags=["Hello"])
