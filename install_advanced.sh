#!/bin/bash

# Скрипт установки продвинутой кластеризации для macOS/Linux

echo "🚀 Установка продвинутой системы кластеризации лиц"
echo "=================================================="
echo ""

# Проверка Python версии
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Обнаружен Python: $python_version"

# Проверка виртуального окружения
if [ ! -d ".venv" ]; then
    echo "⚠️  Виртуальное окружение не найдено"
    echo "📦 Создаю виртуальное окружение..."
    python3 -m venv .venv
fi

echo "🔧 Активация виртуального окружения..."
source .venv/bin/activate

echo "📥 Установка базовых зависимостей..."
pip install --upgrade pip setuptools wheel

echo "📥 Установка продвинутых зависимостей..."
pip install -r requirements-advanced.txt

echo ""
echo "✅ Установка завершена!"
echo ""
echo "📚 Дополнительная информация:"
echo "   - Документация: ADVANCED_CLUSTERING_GUIDE.md"
echo "   - Модели InsightFace будут загружены автоматически при первом запуске (~500MB)"
echo ""
echo "🚀 Запуск с продвинутой кластеризацией:"
echo "   export USE_ADVANCED_CLUSTERING=true"
echo "   python main.py"
echo ""
echo "💡 Для GPU (опционально):"
echo "   pip install onnxruntime-gpu"
echo "   # и измените use_gpu=True в main.py"
echo ""

