---
name: Security-First Development
description: セキュリティを重視したPython開発パターンとベストプラクティス
version: 1.0
tags: [security, owasp, authentication, validation, python]
---

# Security-First Development

セキュリティを最優先に考えたPython開発のためのパターンとベストプラクティス。

## 入力検証・サニタイゼーション

### Pydanticによる安全な入力検証
```python
from pydantic import BaseModel, validator, Field, EmailStr
from typing import Literal
import re

class UserRegistration(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        regex=r'^[a-zA-Z0-9_]+$'  # 英数字とアンダースコアのみ
    )
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal["user", "admin"] = "user"

    @validator('username')
    def sanitize_username(cls, v: str) -> str:
        # HTMLエスケープ
        return v.strip().lower()

    @validator('password')
    def validate_password_strength(cls, v: str) -> str:
        # パスワード強度チェック
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain special character')
        return v
```

### SQLインジェクション対策
```python
# ✅ 安全（パラメータ化クエリ）
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# ✅ 安全（ORMクエリビルダー）
async def search_users(db: AsyncSession, search_term: str) -> list[User]:
    stmt = select(User).where(
        User.username.ilike(f"%{search_term}%")  # SQLAlchemyが自動エスケープ
    )
    result = await db.execute(stmt)
    return result.scalars().all()

# ❌ 危険（SQLインジェクション脆弱性）
# def get_user_unsafe(db, user_input):
#     query = f"SELECT * FROM users WHERE name = '{user_input}'"
#     return db.execute(query)
```

## 認証・認可

### JWT認証の安全な実装
```python
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = timedelta(minutes=30)
        self.refresh_token_expire = timedelta(days=7)

    def create_access_token(
        self,
        subject: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        expire = datetime.now(timezone.utc) + (
            expires_delta or self.access_token_expire
        )

        payload = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access"
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": True}
            )
            return payload.get("sub")
        except jwt.PyJWTError:
            return None

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
```

### セキュアなセッション管理
```python
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db)
) -> User:
    # レート制限チェック
    client_ip = request.client.host
    if await is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many authentication attempts"
        )

    # トークン検証
    user_id = auth_service.verify_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    # ユーザー取得
    user = await get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return user
```

## データ保護

### 機密データの暗号化
```python
from cryptography.fernet import Fernet
import base64
import os

class DataEncryption:
    def __init__(self, key: Optional[bytes] = None):
        self.key = key or self._generate_key()
        self.fernet = Fernet(self.key)

    @staticmethod
    def _generate_key() -> bytes:
        return Fernet.generate_key()

    def encrypt(self, data: str) -> str:
        """文字列を暗号化してbase64文字列で返す"""
        encrypted_data = self.fernet.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """暗号化された文字列を復号化"""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted_data = self.fernet.decrypt(encrypted_bytes)
        return decrypted_data.decode()

# 使用例：機密データモデル
class SecureUser(BaseModel):
    id: int
    username: str
    email: str
    _encrypted_ssn: str = Field(alias="ssn")  # 社会保障番号（暗号化）

    @validator('_encrypted_ssn', pre=True)
    def encrypt_ssn(cls, v: str) -> str:
        encryption = DataEncryption()
        return encryption.encrypt(v)

    def get_ssn(self, encryption: DataEncryption) -> str:
        return encryption.decrypt(self._encrypted_ssn)
```

### 環境変数とシークレット管理
```python
from pydantic_settings import BaseSettings
from typing import Optional

class SecuritySettings(BaseSettings):
    # 必須のシークレット
    secret_key: str = Field(min_length=32)  # JWT用
    database_url: str

    # オプションのセキュリティ設定
    encryption_key: Optional[str] = None
    cors_origins: list[str] = ["http://localhost:3000"]

    # セキュリティヘッダー設定
    hsts_max_age: int = 31536000  # 1年
    csrf_token_secret: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # 本番環境では.envファイルを使わない
        env_ignore_empty = True

    @validator('secret_key')
    def validate_secret_key(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError('Secret key must be at least 32 characters')
        return v

# シークレット検証
def validate_secrets():
    """本番環境でのシークレット検証"""
    import secrets
    import string

    settings = SecuritySettings()

    # 弱いシークレットキー検出
    weak_patterns = ['secret', 'password', '123456', 'admin']
    if any(pattern in settings.secret_key.lower() for pattern in weak_patterns):
        raise ValueError("Weak secret key detected!")

    return settings
```

## API セキュリティ

### CORS設定
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

def setup_security_middleware(app: FastAPI, settings: SecuritySettings):
    # CORS設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
        expose_headers=["X-Request-ID"]
    )

    # 信頼できるホストのみ許可
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "*.example.com"]
    )
```

### セキュリティヘッダー
```python
from fastapi import Request, Response

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)

    # セキュリティヘッダー追加
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response
```

## ログ記録・監査

### セキュリティイベントログ
```python
import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any

class SecurityLogger:
    def __init__(self, logger_name: str = "security"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

        # 構造化ログ用フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_auth_attempt(
        self,
        username: str,
        success: bool,
        ip_address: str,
        user_agent: str = ""
    ):
        event = {
            "event_type": "authentication",
            "username": username,
            "success": success,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        level = logging.INFO if success else logging.WARNING
        self.logger.log(level, json.dumps(event))

    def log_permission_denied(
        self,
        user_id: int,
        resource: str,
        action: str,
        ip_address: str
    ):
        event = {
            "event_type": "permission_denied",
            "user_id": user_id,
            "resource": resource,
            "action": action,
            "ip_address": ip_address,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.logger.warning(json.dumps(event))
```

## 脆弱性検証

### 依存関係セキュリティチェック
```bash
# Safetyによる脆弱性チェック
uv add --group dev safety

# セキュリティ監査実行
uv run safety check

# Banditによる静的解析
uv add --group dev bandit
uv run bandit -r src/
```

### セキュリティテストパターン
```python
import pytest
from fastapi.testclient import TestClient

class TestSecurity:
    def test_sql_injection_protection(self, client: TestClient):
        """SQLインジェクション攻撃の防御テスト"""
        malicious_input = "'; DROP TABLE users; --"

        response = client.post("/users/search", json={
            "query": malicious_input
        })

        # 適切にエラーが返される、またはサニタイズされる
        assert response.status_code in [400, 422]

    def test_xss_protection(self, client: TestClient):
        """XSS攻撃の防御テスト"""
        malicious_script = "<script>alert('XSS')</script>"

        response = client.post("/comments", json={
            "content": malicious_script
        })

        # スクリプトタグがエスケープされている
        if response.status_code == 201:
            assert "<script>" not in response.json()["content"]

    def test_rate_limiting(self, client: TestClient):
        """レート制限テスト"""
        for _ in range(100):  # 大量リクエスト
            response = client.post("/auth/login", json={
                "username": "test",
                "password": "wrong"
            })

        # レート制限が発動
        assert response.status_code == 429
```

このスキルにより、セキュリティを最優先にした堅牢なPythonアプリケーションを開発できます。
