from __future__ import annotations

import hashlib
import hmac
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from auth import (
    authenticate_user,
    create_user,
    delete_user,
    init_users,
    issue_session,
    list_users,
    rename_user,
    set_user_active,
    set_user_environment,
    set_user_password,
    verify_session,
)

try:
    from crewai import Agent, Crew, Process, Task
except ImportError:  # The backend remains inspectable before dependencies are installed.
    Agent = Crew = Process = Task = None

ROOT = Path(__file__).resolve().parent
DRIVE_ROOT = Path(os.getenv("SESA_DRIVE_ROOT", r"G:\Meu Drive\Projeto_SESA"))
DRIVE_FOLDERS = {
    "knowledge": "01_Conhecimento_Aprovado",
    "training": "02_Preparacao_e_Treinamento",
    "production": "03_Producao_Autorizada",
    "audit": "04_Auditoria",
    "master": "05_Administracao_Master",
}
STATE_FILE = Path(os.getenv("SESA_STATUS_FILE", ROOT / "status.json"))
AUDIT_DB = Path(os.getenv("SESA_AUDIT_DB", ROOT / "audit.db"))
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

app = FastAPI(title="SESA — Agente Gestor", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("SESA_ALLOWED_ORIGINS", "*").split(",")],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

DEFAULT_STATUS: dict[str, Any] = {
    "project": "SESA",
    "updated_at": None,
    "mode": "developer",
    "connection": "backend-online",
    "stages": {
        "gestor": {"label": "Em implementação", "state": "active", "progress": 35},
        "juridico": {"label": "Piloto preparado", "state": "active", "progress": 20},
        "dados": {"label": "Planejado", "state": "planned", "progress": 0},
        "estatistico": {"label": "Planejado", "state": "planned", "progress": 0},
        "relatorios": {"label": "Planejado", "state": "planned", "progress": 0},
        "servidor_publico": {"label": "Preparação", "state": "planned", "progress": 0},
        "bases": {"label": "Em definição", "state": "source", "progress": 10},
    },
}


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    mode: str = Field(default="developer", pattern="^(developer|operational)$")


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80, pattern=r"^[a-zA-Z0-9_.-]+$")
    role: str = Field(min_length=2, max_length=40)
    environment: str = Field(default="gestor", pattern="^(gestor|developer)$")
    password: str = Field(min_length=1, max_length=200)


class UserRenameRequest(BaseModel):
    new_username: str = Field(min_length=3, max_length=80, pattern=r"^[a-zA-Z0-9_.-]+$")


class UserEnvironmentRequest(BaseModel):
    environment: str = Field(pattern="^(gestor|developer)$")


class UserPasswordRequest(BaseModel):
    password: str = Field(min_length=1, max_length=200)


class UserStatusRequest(BaseModel):
    active: bool


class StatusUpdate(BaseModel):
    node: str = Field(min_length=1, max_length=60)
    label: str = Field(min_length=1, max_length=120)
    state: str = Field(pattern="^(planned|active|done|blocked|source)$")
    progress: int = Field(ge=0, le=100)
    note: str = Field(default="", max_length=500)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_status() -> dict[str, Any]:
    if not STATE_FILE.exists():
        state = {**DEFAULT_STATUS, "updated_at": now_iso()}
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return state
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def write_status(status: dict[str, Any]) -> None:
    status["updated_at"] = now_iso()
    STATE_FILE.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")


def drive_overview() -> dict[str, Any]:
    folders: dict[str, Any] = {}
    for key, folder_name in DRIVE_FOLDERS.items():
        folder = DRIVE_ROOT / folder_name
        if not folder.exists():
            folders[key] = {"name": folder_name, "exists": False, "files": 0, "directories": 0}
            continue
        files = [item for item in folder.rglob("*") if item.is_file()]
        directories = [item for item in folder.rglob("*") if item.is_dir()]
        folders[key] = {
            "name": folder_name,
            "exists": True,
            "files": len(files),
            "directories": len(directories),
            "last_modified": max((item.stat().st_mtime for item in files), default=None),
        }
    return {"root": str(DRIVE_ROOT), "exists": DRIVE_ROOT.exists(), "folders": folders}


def init_audit() -> None:
    with sqlite3.connect(AUDIT_DB) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY, created_at TEXT, action TEXT, actor TEXT, payload TEXT)"
        )


def audit(action: str, actor: str, payload: dict[str, Any]) -> None:
    init_audit()
    with sqlite3.connect(AUDIT_DB) as conn:
        conn.execute(
            "INSERT INTO audit_log(created_at, action, actor, payload) VALUES (?, ?, ?, ?)",
            (now_iso(), action, actor, json.dumps(payload, ensure_ascii=False)),
        )


def require_master(authorization: str | None = Header(default=None)) -> str:
    configured = os.getenv("SESA_MASTER_TOKEN")
    if not configured:
        raise HTTPException(status_code=503, detail="SESA_MASTER_TOKEN não configurado no backend")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Autorização Master necessária")
    supplied = authorization.removeprefix("Bearer ").strip()
    direct_valid = hmac.compare_digest(hashlib.sha256(supplied.encode()).digest(), hashlib.sha256(configured.encode()).digest())
    session_user = verify_session(supplied, required_role="Master")
    if not direct_valid and not session_user:
        raise HTTPException(status_code=403, detail="Token Master inválido")
    return session_user["username"] if session_user else "master"


def build_developer_context() -> str:
    return (
        "Você é o Agente Gestor do SESA no modo Desenvolvedor. "
        "Atue como especialista em Python, CrewAI, GitHub, APIs, LLMs e arquitetura multiagente. "
        "Somente usuários Master podem usar este modo. Explique mudanças com precisão, não invente execução "
        "e nunca revele segredos, tokens ou variáveis de ambiente. Ao concluir uma alteração, indique o nó do mapa "
        "que deve ser atualizado e o motivo."
    )


def build_crewai_developer_agent() -> Any:
    """Creates the Master developer agent when CrewAI is installed and enabled."""
    if not all((Agent, Crew, Task)) or os.getenv("SESA_USE_CREWAI", "true").lower() != "true":
        return None
    return Agent(
        role="Agente Gestor — Desenvolvedor SESA",
        goal="Evoluir com segurança a arquitetura Python/CrewAI do SESA sob comando de um usuário Master.",
        backstory=build_developer_context(),
        verbose=False,
        allow_delegation=False,
    )


def process_events(mode: str, groq_enabled: bool) -> list[dict[str, str]]:
    events = [
        {"key": "receber", "label": "Solicitação recebida pelo SESA"},
        {"key": "compreender", "label": "Agente Gestor validou o modo de atendimento"},
        {"key": "consultar", "label": "Contexto técnico preparado para a análise"},
    ]
    if groq_enabled:
        events.append({"key": "consultar", "label": "Solicitando resposta à LLM configurada"})
    else:
        events.append({"key": "consultar", "label": "Modo local ativo; LLM não configurada"})
    events.append({"key": "responder", "label": "Orientação do SESA preparada"})
    return events


def groq_chat(message: str, mode: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Modo local ativo: GROQ_API_KEY ainda não configurada. Posso analisar a arquitetura e preparar o código, mas a resposta da LLM ficará desativada até a configuração segura do backend."
    payload = {
        "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": build_developer_context() if mode == "developer" else "Você é o Agente Gestor operacional do SESA. Encaminhe solicitações sem expor código ou segredos."},
            {"role": "user", "content": message},
        ],
    }
    response = requests.post(GROQ_URL, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


@app.on_event("startup")
def startup() -> None:
    read_status()
    init_audit()
    init_users()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sesa-agente-gestor"}


@app.get("/api/status")
def status() -> dict[str, Any]:
    return read_status()


@app.post("/api/auth/login")
def login(request: LoginRequest) -> dict[str, Any]:
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    if user["role"] != "Master" or user.get("environment") != "developer":
        audit("auth.login", user["username"], {"role": user["role"], "environment": user.get("environment", "gestor"), "mode": "operational"})
        return {"authenticated": True, "mode": "operational", "user": user}
    token = issue_session(user)
    audit("auth.login", user["username"], {"role": user["role"], "environment": user["environment"], "mode": "developer"})
    return {"authenticated": True, "mode": "developer", "user": user, "token": token}


@app.get("/api/auth/master", dependencies=[Depends(require_master)])
def master_authentication() -> dict[str, Any]:
    audit("auth.master", "master", {"result": "authenticated"})
    return {"authenticated": True, "mode": "developer"}


@app.get("/api/users", dependencies=[Depends(require_master)])
def users() -> dict[str, Any]:
    return {"users": list_users()}


@app.post("/api/users", dependencies=[Depends(require_master)])
def add_user(request: UserCreateRequest) -> dict[str, Any]:
    if request.environment == "developer" and request.role != "Master":
        raise HTTPException(status_code=400, detail="Somente usuários Master podem acessar o ambiente Desenvolvedor")
    try:
        user = create_user(request.username, request.role, request.environment, request.password)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Usuário já existe") from None
    audit("user.create", "master", {"username": user["username"], "role": user["role"]})
    return user


@app.patch("/api/users/{username}/password", dependencies=[Depends(require_master)])
def change_user_password(username: str, request: UserPasswordRequest) -> dict[str, bool]:
    try:
        set_user_password(username, request.password)
    except KeyError:
        raise HTTPException(status_code=404, detail="Usuário não encontrado") from None
    audit("user.password.reset", "master", {"username": username})
    return {"updated": True}


@app.patch("/api/users/{username}/status", dependencies=[Depends(require_master)])
def change_user_status(username: str, request: UserStatusRequest) -> dict[str, bool]:
    try:
        set_user_active(username, request.active)
    except KeyError:
        raise HTTPException(status_code=404, detail="Usuário não encontrado") from None
    audit("user.status.update", "master", {"username": username, "active": request.active})
    return {"updated": True}


@app.patch("/api/users/{username}/environment", dependencies=[Depends(require_master)])
def change_user_environment(username: str, request: UserEnvironmentRequest) -> dict[str, bool]:
    try:
        current = next(user for user in list_users() if user["username"] == username.strip().lower())
        if request.environment == "developer" and current["role"] != "Master":
            raise HTTPException(status_code=400, detail="Somente usuários Master podem acessar o ambiente Desenvolvedor")
        set_user_environment(username, request.environment)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Usuário não encontrado") from None
    audit("user.environment.update", "master", {"username": username, "environment": request.environment})
    return {"updated": True}


@app.patch("/api/users/{username}/rename", dependencies=[Depends(require_master)])
def rename_existing_user(username: str, request: UserRenameRequest) -> dict[str, Any]:
    try:
        renamed = rename_user(username, request.new_username)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Novo nome de usuário já existe") from None
    except KeyError:
        raise HTTPException(status_code=404, detail="Usuário não encontrado") from None
    audit("user.rename", "master", {"username": username, "new_username": renamed["username"]})
    return {"updated": True, **renamed}


@app.delete("/api/users/{username}", dependencies=[Depends(require_master)])
def remove_existing_user(username: str) -> dict[str, bool]:
    try:
        delete_user(username)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from None
    except KeyError:
        raise HTTPException(status_code=404, detail="Usuário não encontrado") from None
    audit("user.delete", "master", {"username": username})
    return {"deleted": True}


@app.get("/api/drive/overview", dependencies=[Depends(require_master)])
def drive_status() -> dict[str, Any]:
    overview = drive_overview()
    audit("drive.overview", "master", {"root_exists": overview["exists"]})
    return overview


@app.post("/api/status", dependencies=[Depends(require_master)])
def update_status(update: StatusUpdate) -> dict[str, Any]:
    status = read_status()
    if update.node not in status["stages"]:
        raise HTTPException(status_code=404, detail=f"Nó desconhecido: {update.node}")
    status["stages"][update.node] = {"label": update.label, "state": update.state, "progress": update.progress, "note": update.note}
    write_status(status)
    audit("status.update", "master", update.model_dump())
    return status


@app.post("/api/chat")
def chat(request: ChatRequest, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    actor = "gestor"
    if request.mode == "developer":
        require_master(authorization)
        actor = "master"
    status = read_status()
    status["stages"]["gestor"] = {"label": "Processando solicitação", "state": "active", "progress": 45, "note": f"Modo {request.mode}"}
    write_status(status)
    try:
        groq_enabled = bool(os.getenv("GROQ_API_KEY"))
        answer = groq_chat(request.message, request.mode)
        events = process_events(request.mode, groq_enabled)
        status = read_status()
        status["stages"]["gestor"] = {"label": "Atendimento concluído", "state": "active", "progress": 50, "note": f"Modo {request.mode}"}
        write_status(status)
        audit("chat", actor, {"mode": request.mode, "message_length": len(request.message), "crewai_available": bool(build_crewai_developer_agent())})
        return {"answer": answer, "mode": request.mode, "events": events, "updated_at": now_iso()}
    except Exception:
        status = read_status()
        status["stages"]["gestor"] = {"label": "Falha controlada", "state": "blocked", "progress": 45, "note": "Verificar logs do backend"}
        write_status(status)
        raise
