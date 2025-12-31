#!/bin/bash
# Claude Code hooks - pre-commitの完全な代替スクリプト

set -e

echo "🚀 Claude Code Hooks: 統合品質チェック開始..."
echo "📍 Git staged状態をチェック中..."

# Gitリポジトリかチェック
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Gitリポジトリではありません"
    exit 1
fi

# 変更されたファイルを取得
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM || true)
ALL_CHANGED_FILES=$(git diff --name-only || true)

if [ -z "$STAGED_FILES" ] && [ -z "$ALL_CHANGED_FILES" ]; then
    echo "✅ 変更されたファイルがありません"
    exit 0
fi

echo "📂 処理対象ファイル:"
if [ -n "$STAGED_FILES" ]; then
    echo "  Staged: $(echo "$STAGED_FILES" | wc -l) files"
    echo "$STAGED_FILES" | head -5
    [ $(echo "$STAGED_FILES" | wc -l) -gt 5 ] && echo "  ..."
fi

if [ -n "$ALL_CHANGED_FILES" ]; then
    echo "  Modified: $(echo "$ALL_CHANGED_FILES" | wc -l) files"
    echo "$ALL_CHANGED_FILES" | head -5
    [ $(echo "$ALL_CHANGED_FILES" | wc -l) -gt 5 ] && echo "  ..."
fi

# 1. ファイル品質チェック
echo ""
echo "1️⃣ ファイル品質チェック"
.claude/scripts/file-checks.sh

# 2. Pythonコード品質チェック
PYTHON_FILES=$(echo "$STAGED_FILES $ALL_CHANGED_FILES" | tr ' ' '\n' | grep '\.py$' | sort -u || true)
if [ -n "$PYTHON_FILES" ]; then
    echo ""
    echo "2️⃣ Python コード品質チェック"
    .claude/scripts/code-quality.sh
    
    echo ""
    echo "3️⃣ テスト実行"
    .claude/scripts/run-tests.sh
else
    echo ""
    echo "2️⃣ Python ファイルなし - コード品質チェックとテストをスキップ"
fi

echo ""
echo "✨ すべてのClaude Code Hooks チェックが完了しました！"
echo "🎯 pre-commitの機能を完全に置き換えました"