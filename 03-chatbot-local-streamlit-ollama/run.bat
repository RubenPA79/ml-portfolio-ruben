@echo off
echo ================================================
echo       INICIANDO CHATBOT STREAMLIT + OLLAMA
echo ================================================
echo.

REM Activar entorno virtual
if not exist .venv (
    echo [ERROR] Entorno virtual no encontrado.
    echo Ejecuta install.bat primero.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

REM Verificar Ollama
echo Verificando conexion con Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ADVERTENCIA] Ollama no esta corriendo.
    echo.
    echo SOLUCION:
    echo 1. Abre otra terminal
    echo 2. Ejecuta: ollama serve
    echo 3. Instala modelo: ollama pull phi3:mini
    echo.
    echo Presiona Enter para continuar de todas formas...
    pause >nul
)

REM Ejecutar aplicación
echo.
echo Iniciando aplicacion Streamlit...
echo Tu navegador se abrira automaticamente en http://localhost:8501
echo.
echo Para detener la aplicacion: Ctrl+C
echo.
streamlit run app.py