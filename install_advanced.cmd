@echo off
REM Скрипт установки продвинутой кластеризации для Windows

echo 🚀 Установка продвинутой системы кластеризации лиц
echo ==================================================
echo.

REM Проверка Python
python --version
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)

REM Проверка виртуального окружения
if not exist ".venv" (
    echo ⚠️  Виртуальное окружение не найдено
    echo 📦 Создаю виртуальное окружение...
    python -m venv .venv
)

echo 🔧 Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo 📥 Установка базовых зависимостей...
python -m pip install --upgrade pip setuptools wheel

echo 📥 Установка продвинутых зависимостей...
pip install -r requirements-advanced.txt

echo.
echo ✅ Установка завершена!
echo.
echo 📚 Дополнительная информация:
echo    - Документация: ADVANCED_CLUSTERING_GUIDE.md
echo    - Модели InsightFace будут загружены автоматически при первом запуске (~500MB)
echo.
echo 🚀 Запуск с продвинутой кластеризацией:
echo    set USE_ADVANCED_CLUSTERING=true
echo    python main.py
echo.
echo 💡 Для GPU (опционально):
echo    pip install onnxruntime-gpu
echo    # и измените use_gpu=True в main.py
echo.
pause

