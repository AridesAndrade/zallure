from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
import sqlite3
import time
from pathlib import Path
from typing import Any

USERS_DB = Path(os.getenv("SESA_USERS_DB", Path(__file__).resolve().parent / "users.db"))
PASSWORD_ITERATIONS = 240_000
SESSION_HOURS = 8

DEFAULT_USERS = (
    ("master_01", "Master", "developer"),
    ("master_02", "Master", "developer"),
    ("gestor", "Gestor", "gestor"),
    ("secretaria", "Secretaria", "gestor"),
    ("auditor", "Auditor", "gestor"),
    ("dados", "Dados", "gestor"),
    ("estatistico", "Estatístico", "gestor"),
    ("relatorios", "Relatórios", "gestor"),
)


def _secret() -> str:
    return os.getenv("SESA_SESSION_SECRET") or os.getenv("SESA_MASTER_TOKEN", "")


def _connection() -> sqlite3.Connection:
    USERS_DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(USERS_DB)


def _hash_password(password: str, salt: bytes) -> str:
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    return digest.hex()


def init_users(default_password: str = "123456") -> None:
    with _connection() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL,
                environment TEXT NOT NULL DEFAULT 'gestor',
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        columns = {row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
        if "environment" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN environment TEXT NOT NULL DEFAULT 'gestor'")
        for username, role, environment in DEFAULT_USERS:
            salt = secrets.token_bytes(16)
            conn.execute(
                "INSERT OR IGNORE INTO users(username, role, environment, salt, password_hash) VALUES (?, ?, ?, ?, ?)",
                (username, role, environment, salt.hex(), _hash_password(default_password, salt)),
            )
        conn.execute("UPDATE users SET environment = 'developer' WHERE role = 'Master'")


def authenticate_user(username: str, password: str) -> dict[str, Any] | None:
    with _connection() as conn:
        row = conn.execute(
            "SELECT username, role, environment, salt, password_hash, active FROM users WHERE username = ?",
            (username.strip().lower(),),
        ).fetchone()
    if not row or not row[5]:
        return None
    salt = bytes.fromhex(row[3])
    valid = hmac.compare_digest(_hash_password(password, salt), row[4])
    if not valid:
        return None
    return {"username": row[0], "role": row[1], "environment": row[2]}


def issue_session(user: dict[str, Any]) -> str:
    secret = _secret()
    if not secret:
        raise RuntimeError("SESA_MASTER_TOKEN não configurado para assinar a sessão")
    expires = int(time.time()) + SESSION_HOURS * 3600
    payload = f"{user['username']}|{user['role']}|{user.get('environment', 'developer')}|{expires}".encode("utf-8")
    encoded = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
    signature = hmac.new(secret.encode("utf-8"), encoded.encode("ascii"), hashlib.sha256).hexdigest()
    return f"sesa.{encoded}.{signature}"


def verify_session(token: str, required_role: str | None = None) -> dict[str, Any] | None:
    secret = _secret()
    if not secret or not token.startswith("sesa."):
        return None
    try:
        _, encoded, signature = token.split(".", 2)
        expected = hmac.new(secret.encode("utf-8"), encoded.encode("ascii"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            return None
        padding = "=" * (-len(encoded) % 4)
        parts = base64.urlsafe_b64decode((encoded + padding).encode("ascii")).decode("utf-8").split("|")
        if len(parts) == 3:
            username, role, expires = parts
            environment = "developer" if role == "Master" else "gestor"
        else:
            username, role, environment, expires = parts
        if int(expires) < int(time.time()) or (required_role and role != required_role):
            return None
        return {"username": username, "role": role, "environment": environment}
    except (ValueError, TypeError, UnicodeError):
        return None


def create_user(username: str, role: str, environment: str = "gestor", password: str = "123456") -> dict[str, Any]:
    username = username.strip().lower()
    salt = secrets.token_bytes(16)
    with _connection() as conn:
        conn.execute(
            "INSERT INTO users(username, role, environment, salt, password_hash) VALUES (?, ?, ?, ?, ?)",
            (username, role, environment, salt.hex(), _hash_password(password, salt)),
        )
    return {"username": username, "role": role, "environment": environment, "active": True}


def set_user_password(username: str, password: str) -> None:
    salt = secrets.token_bytes(16)
    with _connection() as conn:
        updated = conn.execute(
            "UPDATE users SET salt = ?, password_hash = ? WHERE username = ?",
            (salt.hex(), _hash_password(password, salt), username.strip().lower()),
        ).rowcount
    if not updated:
        raise KeyError(username)


def set_user_active(username: str, active: bool) -> None:
    with _connection() as conn:
        updated = conn.execute(
            "UPDATE users SET active = ? WHERE username = ?",
            (1 if active else 0, username.strip().lower()),
        ).rowcount
    if not updated:
        raise KeyError(username)


def set_user_environment(username: str, environment: str) -> None:
    with _connection() as conn:
        updated = conn.execute("UPDATE users SET environment = ? WHERE username = ?", (environment, username.strip().lower())).rowcount
    if not updated:
        raise KeyError(username)


def set_user_role(username: str, role: str) -> None:
    username = username.strip().lower()
    role = role.strip()
    with _connection() as conn:
        row = conn.execute("SELECT role, active FROM users WHERE username = ?", (username,)).fetchone()
        if not row:
            raise KeyError(username)
        if row[0] == "Master" and role != "Master":
            masters = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'Master' AND active = 1").fetchone()[0]
            if masters <= 1:
                raise ValueError("Não é permitido retirar o perfil do último Master ativo")
        updated = conn.execute(
            "UPDATE users SET role = ?, environment = CASE WHEN ? = 'Master' THEN environment ELSE 'gestor' END WHERE username = ?",
            (role, role, username),
        ).rowcount
    if not updated:
        raise KeyError(username)


def rename_user(username: str, new_username: str) -> dict[str, str]:
    old_username = username.strip().lower()
    new_username = new_username.strip().lower()
    with _connection() as conn:
        updated = conn.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, old_username)).rowcount
    if not updated:
        raise KeyError(username)
    return {"username": new_username}


def delete_user(username: str) -> None:
    with _connection() as conn:
        row = conn.execute("SELECT role FROM users WHERE username = ?", (username.strip().lower(),)).fetchone()
        if not row:
            raise KeyError(username)
        if row[0] == "Master":
            masters = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'Master' AND active = 1").fetchone()[0]
            if masters <= 1:
                raise ValueError("Não é permitido excluir o último Master ativo")
        conn.execute("DELETE FROM users WHERE username = ?", (username.strip().lower(),))


def list_users() -> list[dict[str, Any]]:
    with _connection() as conn:
        rows = conn.execute("SELECT username, role, environment, active, created_at FROM users ORDER BY id").fetchall()
    return [{"username": row[0], "role": row[1], "environment": row[2], "active": bool(row[3]), "created_at": row[4]} for row in rows]
