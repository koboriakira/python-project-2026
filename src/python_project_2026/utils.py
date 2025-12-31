"""ユーティリティ関数"""

from pathlib import Path
from typing import Any


def ensure_directory(path: Path) -> Path:
    """ディレクトリが存在することを確認し、必要に応じて作成"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_size(size_bytes: int) -> str:
    """バイト数を人間が読みやすい形式に変換"""
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size_float = float(size_bytes)
    while size_float >= 1024.0 and i < len(size_names) - 1:
        size_float /= 1024.0
        i += 1

    return f"{size_float:.1f}{size_names[i]}"


def safe_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """辞書から安全にキーを取得"""
    return data.get(key, default)
