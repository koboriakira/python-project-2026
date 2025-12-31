---
description: "現在のブランチから新しいPull Requestを作成"
argument-hint: "[title] [description]"
allowed-tools: Bash(git:*), Bash(gh:*)
model: inherit
---

# Pull Request作成コマンド

現在のブランチからmainブランチへのPull Requestを作成します。

## 実行内容

1. **Git状態確認**
   - 現在のブランチ確認
   - 変更内容の表示
   - コミット履歴の確認

2. **品質チェック実行**
   - Claude Code hooks統合チェック実行
   - テスト、リンティング、型チェック
   - 問題がある場合は警告表示

3. **PR作成**
   - GitHub CLI使用
   - テンプレート適用
   - 自動ラベル付与

## 使用例

```bash
/create-pr "新機能: ユーザー認証機能追加"
/create-pr "バグ修正: CSV出力エラー" "詳細な説明をここに記載"
```

## 実装

```bash
#!/bin/bash
set -e

TITLE="$1"
DESCRIPTION="${2:-}"

echo "🚀 Pull Request作成プロセス開始..."

# 1. Git状態確認
echo "📍 現在の状態確認..."
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo "❌ エラー: mainブランチからPRは作成できません"
    exit 1
fi

echo "📋 ブランチ: $CURRENT_BRANCH"

# 2. 変更内容確認
echo "📂 変更内容:"
git diff --name-only origin/main...HEAD | head -10

# 3. コミット履歴
echo "📝 コミット履歴:"
git log origin/main...HEAD --oneline | head -5

# 4. 品質チェック
echo ""
echo "🔍 品質チェック実行中..."
if [ -f ".claude/scripts/pre-commit-replacement.sh" ]; then
    .claude/scripts/pre-commit-replacement.sh
else
    echo "⚠️ 品質チェックスクリプトが見つかりません"
fi

# 5. リモートプッシュ（必要に応じて）
echo ""
echo "📤 リモートブランチ確認..."
if ! git ls-remote --heads origin "$CURRENT_BRANCH" | grep -q "$CURRENT_BRANCH"; then
    echo "🔄 リモートブランチを作成中..."
    git push -u origin "$CURRENT_BRANCH"
fi

# 6. PR作成
echo ""
echo "🎯 Pull Request作成中..."

PR_BODY="## 概要
$DESCRIPTION

## 変更内容
$(git diff --name-only origin/main...HEAD | sed 's/^/- /')

## テストプラン
- [ ] 既存テストの通過確認
- [ ] 新機能のテスト実行
- [ ] 品質チェック（ruff, mypy）の通過

## チェックリスト
- [ ] コードレビュー完了
- [ ] テスト追加・更新
- [ ] ドキュメント更新
- [ ] CHANGELOG.md更新（必要に応じて）

🤖 Generated with [Claude Code](https://claude.ai/code)"

gh pr create \
  --title "$TITLE" \
  --body "$PR_BODY" \
  --base main \
  --head "$CURRENT_BRANCH"

echo ""
echo "✅ Pull Request作成完了!"
echo "🔗 URL: $(gh pr view --web 2>/dev/null || echo 'GitHub上で確認してください')"
```
