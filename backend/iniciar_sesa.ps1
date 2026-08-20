$ErrorActionPreference = "Stop"

# Execute este arquivo a partir da pasta backend do projeto clonado.
# Configure SESA_MASTER_TOKEN e GROQ_API_KEY no ambiente do Windows antes de iniciar.
$env:SESA_DRIVE_ROOT = "G:\Meu Drive\Projeto_SESA"
$env:SESA_ALLOWED_ORIGINS = "https://www.zallure.com.br,http://localhost:5173"

# Carrega credenciais somente do arquivo local ignorado pelo Git.
$localEnv = Join-Path $PSScriptRoot ".env.local"
if (Test-Path $localEnv) {
    Get-Content $localEnv | ForEach-Object {
        if ($_ -match '^\s*([^#=]+?)\s*=\s*(.*)\s*$') {
            [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}
if (-not $env:SESA_MASTER_TOKEN) {
    throw "SESA_MASTER_TOKEN não configurado. Crie backend/.env.local, que não será publicado, e defina o token Master."
}
$env:SESA_STATUS_FILE = Join-Path $PSScriptRoot "status.json"
$env:SESA_AUDIT_DB = Join-Path $PSScriptRoot "audit.db"

python -m uvicorn app:app --host 127.0.0.1 --port 8787
