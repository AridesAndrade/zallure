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

try:
    from crewai import Agent, Crew, Process, Task
except ImportError:  # The backend remains inspectable before dependencies are installed.
    Agent = Crew = Process = Task = None

ROOT = Path(__file__).resolve().parent
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
    if not hmac.compare_digest(hashlib.sha256(supplied.encode()).digest(), hashlib.sha256(configured.encode()).digest()):
        raise HTTPException(status_code=403, detail="Token Master inválido")
    return "master"


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


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sesa-agente-gestor"}


@app.get("/api/status")
def status() -> dict[str, Any]:
    return read_status()


@app.post("/api/status", dependencies=[Depends(require_master)])
def update_status(update: StatusUpdate) -> dict[str, Any]:
    status = read_status()
    if update.node not in status["stages"]:
        raise HTTPException(status_code=404, detail=f"Nó desconhecido: {update.node}")
    status["stages"][update.node] = {"label": update.label, "state": update.state, "progress": update.progress, "note": update.note}
    write_status(status)
    audit("status.update", "master", update.model_dump())
    return status


@app.post("/api/chat", dependencies=[Depends(require_master)])
def chat(request: ChatRequest) -> dict[str, Any]:
    status = read_status()
    status["stages"]["gestor"] = {"label": "Processando solicitação", "state": "active", "progress": 45, "note": "Modo Desenvolvedor Master"}
    write_status(status)
    try:
        answer = groq_chat(request.message, request.mode)
        status = read_status()
        status["stages"]["gestor"] = {"label": "Modo Desenvolvedor ativo", "state": "active", "progress": 50, "note": "Solicitação concluída"}
        write_status(status)
        audit("chat", "master", {"mode": request.mode, "message_length": len(request.message), "crewai_available": bool(build_crewai_developer_agent())})
        return {"answer": answer, "mode": request.mode, "updated_at": now_iso()}
    except Exception:
        status = read_status()
        status["stages"]["gestor"] = {"label": "Falha controlada", "state": "blocked", "progress": 45, "note": "Verificar logs do backend"}
        write_status(status)
        raise
