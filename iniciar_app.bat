@echo off
cd /d "%~dp0"
echo Iniciando app de planificacion de inventarios...
set FLASK_APP=wsgi.py
set FLASK_DEBUG=1
uv run python -m flask run --host=127.0.0.1 --port=5000
start http://127.0.0.1:5000/
pause
