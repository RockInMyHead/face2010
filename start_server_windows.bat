@echo off
echo 🚀 Запуск проекта FaceSort на Windows...
echo 📁 Рабочая директория: %cd%
python --version
echo.

echo 📦 Проверяем виртуальное окружение...
if not exist venv (
    echo 🔧 Создаем виртуальное окружение...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Ошибка создания виртуального окружения
        pause
        exit /b 1
    )
    echo ✅ Виртуальное окружение создано
) else (
    echo ✅ Виртуальное окружение найдено
)

echo 🔄 Активируем виртуальное окружение...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Ошибка активации виртуального окружения
    pause
    exit /b 1
)
echo ✅ Виртуальное окружение активировано
echo.

echo 📦 Проверяем зависимости...
python -c "import fastapi, uvicorn, PIL, cv2, insightface, faiss" 2>nul
if errorlevel 1 (
    echo ❌ Некоторые зависимости не установлены.
    echo 🔧 Устанавливаем зависимости...
    pip install --upgrade pip
    pip install -r requirements-win.txt
    if errorlevel 1 (
        echo ❌ Ошибка установки зависимостей
        pause
        exit /b 1
    )
    echo ✅ Зависимости установлены
) else (
    echo ✅ Основные зависимости установлены
)
echo.

echo 🛑 Останавливаем предыдущие процессы...
taskkill /f /im python.exe /fi "WINDOWTITLE eq main.py*" >nul 2>&1
taskkill /f /im python.exe /fi "IMAGENAME eq python.exe" /fi "MEMUSAGE gt 100000" >nul 2>&1
timeout /t 2 >nul

echo 🚀 Запускаем сервер FaceSort...
start "FaceSort Server" python main.py

echo ✅ Сервер запущен!
echo 🌐 URL: http://localhost:8000
echo 📊 Проверка через 5 секунд...
timeout /t 5 >nul

echo 📋 Для остановки сервера закройте окно командной строки или нажмите Ctrl+C
echo 🎯 Откройте http://localhost:8000 в браузере
pause
