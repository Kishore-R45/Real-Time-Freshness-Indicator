@echo off
echo ========================================
echo   Real-Time Freshness Indicator
echo ========================================
echo.

echo Starting Backend Server...
start "Backend" cmd /k "cd backend && python app.py"

echo Waiting for backend to start...
timeout /t 5

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && streamlit run app.py --server.port 8501"

echo.
echo ========================================
echo   Application is running!
echo   Frontend: http://localhost:8501
echo   Backend:  http://localhost:5000
echo ========================================
pause