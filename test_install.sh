#!/bin/bash

# install.shのテストスクリプト
set -e

TEST_DIR="test_installation"
TEST_PROJECT="my-test-project"

cleanup() {
    echo "🧹 クリーンアップ中..."
    rm -rf "$TEST_DIR"
}

# テスト前にクリーンアップ
trap cleanup EXIT

test_basic_installation() {
    echo "🧪 基本インストールテスト開始"

    # テストディレクトリ作成
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"

    # install.shをコピー
    cp ../install.sh .
    cp -r ../src .
    cp -r ../tests .
    cp ../pyproject.toml .
    cp ../LICENSE .
    cp ../README.md .
    cp -r ../.claude .
    mkdir -p .github/workflows
    cp -r ../.github/workflows/* .github/workflows/ || true

    # インストール実行（uv syncなしバージョン）
    echo "📦 インストール実行: ./install.sh $TEST_PROJECT"

    # install.shを編集してuv syncをスキップ
    sed -i.bak 's/uv sync/echo "✅ uv sync スキップ（テストモード）"/' install.sh

    ./install.sh "$TEST_PROJECT"

    # 結果検証
    cd "$TEST_PROJECT"

    echo "✅ ファイル存在チェック"
    [[ -f "pyproject.toml" ]] || { echo "❌ pyproject.toml missing"; exit 1; }
    [[ -d "src/my_test_project" ]] || { echo "❌ src/my_test_project missing"; exit 1; }
    [[ -f "src/my_test_project/__init__.py" ]] || { echo "❌ __init__.py missing"; exit 1; }

    echo "✅ プロジェクト名置換チェック"
    if grep -q "python-project-2026" pyproject.toml; then
        echo "❌ プロジェクト名が置換されていません"
        exit 1
    fi

    if grep -q "my-test-project" pyproject.toml; then
        echo "✅ プロジェクト名置換完了"
    else
        echo "❌ 新しいプロジェクト名が見つかりません"
        exit 1
    fi

    echo "✅ パッケージ名置換チェック"
    if grep -q "python_project_2026" pyproject.toml; then
        echo "❌ パッケージ名が置換されていません"
        exit 1
    fi

    if grep -q "my_test_project" pyproject.toml; then
        echo "✅ パッケージ名置換完了"
    else
        echo "❌ 新しいパッケージ名が見つかりません"
        exit 1
    fi

    echo "✅ .gitディレクトリ除外チェック"
    # テンプレートの.gitディレクトリが存在しないことを確認
    if [[ -d ".git" ]]; then
        echo "❌ .gitディレクトリがコピーされています"
        exit 1
    fi
    echo "✅ .gitディレクトリは正しく除外されました"

    cd ../..
    echo "🎉 基本インストールテスト完了"
}

test_error_cases() {
    echo "🧪 エラーケーステスト開始"

    cd "$TEST_DIR"

    # 引数なしテスト
    echo "📋 引数なしエラーテスト"
    if ./install.sh 2>/dev/null; then
        echo "❌ 引数なしでエラーになるべき"
        exit 1
    else
        echo "✅ 引数なしエラー正常"
    fi

    # 無効な名前テスト
    echo "📋 無効な名前エラーテスト"
    if ./install.sh "INVALID-Name" 2>/dev/null; then
        echo "❌ 無効な名前でエラーになるべき"
        exit 1
    else
        echo "✅ 無効な名前エラー正常"
    fi

    cd ..
    echo "🎉 エラーケーステスト完了"
}

main() {
    echo "🚀 install.sh テスト実行開始"
    echo "=============================="

    test_basic_installation
    test_error_cases

    echo ""
    echo "🎉 すべてのテスト完了!"
    echo "install.sh は正常に動作します。"
}

main
