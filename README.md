# Python Project 2026

2026年の最新Python開発テンプレート - uv、ruff、pytestを使った現代的な開発環境

## 🚀 クイックスタート

ワンコマンドで新しいPythonプロジェクトを作成：

```bash
curl -fsSL https://raw.githubusercontent.com/koboriakira/python-project-2026/main/install.sh | sh -s my-new-project
```

作成後：

```bash
cd my-new-project
uv run pytest  # テスト実行
uv run my-new-project --help  # アプリケーション確認
```

## 📋 テンプレートとして使用

手動でテンプレートを使用する場合：

```bash
# このリポジトリをクローン
git clone https://github.com/koboriakira/python-project-2026.git
cd python-project-2026

# 新しいプロジェクトを作成
./install.sh my-new-project

# 作成されたプロジェクトに移動
cd my-new-project

# 開発開始！
uv run pytest  # テスト実行
uv run my-new-project --help  # アプリケーション確認
```

### install.shの機能

- ✅ **自動ダウンロード**: GitHubから最新のテンプレートを取得
- ✅ **完全なファイルコピー**: すべてのテンプレートファイルを新しいディレクトリにコピー
- ✅ **名前の一括置換**: プロジェクト名・パッケージ名を適切に変換
- ✅ **Git初期化**: 新しいGitリポジトリの初期化と初回コミット
- ✅ **環境セットアップ**: uv syncによる依存関係のインストール
- ✅ **エラーハンドリング**: 無効な名前や既存ディレクトリの検証

## 特徴

- 🚀 **超高速**: uvによる爆速パッケージ管理
- 🛠️ **最新ツール**: ruff、mypy、pytest、Claude Code hooks、pre-commit
- 📦 **モダンな構成**: pyproject.tomlによる一元管理
- 🧪 **完全なテスト**: カバレッジ測定とCI/CD
- 🔧 **開発者体験**: リンター、フォーマッター、型チェック
- 🚀 **自動リリース**: release-pleaseによるセマンティックバージョニング

## 必要要件

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (推奨)

## セットアップ

### uvを使用（推奨）

```bash
# uvのインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# プロジェクトのセットアップ
uv sync

# 品質管理ツールのセットアップ
uv run pre-commit install              # Git hooks（手動開発時）
# Claude Code hooks（AI統合）は .claude/settings.local.json で設定済み
```

### 従来の方法

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## 開発コマンド

```bash
# テスト実行
uv run pytest

# テスト（カバレッジ付き）
uv run pytest --cov

# コードフォーマット
uv run ruff format .

# リンティング
uv run ruff check .

# 型チェック
uv run mypy

# 品質チェック実行
.claude/scripts/pre-commit-replacement.sh   # Claude Code hooks（推奨）
uv run pre-commit run --all-files           # 従来のpre-commit

# アプリケーション実行
uv run python-project-2026 hello --name "開発者"
```

## FastAPI Web API

FastAPIによるモダンなWeb APIも実装されています：

```bash
# 開発サーバー起動
uv run uvicorn python_project_2026.api:app --reload

# APIドキュメントにアクセス
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)

# APIテスト実行
uv run pytest tests/test_api.py
```

## プロジェクト構造

```
python-project-2026/
├── src/
│   └── python_project_2026/
│       ├── __init__.py
│       ├── main.py          # CLIエントリーポイント
│       ├── api.py           # FastAPI アプリケーション
│       ├── utils.py
│       └── routers/         # FastAPI ルーター
│           ├── __init__.py
│           └── hello.py
├── tests/
│   ├── test_main.py
│   ├── test_api.py          # API テスト
│   └── test_utils.py
├── pyproject.toml
├── README.md
└── .pre-commit-config.yaml
```

## 設定ファイル

すべての設定は `pyproject.toml` に統一されています：

- **ruff**: リンティングとフォーマット
- **pytest**: テストの実行と設定
- **mypy**: 型チェック
- **coverage**: カバレッジ測定

## デプロイ

### Render（FastAPI Web Service）

[Render](https://render.com)を使用したFastAPIアプリケーションのデプロイが可能です：

#### デプロイ設定

1. Render Dashboardで"New Web Service"を作成
2. GitHubリポジトリを接続
3. 以下の設定を使用：

| 項目 | 設定値 |
|------|--------|
| **Root Directory** | （指定なし） |
| **Build Command** | `uv sync --frozen && uv cache prune --ci` |
| **Start Command** | `uvicorn src.python_project_2026.api:app --host 0.0.0.0 --port $PORT` |
| **Language** | Python 3 |

#### デプロイ後のアクセス

- **API Root**: `https://your-app.onrender.com/`
- **API ドキュメント**: `https://your-app.onrender.com/docs`
- **ReDoc**: `https://your-app.onrender.com/redoc`

#### 注意事項

- 本番環境では[api.py](src/python_project_2026/api.py)のCORS設定を適切に制限してください
- 環境変数はRender DashboardまたはBlueprint（render.yaml）で管理可能

## CI/CD

GitHub Actionsによる自動化：

- マルチプラットフォーム（Linux、Windows、macOS）
- 複数Python バージョン（3.12、3.13）
- テスト、リンティング、型チェック
- セキュリティ監査

## 自動リリース管理

[release-please](https://github.com/googleapis/release-please)による自動リリース：

### Conventional Commits使用例

```bash
# パッチバージョン更新 (0.1.0 → 0.1.1)
git commit -m "fix: バリデーションエラーを修正"

# マイナーバージョン更新 (0.1.0 → 0.2.0)
git commit -m "feat: 新しい機能を追加"

# メジャーバージョン更新 (0.1.0 → 1.0.0)
git commit -m "feat!: 破壊的変更を実装"
```

### 自動化される処理

- **バージョン更新**: Conventional Commitsに基づいてセマンティックバージョニング
- **CHANGELOG生成**: コミットメッセージから自動的にCHANGELOGを更新
- **GitHub Releases**: 新しいバージョンのリリースを自動作成
- **PyPI公開**: 本番環境とテスト環境への自動パッケージ公開

## ライセンス

MIT License
