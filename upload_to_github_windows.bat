@echo off
echo 🚀 Загрузка FaceSort на GitHub (Windows версия)...
echo 📁 Рабочая директория: %cd%
echo.

echo 📝 Проверяем статус Git...
git status --porcelain
if errorlevel 1 (
    echo ❌ Ошибка: это не Git репозиторий
    echo 🔧 Инициализируйте Git: git init
    pause
    exit /b 1
)
echo ✅ Git репозиторий найден
echo.

echo 📦 Добавляем все изменения...
git add .
echo ✅ Изменения добавлены
echo.

echo 💾 Создаем коммит...
set "COMMIT_MSG=🚀 FaceSort - Кластеризация лиц в фотографиях

✨ Основные возможности:
- 🔍 Автоматическое распознавание лиц с ArcFace и InsightFace
- 📁 Умная кластеризация фотографий по людям
- 🎯 Два алгоритма: стандартный и продвинутый
- 📂 Обработка общих папок с автоматическим поиском
- 🔄 Автоматическое обновление в реальном времени
- 📱 Современный веб-интерфейс с drag & drop
- 📦 Экспорт результатов в ZIP архивы
- 🪟 Полная поддержка Windows

🛠 Технологии:
- Backend: FastAPI, InsightFace, ArcFace, Faiss, OpenCV
- Frontend: Vanilla JavaScript, HTML5/CSS3, Drag & Drop API

🎨 Особенности:
- Квадратные папки 150x150px
- Единообразные размеры элементов
- Автоматическое обновление каждую секунду
- Обработка общих папок с рекурсивным поиском
- Подсчет реального количества фотографий
- Виртуальное окружение для Windows"

git commit -m "%COMMIT_MSG%" 2>nul
if errorlevel 1 (
    echo ⚠️ Нет изменений для коммита или ошибка
) else (
    echo ✅ Коммит создан
)
echo.

echo 🔍 Проверяем remote origin...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Remote origin не настроен
    echo 🔧 Настройте remote origin:
    echo    git remote add origin https://github.com/ВАШ_USERNAME/facesort.git
    echo.
    echo 📋 Создайте репозиторий на https://github.com/new
    echo    - Название: facesort
    echo    - Описание: 📸 FaceSort - Кластеризация лиц в фотографиях с использованием ArcFace и InsightFace
    echo    - Видимость: Public
    echo.
    pause
    exit /b 1
)

echo ✅ Remote origin настроен
echo.

echo ⬆️ Загружаем на GitHub...
git push origin main 2>nul
if errorlevel 1 (
    echo ❌ Ошибка загрузки
    echo 🔧 Проверьте:
    echo    - Правильность URL репозитория
    echo    - Наличие прав на запись
    echo    - Подключение к интернету
    pause
    exit /b 1
)
echo ✅ Проект загружен на GitHub!
echo.

echo 🌐 Получаем ссылку на репозиторий...
for /f "tokens=*" %%i in ('git remote get-url origin') do set REMOTE_URL=%%i
echo Ссылка на репозиторий: %REMOTE_URL%
echo.

echo 🎉 Готово! Проект FaceSort доступен на GitHub
echo 📋 Следующие шаги:
echo    - Откройте ссылку выше в браузере
echo    - Добавьте описание и теги
echo    - Пригласите контрибьюторов
echo.
pause
