---
description: "バグ報告、機能要求、技術的課題のIssueを作成"
argument-hint: "[type] [title] [description]"
allowed-tools: Bash(gh:*), Read(*)
model: inherit
---

# Issue作成コマンド

プロジェクトの課題や要求をGitHub Issueとして作成します。

## 対応タイプ

- **bug**: バグ報告
- **feature**: 機能要求
- **tech-debt**: 技術的負債
- **security**: セキュリティ問題

## 使用例

```bash
/create-issue bug "テスト実行でメモリリークが発生"
/create-issue feature "APIレート制限機能" "詳細な要件説明"
/create-issue tech-debt "依存関係の更新"
/create-issue security "脆弱な依存関係の修正"
```

## 実装

```bash
#!/bin/bash
set -e

TYPE="$1"
TITLE="$2"
DESCRIPTION="${3:-}"

echo "🎯 GitHub Issue作成プロセス開始..."

# タイプ検証
case "$TYPE" in
    "bug"|"feature"|"tech-debt"|"security")
        echo "📋 タイプ: $TYPE"
        ;;
    *)
        echo "❌ エラー: 無効なタイプです"
        echo "利用可能: bug, feature, tech-debt, security"
        exit 1
        ;;
esac

# ラベル設定
case "$TYPE" in
    "bug")
        LABELS="bug,priority:high"
        ;;
    "feature")
        LABELS="enhancement,priority:medium"
        ;;
    "tech-debt")
        LABELS="technical-debt,priority:low"
        ;;
    "security")
        LABELS="security,priority:critical"
        ;;
esac

# テンプレート生成
case "$TYPE" in
    "bug")
        TEMPLATE="## 🐛 バグ報告

### 問題の概要
$DESCRIPTION

### 再現手順
1.
2.
3.

### 期待される動作


### 実際の動作


### 環境情報
- OS: $(uname -s)
- Python: $(python --version 2>/dev/null || echo 'N/A')
- uv: $(uv --version 2>/dev/null || echo 'N/A')

### 追加情報
"
        ;;
    "feature")
        TEMPLATE="## 🚀 機能要求

### 機能の概要
$DESCRIPTION

### 動機・背景


### 提案される解決方法


### 代替案


### 追加コンテキスト
"
        ;;
    "tech-debt")
        TEMPLATE="## 🔧 技術的負債

### 問題の詳細
$DESCRIPTION

### 現在の影響


### 提案される改善


### 期待される効果


### 実装計画
- [ ] 調査・分析
- [ ] 実装
- [ ] テスト
- [ ] ドキュメント更新
"
        ;;
    "security")
        TEMPLATE="## 🔒 セキュリティ問題

### 問題の概要
$DESCRIPTION

### 影響度評価


### 推奨対応


### 緊急度


### 参考情報
"
        ;;
esac

TEMPLATE="$TEMPLATE

---
🤖 Created with [Claude Code](https://claude.ai/code)"

# Issue作成
echo ""
echo "📝 Issue作成中..."

gh issue create \
  --title "$TITLE" \
  --body "$TEMPLATE" \
  --label "$LABELS"

echo ""
echo "✅ Issue作成完了!"
echo "🔗 URL: $(gh issue list --limit 1 --json url --jq '.[0].url')"
```
