@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================================================
REM SESA - Inicializador local do backend
REM Estrutura oficial: Projeto_SESA\backend\app.py
REM ============================================================

set "PROJECT_DIR=%~dp0"
set "BACKEND_DIR=%PROJECT_DIR%backend"

if not exist "%BACKEND_DIR%\app.py" (
    echo ERRO: o arquivo backend\app.py nao foi encontrado em:
    echo %BACKEND_DIR%
    echo.
    echo Restaure a pasta backend ao lado da pasta SESA.
    pause
    exit /b 1
)

cd /d "%PROJECT_DIR%"

echo.
echo ============================================
echo        SESA - Backend local
echo ============================================
echo.
echo Pasta do projeto: %PROJECT_DIR%
echo Pasta do backend: %BACKEND_DIR%

REM Carrega o .env.local que fica na raiz do projeto.
if exist "%PROJECT_DIR%.env.local" (
    echo [OK] Configuracao .env.local encontrada.
    for /f "usebackq tokens=1,* delims==" %%A in ("%PROJECT_DIR%.env.local") do (
        if not "%%A"=="" if not "%%A:~0,1"=="#" set "%%A=%%B"
    )
) else (
    echo .env.local nao encontrado; usando configuracao provisoria da Fase 1.
)

if not defined SESA_MASTER_TOKEN (
    echo Token Master nao encontrado em .env.local.
    set /p SESA_MASTER_TOKEN=Digite o token Master provisoriamente: 
)
if not defined SESA_SESSION_SECRET set "SESA_SESSION_SECRET=%SESA_MASTER_TOKEN%"
if not defined SESA_USE_CREWAI set "SESA_USE_CREWAI=false"

REM Procura primeiro um ambiente virtual e depois o Python Launcher (py.exe).
REM Nao usamos o comando python, pois o Windows pode redireciona-lo para a Microsoft Store.
set "PYTHON_CMD="
if exist "%PROJECT_DIR%.venv\Scripts\python.exe" set "PYTHON_CMD=%PROJECT_DIR%.venv\Scripts\python.exe"
if defined PYTHON_CMD goto python_found
if exist "%BACKEND_DIR%\.venv\Scripts\python.exe" set "PYTHON_CMD=%BACKEND_DIR%\.venv\Scripts\python.exe"
if defined PYTHON_CMD goto python_found
where py >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3"
if not defined PYTHON_CMD (
    echo ERRO: o Python Launcher py.exe nao foi encontrado.
    echo Verifique no PowerShell com: py --version
    pause
    exit /b 1
)

:python_found
cd /d "%BACKEND_DIR%"
echo [OK] Interpretador encontrado: %PYTHON_CMD%
echo.
echo Iniciando SESA em http://127.0.0.1:8787
echo Interface: http://127.0.0.1:8787/SESA/
echo Verificacao: http://127.0.0.1:8787/api/health
echo Mantenha esta janela aberta durante o uso.
echo.

REM Abre a interface sem usar o comando timeout do CMD.
start "" /b powershell.exe -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8787/SESA/'"
%PYTHON_CMD% -m uvicorn app:app --host 127.0.0.1 --port 8787

set "EXIT_CODE=%ERRORLEVEL%"
echo.
echo O backend foi encerrado com codigo %EXIT_CODE%.
pause
exit /b %EXIT_CODE%
