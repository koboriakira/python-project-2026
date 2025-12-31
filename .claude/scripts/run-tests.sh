#!/bin/bash
# Claude Code hooks - テスト実行スクリプト

set -e

echo "🧪 Claude Code Hooks: テスト実行開始..."

# 関連するテストファイルがあるかチェック
CHANGED_PY_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

if [ -z "$CHANGED_PY_FILES" ]; then
    echo "✅ Python ファイルの変更なし - スキップ"
    exit 0
fi

# 変更されたファイルに対応するテストを実行
echo "🎯 関連するテストを実行中..."

# src/ の変更があった場合は全テスト実行
if echo "$CHANGED_PY_FILES" | grep -q "src/"; then
    echo "📦 src/ の変更を検出 - 全テスト実行"
    if ! uv run pytest -v; then
        echo "❌ テストが失敗しました"
        exit 1
    fi
else
    # tests/ の変更のみの場合は変更されたテストファイルのみ実行
    CHANGED_TEST_FILES=$(echo "$CHANGED_PY_FILES" | grep "test_" || true)
    if [ -n "$CHANGED_TEST_FILES" ]; then
        echo "🧪 変更されたテストファイルを実行: $CHANGED_TEST_FILES"
        if ! uv run pytest -v $CHANGED_TEST_FILES; then
            echo "❌ テストが失敗しました"
            exit 1
        fi
    else
        echo "ℹ️  テストファイルの変更なし"
    fi
fi

echo "✅ すべてのテストが成功しました"
