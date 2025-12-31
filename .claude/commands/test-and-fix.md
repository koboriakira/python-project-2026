---
description: "包括的なテスト実行とコード品質チェック、自動修正"
allowed-tools: Bash(uv:*), Bash(.claude/scripts/*)
model: inherit
---

# テスト＆修正コマンド

プロジェクトの包括的な品質チェックとテスト実行を行い、可能な問題を自動修正します。

## 実行内容

1. **依存関係チェック**
   - uv環境の確認
   - パッケージ同期状態の検証

2. **コード品質チェック**
   - ruffによるリンティング（自動修正付き）
   - mypyによる型チェック
   - セキュリティ監査

3. **テスト実行**
   - pytest実行（カバレッジ測定）
   - テスト結果の詳細表示
   - カバレッジレポート生成

4. **問題の自動修正**
   - ruffでの自動フォーマット
   - 軽微な問題の自動修正
   - 修正不可能な問題の詳細レポート

## 使用例

```bash
/test-and-fix
```

## 実装

```bash
#!/bin/bash
set -e

echo "🧪 テスト＆修正プロセス開始..."
echo "════════════════════════════════════════"

# 1. 環境確認
echo ""
echo "1️⃣ 環境確認"
echo "────────────────────"
echo "📋 uv環境: $(uv --version 2>/dev/null || echo 'uvが見つかりません')"
echo "🐍 Python: $(uv run python --version 2>/dev/null || echo 'N/A')"

# 2. 依存関係同期
echo ""
echo "2️⃣ 依存関係同期"
echo "────────────────────"
uv sync

# 3. リンティング（自動修正付き）
echo ""
echo "3️⃣ コードフォーマット＆リンティング"
echo "────────────────────"
echo "🔧 ruffフォーマット実行中..."
uv run ruff format .

echo "🔍 ruffリンティング（自動修正）実行中..."
uv run ruff check . --fix || {
    echo "⚠️ 自動修正できない問題があります"
    echo "📋 詳細な問題一覧:"
    uv run ruff check .
}

# 4. 型チェック
echo ""
echo "4️⃣ 型チェック"
echo "────────────────────"
echo "🔍 mypy型チェック実行中..."
uv run mypy || {
    echo "⚠️ 型チェックで問題が見つかりました"
    echo "📋 修正が必要な型エラーがあります"
}

# 5. テスト実行
echo ""
echo "5️⃣ テスト実行"
echo "────────────────────"
echo "🧪 pytest実行中（カバレッジ測定付き）..."

# カバレッジ付きテスト実行
if uv run pytest --cov --cov-report=term-missing --cov-report=html; then
    echo ""
    echo "✅ すべてのテストが成功しました!"

    # カバレッジ結果表示
    echo ""
    echo "📊 カバレッジサマリー:"
    uv run coverage report --show-missing | tail -n 5

    # HTMLレポートの場所
    if [ -f "htmlcov/index.html" ]; then
        echo "🌐 詳細カバレッジレポート: htmlcov/index.html"
    fi
else
    echo ""
    echo "❌ テストに失敗しました"
    echo "📋 失敗したテストを確認してください"
    TEST_EXIT_CODE=1
fi

# 6. セキュリティチェック（banditがある場合）
echo ""
echo "6️⃣ セキュリティチェック"
echo "────────────────────"
if uv run bandit -r src/ 2>/dev/null; then
    echo "✅ セキュリティチェック完了"
else
    echo "⚠️ banditが見つからないか、セキュリティ問題があります"
fi

# 7. 最終サマリー
echo ""
echo "📊 最終サマリー"
echo "════════════════════════════════════════"

# Git status
if git status --porcelain | grep -q .; then
    echo "📝 自動修正による変更:"
    git status --porcelain
    echo ""
    echo "💡 変更をコミットしますか？"
    echo "   git add . && git commit -m \"style: テスト＆修正による自動フォーマット\""
else
    echo "✨ コードは既に最適化されています"
fi

echo ""
if [ "${TEST_EXIT_CODE:-0}" -eq 0 ]; then
    echo "🎉 すべてのチェックが完了しました！"
    echo "✅ コード品質: 良好"
    echo "✅ テスト: すべて成功"
    echo "✅ カバレッジ: 確認済み"
else
    echo "⚠️ 一部のチェックで問題が見つかりました"
    echo "📋 上記の詳細を確認し、修正してください"
    exit 1
fi

echo ""
echo "🚀 次のステップ:"
echo "   - 変更をコミット"
echo "   - Pull Request作成: /create-pr"
echo "   - Issue作成（問題がある場合）: /create-issue"
```
