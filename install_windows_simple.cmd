@echo off
echo 🚀 Установка FaceSort для Windows (без dlib)...
echo.

REM Создаем виртуальное окружение
echo 📦 Создание виртуального окружения...
python -m venv venv
if errorlevel 1 (
    echo ❌ Ошибка создания виртуального окружения
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
echo 🔧 Активация виртуального окружения...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Ошибка активации виртуального окружения
    pause
    exit /b 1
)

REM Обновляем pip
echo 📥 Обновление pip...
python -m pip install --upgrade pip

REM Устанавливаем зависимости без dlib
echo 📦 Установка зависимостей (без dlib)...
pip install -r requirements-windows-simple.txt
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo.
echo ✅ Установка завершена!
echo.
echo 🚀 Для запуска используйте:
echo    python main_simple.py
echo.
pause
