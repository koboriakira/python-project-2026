#!/bin/bash
# Claude Code hooks - ファイル品質チェックスクリプト

set -e

echo "📋 Claude Code Hooks: ファイル品質チェック開始..."

# 変更されたファイルを取得
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM || true)

if [ -z "$CHANGED_FILES" ]; then
    echo "✅ 変更されたファイルなし - スキップ"
    exit 0
fi

echo "📝 変更されたファイル:"
echo "$CHANGED_FILES"

# 末尾の空白文字をチェック
echo "🔍 末尾の空白文字をチェック中..."
if echo "$CHANGED_FILES" | xargs grep -l '[[:space:]]$' 2>/dev/null; then
    echo "❌ 末尾の空白文字が見つかりました"
    echo "💡 修正するには: sed -i '' 's/[[:space:]]*$//' <ファイル名>"
    exit 1
fi

# ファイル末尾の改行をチェック
echo "🔚 ファイル末尾の改行をチェック中..."
for file in $CHANGED_FILES; do
    if [ -f "$file" ] && [ -s "$file" ] && [ "$(tail -c1 "$file" | wc -l)" -eq 0 ]; then
        echo "❌ ファイル末尾に改行がありません: $file"
        echo "💡 修正するには: echo >> $file"
        exit 1
    fi
done

# YAML/TOML/JSONファイルの構文チェック
echo "📄 設定ファイルの構文チェック中..."

# YAML ファイルチェック
YAML_FILES=$(echo "$CHANGED_FILES" | grep '\\.ya\\?ml$' || true)
if [ -n "$YAML_FILES" ]; then
    echo "$YAML_FILES" | while read -r file; do
        if ! python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
            echo "❌ YAML構文エラー: $file"
            exit 1
        fi
    done
fi

# TOML ファイルチェック
TOML_FILES=$(echo "$CHANGED_FILES" | grep '\\.toml$' || true)
if [ -n "$TOML_FILES" ]; then
    echo "$TOML_FILES" | while read -r file; do
        if ! python3 -c "import tomllib; tomllib.load(open('$file', 'rb'))" 2>/dev/null; then
            echo "❌ TOML構文エラー: $file"
            exit 1
        fi
    done
fi

# JSON ファイルチェック
JSON_FILES=$(echo "$CHANGED_FILES" | grep '\\.json$' || true)
if [ -n "$JSON_FILES" ]; then
    echo "$JSON_FILES" | while read -r file; do
        if ! python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
            echo "❌ JSON構文エラー: $file"
            exit 1
        fi
    done
fi

echo "✅ すべてのファイル品質チェックが完了しました"
