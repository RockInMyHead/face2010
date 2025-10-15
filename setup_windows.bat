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
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install scikit-learn==1.3.0
pip install scipy==1.11.4
pip install pillow==10.0.1
pip install psutil==5.9.6

echo.
echo ✅ Установка завершена!
echo.
echo 🚀 Для запуска используйте:
echo    venv\Scripts\activate.bat
echo    python main_simple.py
echo.
pause
