#!/bin/bash
echo "🚀 Запуск проекта FaceSort..."
echo "📁 Рабочая директория: $(pwd)"
echo "🐍 Python версия: $(python3 --version)"
echo ""

# Останавливаем предыдущие процессы
echo "🛑 Останавливаем предыдущие процессы..."
pkill -f "python.*main.py" 2>/dev/null || true
sleep 2

# Запускаем сервер
echo "🚀 Запускаем сервер FaceSort..."
python3 main.py &
SERVER_PID=$!

echo "✅ Сервер запущен с PID: $SERVER_PID"
echo "🌐 URL: http://localhost:8000"
echo "📊 Проверка через 5 секунд..."

sleep 5

# Проверяем, что сервер работает
if curl -s http://localhost:8000/api/tasks > /dev/null 2>&1; then
    echo "✅ Сервер работает!"
    echo "🎯 Откройте http://localhost:8000 в браузере"
    echo "🔧 Используйте кнопку '📂 Общие' для тестирования"
else
    echo "❌ Сервер не отвечает"
    echo "🔍 Проверьте логи выше"
fi

echo ""
echo "📋 Для остановки сервера: kill $SERVER_PID"
echo "📋 Или нажмите Ctrl+C"
