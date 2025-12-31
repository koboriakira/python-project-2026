#!/bin/bash
# Claude Code hooks - コード品質チェックスクリプト

set -e

echo "🔧 Claude Code Hooks: コード品質チェック開始..."

# 変更されたPythonファイルのみをチェック
CHANGED_PY_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

if [ -z "$CHANGED_PY_FILES" ]; then
    echo "✅ Python ファイルの変更なし - スキップ"
    exit 0
fi

echo "📝 変更されたファイル:"
echo "$CHANGED_PY_FILES"

# ruffによるリンティングとフォーマット
echo "🦀 Ruff チェック実行中..."
if ! uv run ruff check $CHANGED_PY_FILES; then
    echo "❌ Ruff リンティングエラーが発見されました"
    echo "💡 修正するには: uv run ruff check --fix ."
    exit 1
fi

echo "🎨 Ruff フォーマット実行中..."
uv run ruff format $CHANGED_PY_FILES

# mypyによる型チェック
echo "🔍 MyPy 型チェック実行中..."
if ! uv run mypy $CHANGED_PY_FILES; then
    echo "❌ 型チェックエラーが発見されました"
    echo "💡 型ヒントを確認してください"
    exit 1
fi

echo "✅ すべてのコード品質チェックが完了しました"
