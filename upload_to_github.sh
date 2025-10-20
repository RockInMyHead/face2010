#!/bin/bash

# Скрипт для загрузки FaceSort на GitHub

echo "🚀 Загрузка FaceSort на GitHub..."

# Инициализация Git репозитория
echo "📁 Инициализация Git репозитория..."
git init

# Добавление всех файлов
echo "📝 Добавление файлов в Git..."
git add .

# Первый коммит
echo "💾 Создание первого коммита..."
git commit -m "🎉 Initial commit: FaceSort - Кластеризация лиц в фотографиях

✨ Основные возможности:
- 🔍 Автоматическое распознавание лиц с ArcFace и InsightFace
- 📁 Умная кластеризация фотографий по людям
- 🎯 Два алгоритма: стандартный и продвинутый
- 📂 Обработка общих папок с автоматическим поиском
- 🔄 Автоматическое обновление в реальном времени
- 📱 Современный веб-интерфейс с drag & drop
- 📦 Экспорт результатов в ZIP архивы

🛠 Технологии:
- Backend: FastAPI, InsightFace, ArcFace, Faiss, OpenCV
- Frontend: Vanilla JavaScript, HTML5/CSS3, Drag & Drop API

🎨 Особенности:
- Квадратные папки 150x150px
- Единообразные размеры элементов
- Автоматическое обновление каждую секунду
- Обработка общих папок с рекурсивным поиском
- Подсчет реального количества фотографий"

# Создание репозитория на GitHub (требует GitHub CLI)
echo "🌐 Создание репозитория на GitHub..."
if command -v gh &> /dev/null; then
    gh repo create facesort --public --description "📸 FaceSort - Кластеризация лиц в фотографиях с использованием ArcFace и InsightFace"
    echo "✅ Репозиторий создан на GitHub!"
else
    echo "⚠️ GitHub CLI не установлен. Создайте репозиторий вручную на https://github.com/new"
    echo "📋 Название репозитория: facesort"
    echo "📋 Описание: 📸 FaceSort - Кластеризация лиц в фотографиях с использованием ArcFace и InsightFace"
    echo "📋 Видимость: Public"
fi

# Добавление remote origin
echo "🔗 Добавление remote origin..."
git remote add origin https://github.com/$(git config user.name)/facesort.git

# Push в GitHub
echo "⬆️ Загрузка на GitHub..."
git branch -M main
git push -u origin main

echo "✅ Проект успешно загружен на GitHub!"
echo "🌐 Ссылка: https://github.com/$(git config user.name)/facesort"
