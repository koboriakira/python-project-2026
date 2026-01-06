"""HTMX対応のWebルーター"""

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# テンプレート設定
templates = Jinja2Templates(directory="src/python_project_2026/templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """ホームページ表示"""
    return templates.TemplateResponse(request, "index.html")


@router.get("/api-info", response_class=HTMLResponse)
async def api_info(_request: Request) -> HTMLResponse:
    """APIルートエンドポイントの情報を取得してHTMLで返却"""
    try:
        # 内部APIエンドポイントから情報を取得
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/")
            data = response.json()

        # HTMLフラグメントを返却
        return HTMLResponse(f"""
        <div class="api-info-card env-{data.get("environment", "unknown").lower()}">
            <div class="api-info-header">
                <h3>API情報</h3>
                <span class="status-badge status-{data.get("environment", "unknown").lower()}">
                    {data.get("environment", "Unknown").upper()}
                </span>
            </div>
            <dl>
                <dt>メッセージ</dt>
                <dd>{data.get("message", "N/A")}</dd>

                <dt>バージョン</dt>
                <dd><code>{data.get("version", "N/A")}</code></dd>

                <dt>環境</dt>
                <dd>{data.get("environment", "N/A")}</dd>

                <dt>APIドキュメント</dt>
                <dd>
                    {f'<a href="{data.get("docs")}" target="_blank">Swagger UI</a>' if data.get("docs") else "本番環境では無効"}
                </dd>

                <dt>取得時刻</dt>
                <dd class="text-small text-muted">{__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</dd>
            </dl>

            <button
                hx-get="/api-info"
                hx-target="#api-info-container"
                hx-swap="innerHTML"
                hx-indicator="#loading-indicator"
                style="margin-top: 1rem;"
            >
                再読み込み
            </button>
        </div>
        """)

    except Exception as e:
        return HTMLResponse(f"""
        <div class="api-info-card" style="border-left: 4px solid var(--danger-color);">
            <div class="api-info-header">
                <h3>エラー</h3>
                <span class="status-badge" style="background-color: var(--danger-color); color: white;">
                    ERROR
                </span>
            </div>
            <p>API情報の取得に失敗しました。</p>
            <details>
                <summary>エラー詳細</summary>
                <pre style="background-color: var(--code-background-color); padding: 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;">{e!s}</pre>
            </details>

            <button
                hx-get="/api-info"
                hx-target="#api-info-container"
                hx-swap="innerHTML"
                hx-indicator="#loading-indicator"
                style="margin-top: 1rem;"
            >
                再試行
            </button>
        </div>
        """)


@router.get("/health-check", response_class=HTMLResponse)
async def health_check(_request: Request) -> HTMLResponse:
    """ヘルスチェック結果を取得してHTMLで返却"""
    try:
        # 内部APIエンドポイントからヘルス情報を取得
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            data = response.json()

        return HTMLResponse(f"""
        <div class="api-info-card">
            <div class="api-info-header">
                <h3>ヘルスチェック</h3>
                <span class="status-badge status-healthy">
                    {data.get("status", "unknown").upper()}
                </span>
            </div>
            <dl>
                <dt>ステータス</dt>
                <dd>{data.get("status", "unknown")}</dd>

                <dt>バージョン</dt>
                <dd><code>{data.get("version", "N/A")}</code></dd>

                <dt>最終チェック</dt>
                <dd class="text-small text-muted">{__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</dd>
            </dl>

            <button
                hx-get="/health-check"
                hx-target="#health-check-container"
                hx-swap="innerHTML"
                hx-trigger="click, every 5s"
                hx-indicator="#health-loading"
                style="margin-top: 1rem;"
            >
                再チェック (5秒ごとに自動更新)
            </button>
        </div>
        """)

    except Exception as e:
        return HTMLResponse(f"""
        <div class="api-info-card" style="border-left: 4px solid var(--danger-color);">
            <div class="api-info-header">
                <h3>ヘルスチェック</h3>
                <span class="status-badge" style="background-color: var(--danger-color); color: white;">
                    UNHEALTHY
                </span>
            </div>
            <p>ヘルスチェックに失敗しました。APIサーバーが停止している可能性があります。</p>
            <details>
                <summary>エラー詳細</summary>
                <pre style="background-color: var(--code-background-color); padding: 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;">{e!s}</pre>
            </details>

            <button
                hx-get="/health-check"
                hx-target="#health-check-container"
                hx-swap="innerHTML"
                hx-trigger="click, every 5s"
                hx-indicator="#health-loading"
                style="margin-top: 1rem;"
            >
                再試行 (5秒ごとに自動更新)
            </button>
        </div>
        """)
