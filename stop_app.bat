@echo off
echo Encerrando o app do Streamlit...

:: Encontra o Process ID (PID) rodando na porta 8501 (padrão do Streamlit) e o encerra.
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do (
    taskkill /pid %%a /f 2>nul
)

echo Pronto! App encerrado.
pause
