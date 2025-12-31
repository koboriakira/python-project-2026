# Pull Request

## 概要
<!-- 変更内容を簡潔に説明してください -->

## 変更の種類
- [ ] 🐛 Bug fix (バグ修正)
- [ ] ✨ New feature (新機能)
- [ ] 💥 Breaking change (破壊的変更)
- [ ] 📚 Documentation (ドキュメント)
- [ ] 🧹 Code cleanup (コード整理)
- [ ] ⚡ Performance (パフォーマンス改善)
- [ ] 🔧 Configuration (設定変更)

## Conventional Commits
<!-- release-pleaseが自動的にバージョンとCHANGELOGを更新するため、適切なコミットメッセージを使用してください -->

### 例:
- `feat: ユーザー認証機能を追加` (minor version bump)
- `fix: バリデーションエラーを修正` (patch version bump)
- `feat!: APIレスポンス形式を変更` (major version bump)
- `docs: README更新`
- `chore: 依存関係更新`

## チェックリスト
- [ ] コードが正しくフォーマットされている (`uv run ruff format .`)
- [ ] リンティングエラーがない (`uv run ruff check .`)
- [ ] 型チェックが通る (`uv run mypy`)
- [ ] テストが通る (`uv run pytest`)
- [ ] 新機能にテストを追加した（該当する場合）
- [ ] ドキュメントを更新した（該当する場合）

## 関連Issue
<!-- 関連するIssueがある場合は記載してください -->
Fixes #(issue number)
