$ErrorActionPreference = "Stop"

# Execute este arquivo a partir da pasta backend do projeto clonado.
# Configure SESA_MASTER_TOKEN e GROQ_API_KEY no ambiente do Windows antes de iniciar.
$env:SESA_DRIVE_ROOT = "G:\Meu Drive\Projeto_SESA"
$env:SESA_ALLOWED_ORIGINS = "https://www.zallure.com.br,http://localhost:5173"
$env:SESA_STATUS_FILE = Join-Path $PSScriptRoot "status.json"
$env:SESA_AUDIT_DB = Join-Path $PSScriptRoot "audit.db"

python -m uvicorn app:app --host 127.0.0.1 --port 8787
