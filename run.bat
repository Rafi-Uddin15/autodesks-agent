@echo off
echo Starting AutoDesk System...
echo --------------------------------
echo 1. Starting Backend Server...
start "AutoDesk Server" cmd /k "python server.py"
timeout /t 5 /nobreak
echo.
echo 2. Starting Frontend App...
start "AutoDesk App" cmd /k "python -m streamlit run app.py"
echo.
echo System Started! Check your browser.
pause
