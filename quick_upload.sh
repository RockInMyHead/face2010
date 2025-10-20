#!/bin/bash

# Быстрая загрузка FaceSort на GitHub

echo "🚀 Быстрая загрузка FaceSort на GitHub..."

# Проверяем, что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: файл main.py не найден. Убедитесь, что вы в директории проекта."
    exit 1
fi

# Инициализация Git
echo "📁 Инициализация Git..."
git init

# Добавление файлов
echo "📝 Добавление файлов..."
git add .

# Коммит
echo "💾 Создание коммита..."
git commit -m "🎉 FaceSort: Кластеризация лиц в фотографиях

✨ Возможности:
- 🔍 Распознавание лиц (ArcFace + InsightFace)
- 📁 Умная кластеризация фотографий
- 🔄 Автоматическое обновление в реальном времени
- 📂 Обработка общих папок
- 📱 Современный веб-интерфейс
- 📦 Экспорт в ZIP

🛠 Технологии: FastAPI, InsightFace, ArcFace, Faiss, OpenCV, Vanilla JS

🎨 UI: Квадратные папки 150x150px, drag & drop, автообновление"

echo "✅ Git репозиторий готов!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Создайте репозиторий на https://github.com/new"
echo "2. Название: facesort"
echo "3. Описание: 📸 FaceSort - Кластеризация лиц в фотографиях"
echo "4. Видимость: Public"
echo "5. Затем выполните:"
echo "   git remote add origin https://github.com/ВАШ_USERNAME/facesort.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "🌐 После загрузки проект будет доступен по адресу:"
echo "   https://github.com/ВАШ_USERNAME/facesort"
