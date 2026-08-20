@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================================================
REM SESA - Inicializador local do backend
REM Fase 1 - ambiente de desenvolvimento
REM ============================================================

cd /d "%~dp0backend"
if errorlevel 1 (
    echo ERRO: a pasta backend nao foi encontrada em %~dp0backend
    pause
    exit /b 1
)

echo.
echo ============================================
echo        SESA - Backend local
echo ============================================
echo.
echo Pasta de execucao: %CD%

REM Carrega variaveis do arquivo local ignorado pelo Git, se existir.
if exist ".env.local" (
    echo Carregando configuracao local de .env.local...
    for /f "usebackq tokens=1,* delims==" %%A in (".env.local") do (
        if not "%%A"=="" if not "%%A:~0,1"=="#" set "%%A=%%B"
    )
) else (
    echo .env.local nao encontrado; usando configuracao provisoria da Fase 1.
)

REM A credencial deve estar no .env.local, que nao e publicado pelo Git.
if not defined SESA_MASTER_TOKEN (
    echo Token Master nao encontrado em .env.local.
    set /p SESA_MASTER_TOKEN=Digite o token Master provisoriamente: 
)
if not defined SESA_SESSION_SECRET set "SESA_SESSION_SECRET=%SESA_MASTER_TOKEN%"
if not defined SESA_USE_CREWAI set "SESA_USE_CREWAI=false"

REM Procura Python nesta ordem: ambiente virtual, python no PATH e py.exe.
set "PYTHON_CMD="
if exist ".venv\Scripts\python.exe" set "PYTHON_CMD=.venv\Scripts\python.exe"

if defined PYTHON_CMD goto python_found
where python >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=python"

if defined PYTHON_CMD goto python_found
where py >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3"

if not defined PYTHON_CMD (
    echo.
    echo ERRO: Python nao foi encontrado.
    echo.
    echo Instale o Python 3.11 em https://www.python.org/downloads/windows/
    echo Durante a instalacao, marque a opcao: Add python.exe to PATH.
    echo Depois, feche e abra novamente o arquivo iniciar_sesa.bat.
    pause
    exit /b 1
)

:python_found

echo.
echo Iniciando SESA em http://127.0.0.1:8787
echo Verificacao: http://127.0.0.1:8787/api/health
echo Mantenha esta janela aberta durante o uso.
echo.

%PYTHON_CMD% -m uvicorn app:app --host 127.0.0.1 --port 8787

set "EXIT_CODE=%ERRORLEVEL%"
echo.
echo O backend foi encerrado com codigo %EXIT_CODE%.
pause
exit /b %EXIT_CODE%
