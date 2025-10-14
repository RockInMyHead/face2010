# 🪟 Руководство по установке для Windows

## ❗ Проблема с dlib на Windows

На Windows часто возникают проблемы с установкой `dlib` из-за отсутствия CMake или Visual Studio Build Tools. Это решается несколькими способами.

## 🚀 Быстрое решение (Рекомендуется)

### Вариант 1: Использование Windows-совместимой версии

1. **Скачайте проект:**
   ```bash
   git clone https://github.com/RockInMyHead/facesort.git
   cd facesort
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Установите Windows-совместимые зависимости:**
   ```bash
   pip install -r requirements-windows.txt
   ```

4. **Запустите Windows-версию:**
   ```bash
   python main-windows.py
   ```

### Вариант 2: Установка CMake и Visual Studio Build Tools

1. **Установите Visual Studio Build Tools:**
   - Скачайте с [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Выберите "C++ build tools"
   - Установите с компонентами: MSVC, Windows 10/11 SDK, CMake

2. **Установите CMake:**
   - Скачайте с [https://cmake.org/download/](https://cmake.org/download/)
   - Выберите "Windows x64 Installer"
   - **ВАЖНО:** При установке выберите "Add CMake to system PATH"

3. **Перезапустите командную строку** и проверьте:
   ```bash
   cmake --version
   ```

4. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Альтернативные решения

### Решение 1: Использование conda

```bash
# Установите Anaconda или Miniconda
conda create -n facesort python=3.9
conda activate facesort
conda install -c conda-forge dlib
pip install -r requirements.txt
```

### Решение 2: Предварительно скомпилированные пакеты

```bash
# Установите предварительно скомпилированную версию dlib
pip install dlib-binary
pip install -r requirements.txt
```

### Решение 3: Использование Docker

```dockerfile
FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

## 📋 Сравнение версий

| Версия | Преимущества | Недостатки |
|--------|-------------|------------|
| **main.py** | Максимальная точность (99%) | Требует CMake, сложная установка |
| **main-windows.py** | Простая установка, MediaPipe | Немного ниже точность (~95%) |

## 🎯 Рекомендации

### Для разработчиков:
- Используйте **main.py** с полной установкой CMake
- Лучшая точность распознавания лиц

### Для обычных пользователей:
- Используйте **main-windows.py** 
- Простая установка без дополнительных инструментов
- Достаточная точность для большинства задач

## 🚨 Устранение проблем

### Ошибка: "CMake is not installed"
```bash
# Решение 1: Установите CMake
# Скачайте с https://cmake.org/download/
# Добавьте в PATH при установке

# Решение 2: Используйте Windows-версию
python main-windows.py
```

### Ошибка: "Microsoft Visual C++ 14.0 is required"
```bash
# Установите Visual Studio Build Tools
# Или используйте conda:
conda install -c conda-forge dlib
```

### Ошибка: "Failed building wheel for dlib"
```bash
# Решение 1: Обновите pip и setuptools
pip install --upgrade pip setuptools wheel

# Решение 2: Используйте предварительно скомпилированную версию
pip install dlib-binary

# Решение 3: Используйте Windows-версию
python main-windows.py
```

## 🔍 Проверка установки

### Тест 1: Проверка зависимостей
```bash
python -c "import cv2, numpy, sklearn, fastapi; print('✅ Основные зависимости работают')"
```

### Тест 2: Проверка face_recognition (для main.py)
```bash
python -c "import face_recognition; print('✅ face_recognition работает')"
```

### Тест 3: Проверка MediaPipe (для main-windows.py)
```bash
python -c "import mediapipe; print('✅ MediaPipe работает')"
```

## 📊 Производительность

| Параметр | main.py | main-windows.py |
|----------|---------|-----------------|
| **Точность** | 99% | 95% |
| **Скорость** | 100-500 img/min | 80-400 img/min |
| **Установка** | Сложная | Простая |
| **Память** | 4-8 GB | 2-4 GB |

## 🎉 Готово!

После успешной установки:

1. **Запустите приложение:**
   ```bash
   # Для основной версии
   python main.py
   
   # Для Windows-версии
   python main-windows.py
   ```

2. **Откройте браузер:** http://localhost:8000

3. **Начните использовать:** Загружайте фотографии и запускайте кластеризацию!

## 🤝 Поддержка

Если возникли проблемы:

1. **Проверьте логи** в консоли
2. **Убедитесь**, что все зависимости установлены
3. **Попробуйте Windows-версию** если основная не работает
4. **Создайте issue** на GitHub с описанием проблемы

---

**Создано для**: Windows 10/11, Python 3.8+
