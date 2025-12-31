---
name: Python Modern Practices
description: Python 3.12+の最新機能とベストプラクティスを活用したコード実装スキル
version: 1.0
tags: [python, modern, typing, performance]
---

# Python 3.12+ Modern Practices

Python 3.12以降の最新機能を活用した現代的な開発パターンを提供します。

## 型ヒントの最適化

### 現代的な型ヒント
```python
# ❌ 古いスタイル
from typing import List, Dict, Optional, Union

def process_data(items: List[str]) -> Dict[str, Optional[int]]:
    return {}

# ✅ 現代的スタイル（Python 3.9+）
def process_data(items: list[str]) -> dict[str, int | None]:
    return {}
```

### Generic型の活用
```python
from typing import TypeVar, Generic, Protocol

T = TypeVar('T')

class Repository(Generic[T], Protocol):
    def save(self, entity: T) -> T: ...
    def find_by_id(self, id: int) -> T | None: ...

# 具体的な実装
class UserRepository(Repository[User]):
    def save(self, entity: User) -> User:
        # 実装
        return entity
```

### 新しい型機能（Python 3.12+）
```python
# type statement
type Vector = list[float]
type UserId = int
type UserData = dict[str, str | int | bool]

# Generic type aliases
type Repository[T] = dict[str, T]
type Result[T, E] = T | Exception
```

## パフォーマンス最適化

### f-string vs format vs %
```python
# ✅ 最速（f-string推奨）
name = "Alice"
age = 30
message = f"Hello, {name}! You are {age} years old."

# ❌ 遅い
message = "Hello, {}! You are {} years old.".format(name, age)
message = "Hello, %s! You are %d years old." % (name, age)
```

### リスト内包表記の最適化
```python
# ✅ 効率的
numbers = [x**2 for x in range(1000) if x % 2 == 0]

# ✅ メモリ効率（ジェネレータ）
numbers = (x**2 for x in range(1000) if x % 2 == 0)

# ❌ 非効率
numbers = []
for x in range(1000):
    if x % 2 == 0:
        numbers.append(x**2)
```

### dataclassesの活用
```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass(frozen=True, slots=True)  # Python 3.10+
class User:
    id: int
    name: str
    email: str
    tags: list[str] = field(default_factory=list)

    # クラス変数
    DEFAULT_ROLE: ClassVar[str] = "user"

    def __post_init__(self) -> None:
        if not self.email.count("@") == 1:
            raise ValueError("Invalid email format")
```

## エラーハンドリング現代化

### Exception Groups（Python 3.11+）
```python
def validate_user_data(data: dict[str, str]) -> None:
    errors = []

    if not data.get("name"):
        errors.append(ValueError("Name is required"))

    if not data.get("email") or "@" not in data["email"]:
        errors.append(ValueError("Valid email is required"))

    if errors:
        raise ExceptionGroup("Validation failed", errors)

# 使用例
try:
    validate_user_data({"name": "", "email": "invalid"})
except* ValueError as eg:
    for error in eg.exceptions:
        print(f"Validation error: {error}")
```

### パターンマッチング（Python 3.10+）
```python
def process_api_response(response: dict) -> str:
    match response:
        case {"status": "success", "data": data}:
            return f"Success: {data}"
        case {"status": "error", "message": msg}:
            return f"Error: {msg}"
        case {"status": "pending"}:
            return "Processing..."
        case _:
            return "Unknown response format"
```

## 非同期プログラミング強化

### async/await最適化
```python
import asyncio
import aiohttp
from typing import AsyncIterator

async def fetch_data(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()

# AsyncIterator活用
async def process_large_dataset() -> AsyncIterator[dict]:
    for i in range(1000000):
        # 非同期処理
        data = await fetch_record(i)
        yield data
```

## セキュリティ強化パターン

### 安全な入力検証
```python
from pydantic import BaseModel, validator, Field
from typing import Annotated

class UserInput(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    email: Annotated[str, Field(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')]
    age: Annotated[int, Field(ge=0, le=150)]

    @validator('name')
    def sanitize_name(cls, v: str) -> str:
        return v.strip().title()
```

### 環境変数管理
```python
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

## テスト現代化

### pytest現代的活用
```python
import pytest
from typing import Any

@pytest.mark.parametrize(
    "input_data,expected",
    [
        ({"name": "Alice", "age": 30}, True),
        ({"name": "", "age": 30}, False),
        ({"name": "Bob", "age": -1}, False),
    ],
    ids=["valid_data", "empty_name", "invalid_age"]
)
def test_user_validation(input_data: dict[str, Any], expected: bool) -> None:
    result = validate_user(input_data)
    assert result == expected

# Fixture活用
@pytest.fixture
async def db_session() -> AsyncIterator[Session]:
    async with create_async_session() as session:
        yield session
        await session.rollback()
```

このスキルにより、Development Workflow Agentが最新のPythonベストプラクティスを適用した高品質なコードを生成できます。
