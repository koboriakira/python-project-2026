# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

2026年の最新Python開発テンプレートプロジェクト。uv、ruff、pytest、mypy、Claude Code hooks、pre-commitを使用したモダンなPython開発環境を提供。

## 開発環境とツール

### パッケージ管理: uv
- **uv**: 超高速なRust製パッケージマネージャー（pip、venv、pipxの代替）
- 仮想環境の自動管理とキャッシュ最適化により10-100倍高速

### 必須開発コマンド

```bash
# 環境セットアップ
uv sync                          # 依存関係をインストール（初回・更新時）

# テスト実行
uv run pytest                    # 基本テスト実行
uv run pytest --cov             # カバレッジ付きテスト
uv run pytest -v                # 詳細モード
uv run pytest tests/test_*.py   # 特定のテストファイル

# コード品質チェック
uv run ruff check .              # リンティング
uv run ruff format .             # フォーマット
uv run mypy                      # 型チェック

# 開発者ツール
# Claude Code hooks（推奨）
.claude/scripts/pre-commit-replacement.sh  # 統合品質チェック
.claude/scripts/code-quality.sh           # Python コード品質チェック
.claude/scripts/run-tests.sh              # テスト実行
.claude/scripts/file-checks.sh            # ファイル品質チェック

# 従来のpre-commit（手動開発時）
uv run pre-commit run --all-files         # 全ファイルチェック
uv run pre-commit install                 # Git hooksインストール
```

### パッケージ操作
```bash
uv add package-name              # 本番依存関係追加
uv add --group dev package-name  # 開発依存関係追加
uv remove package-name           # パッケージ削除
```

## プロジェクト構造

```
src/python_project_2026/         # メインアプリケーションコード
├── __init__.py                  # パッケージ初期化・バージョン情報
├── main.py                      # CLIエントリーポイント（typer使用）
└── utils.py                     # 共通ユーティリティ関数

tests/                           # テストコード（pytest）
├── test_main.py                 # CLIアプリケーションテスト
└── test_utils.py                # ユーティリティテスト
```

## 設定ファイルの重要性

**pyproject.toml**: 全ツール設定の中心
- プロジェクトメタデータ、依存関係
- ruff（リンター/フォーマッター）設定
- pytest、mypy、coverage設定
- 依存関係グループ（dev、test、docs）

## 開発ワークフロー

### 新機能開発
1. テスト作成: `tests/test_*.py`
2. 実装: `src/python_project_2026/`
3. テスト実行: `uv run pytest`
4. コード品質: `uv run ruff check . && uv run ruff format .`
5. 型チェック: `uv run mypy`

### テスト駆動開発サイクル
```bash
# 1. テスト作成・実行（失敗確認）
uv run pytest tests/test_new_feature.py -v

# 2. 実装
# コードを書く

# 3. テスト実行（成功確認）
uv run pytest tests/test_new_feature.py -v

# 4. 品質チェック
uv run ruff check . && uv run ruff format . && uv run mypy
```

## コーディング規約

### インポート順序
1. 標準ライブラリ
2. サードパーティライブラリ
3. ローカルモジュール（`from . import`、`from python_project_2026 import`）

### 型ヒント
- Python 3.12+ の現代的な型ヒント使用
- `from typing import`より組み込み型を優先（`list[str]`、`dict[str, Any]`）
- 関数の引数と戻り値に型ヒント必須

### テスト
- `pytest`使用、classベーステスト推奨
- 各テストメソッドは`test_*`命名
- `@pytest.mark.parametrize`でデータ駆動テスト活用
- カバレッジ80%以上維持

## CI/CDとツール連携

### GitHub Actions
- マルチプラットフォーム（Linux、Windows、macOS）
- Python 3.12、3.13 サポート
- テスト・リンティング・型チェック・セキュリティ監査

### Claude Code hooks（AI統合品質管理）
- **ファイル変更時**: 自動的にコード品質チェックを提案
- **コミット時**: リンティング、フォーマット、型チェック、テスト実行
- **設定ファイル**: `.claude/settings.local.json` で hooks 設定管理

#### 利用可能なhooksスクリプト
```bash
# 統合品質チェック（推奨）
.claude/scripts/pre-commit-replacement.sh

# 個別チェック
.claude/scripts/code-quality.sh     # ruff + mypy
.claude/scripts/run-tests.sh        # pytest実行
.claude/scripts/file-checks.sh      # ファイル品質
```

#### hooks自動実行タイミング
- **PostToolUse**: Write/Edit/MultiEdit 後にファイルチェック提案
- **UserPromptSubmit**: 「コミット」関連プロンプトで品質チェック実行

### 従来のpre-commit（手動開発時）
- **Git hooks統合**: コミット前の自動品質チェック
- **設定ファイル**: `.pre-commit-config.yaml`
- **手動実行**: `uv run pre-commit run --all-files`

#### 使い分けの指針
- **Claude Code使用時**: Claude Code hooks（AI統合、リアルタイム提案）
- **手動開発時**: 従来のpre-commit（Git hooks、コミット時実行）
- **CI/CD**: 両方の設定をGitHub Actionsで活用

### Release Please（自動リリース管理）
- **Conventional Commits**に基づく自動バージョニング
- CHANGELOG.md自動生成・更新
- GitHub Releases自動作成
- PyPI自動公開（本番・テスト環境）

#### リリース関連コマンド
```bash
# リリース手動トリガー（通常は自動実行）
gh workflow run release-please.yml

# リリース状態確認
gh release list

# 特定リリース詳細
gh release view v1.0.0
```

#### Conventional Commits形式
```bash
# パッチバージョン更新 (0.1.0 → 0.1.1)
git commit -m "fix: バリデーションエラーを修正"

# マイナーバージョン更新 (0.1.0 → 0.2.0)
git commit -m "feat: 新しいCLIコマンド追加"

# メジャーバージョン更新 (0.1.0 → 1.0.0)
git commit -m "feat!: APIの破壊的変更"

# リリースに含まれないコミット
git commit -m "docs: README更新"
git commit -m "chore: 依存関係更新"
git commit -m "ci: CI設定改善"
```

## 依存関係管理

### 本番依存関係
- `pydantic`: データバリデーション
- `httpx`: 非同期HTTPクライアント
- `rich`: 美しいターミナル出力
- `typer`: CLIアプリケーション構築

### 開発依存関係
- `pytest`: テストフレームワーク + プラグイン
- `ruff`: 高速リンター・フォーマッター
- `mypy`: 静的型チェッカー
- `pre-commit`: Git フック管理

## 注意事項

- uvコマンドは必ず`uv run`プレフィックス使用（仮想環境自動活用）
- pyproject.toml直接編集せず`uv add`/`uv remove`使用
- 新しい依存関係追加時は適切なグループ（dev/test/docs）に分類
- テストは必ず`tests/`ディレクトリに配置、`test_*.py`命名
