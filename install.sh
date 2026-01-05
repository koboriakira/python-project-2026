#!/bin/bash
set -e

# プロジェクトテンプレート化スクリプト
# Usage: curl -fsSL https://raw.githubusercontent.com/koboriakira/python-project-2026/main/install.sh | sh -s {project-name}

PROJECT_NAME="$1"
TEMPLATE_NAME="python-project-2026"
TEMPLATE_PACKAGE="python_project_2026"

# バリデーション関数
validate_project_name() {
    if [[ -z "$PROJECT_NAME" ]]; then
        echo "❌ エラー: プロジェクト名が指定されていません"
        echo "使用方法: ./install.sh {project-name}"
        exit 1
    fi

    # プロジェクト名の形式チェック（ハイフン区切り）
    if [[ ! "$PROJECT_NAME" =~ ^[a-z][a-z0-9\-]*[a-z0-9]$ ]]; then
        echo "❌ エラー: 無効なプロジェクト名です"
        echo "形式: 小文字・数字・ハイフンのみ、先頭は文字、末尾は文字または数字"
        echo "例: my-project, data-processor, web-api"
        exit 1
    fi
}

# パッケージ名変換（ハイフン → アンダースコア）
convert_to_package_name() {
    echo "$PROJECT_NAME" | tr '-' '_'
}

# GitHubからテンプレートをダウンロード
download_template() {
    local target_dir="$PROJECT_NAME"
    local temp_dir="/tmp/python-project-2026-$$"
    local zip_file="$temp_dir/template.zip"
    local repo_url="https://github.com/koboriakira/python-project-2026/archive/refs/heads/main.zip"

    echo "📁 プロジェクトディレクトリを設定中: $target_dir"

    # ターゲットディレクトリが存在する場合の処理
    if [[ -d "$target_dir" ]]; then
        if [[ "$(ls -A "$target_dir" 2>/dev/null)" ]]; then
            echo "❌ エラー: ディレクトリ '$target_dir' は既に存在し、空ではありません"
            exit 1
        fi
    else
        mkdir -p "$target_dir"
    fi

    # 一時ディレクトリ作成
    mkdir -p "$temp_dir"

    # テンプレートをダウンロード
    echo "📋 テンプレートをダウンロード中..."

    # curlまたはwgetでダウンロード
    if command -v curl &> /dev/null; then
        curl -fsSL "$repo_url" -o "$zip_file"
    elif command -v wget &> /dev/null; then
        wget -q "$repo_url" -O "$zip_file"
    else
        echo "❌ エラー: curlまたはwgetが必要です。いずれかをインストールしてください。"
        rm -rf "$temp_dir"
        exit 1
    fi

    # unzipで解凍
    if ! command -v unzip &> /dev/null; then
        echo "❌ エラー: unzipコマンドが見つかりません。unzipをインストールしてください。"
        rm -rf "$temp_dir"
        exit 1
    fi

    echo "📦 ファイルを展開中..."
    unzip -q "$zip_file" -d "$temp_dir"

    # 解凍されたディレクトリからファイルをコピー
    # GitHubのzipは {repo}-{branch} という名前のディレクトリに解凍される
    echo "📦 ファイルをコピー中..."
    cp -r "$temp_dir/python-project-2026-main/." "$target_dir/"

    # .gitディレクトリとinstall.shを削除（不要なファイル除外）
    rm -rf "$target_dir/.git"
    rm -f "$target_dir/install.sh"

    # テンポラリディレクトリを削除
    rm -rf "$temp_dir"

    echo "✅ ファイルダウンロード完了"
}

# プロジェクト名を一括置換
replace_project_names() {
    local target_dir="$PROJECT_NAME"
    local package_name
    package_name=$(convert_to_package_name)

    echo "🔄 プロジェクト名を置換中: $TEMPLATE_NAME → $PROJECT_NAME"
    echo "📦 パッケージ名を置換中: $TEMPLATE_PACKAGE → $package_name"

    # テキストファイル内の文字列置換
    find "$target_dir" -type f \( -name "*.toml" -o -name "*.py" -o -name "*.md" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) \
        -exec sed -i.bak \
            -e "s/$TEMPLATE_NAME/$PROJECT_NAME/g" \
            -e "s/$TEMPLATE_PACKAGE/$package_name/g" \
            {} \;

    # バックアップファイルを削除
    find "$target_dir" -name "*.bak" -delete

    # ディレクトリ名を変更
    if [[ -d "$target_dir/src/$TEMPLATE_PACKAGE" ]]; then
        mv "$target_dir/src/$TEMPLATE_PACKAGE" "$target_dir/src/$package_name"
        echo "📁 パッケージディレクトリ名を変更: src/$TEMPLATE_PACKAGE → src/$package_name"
    fi

    echo "✅ 名前置換完了"
}

# 初期化処理
initialize_project() {
    local target_dir="$PROJECT_NAME"

    echo "🚀 プロジェクト初期化中..."

    cd "$target_dir"

    # uv環境セットアップ
    echo "📦 Python環境をセットアップ中..."
    if command -v uv &> /dev/null; then
        uv sync
        echo "✅ uv sync完了"
    else
        echo "⚠️  警告: uvが見つかりません。手動で 'uv sync' を実行してください"
    fi

    cd ..

    echo "✅ 初期化完了"
}

# メイン処理
main() {
    echo "🎯 Python Project 2026 テンプレートインストーラー"
    echo "=================================================="
    echo ""

    validate_project_name

    local package_name
    package_name=$(convert_to_package_name)

    echo "📋 設定情報:"
    echo "  プロジェクト名: $PROJECT_NAME"
    echo "  パッケージ名: $package_name"
    echo ""

    download_template
    replace_project_names
    initialize_project

    echo ""
    echo "🎉 プロジェクト作成完了!"
    echo ""
    echo "次のステップ:"
    echo "  1. cd $PROJECT_NAME"
    echo "  2. git init  # Git管理を開始する場合（オプショナル）"
    echo "  3. uv run pytest  # テスト実行"
    echo "  4. uv run $PROJECT_NAME --help  # アプリケーション確認"
    echo ""
    echo "開発の開始:"
    echo "  - src/$package_name/ でコードを編集"
    echo "  - tests/ でテストを追加"
    echo "  - uv run ruff check . でコード品質チェック"
    echo ""
    echo "Happy coding! 🚀"
}

# スクリプト実行
main
