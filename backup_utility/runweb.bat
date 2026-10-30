@echo off
chcp 65001 > nul
cd /d "C:\Users\Артем\Desktop\backup_utility"
python -m streamlit run app_web.py
if %errorlevel% neq 0 (
    echo.
    echo [ОШИБКА] Не удалось запустить Streamlit через команду "python".
    echo Попробуем запустить через явный путь...
    echo.
    py -3 -m streamlit run app_web.py
)
pause
