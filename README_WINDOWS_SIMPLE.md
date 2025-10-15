# FaceSort - Простая версия для Windows

## 🚀 Быстрый старт

### 1. Установка зависимостей
```cmd
install_windows_simple.cmd
```

### 2. Запуск сервера
```cmd
call venv\Scripts\activate.bat
python main_windows_simple.py
```

### 3. Открыть в браузере
```
http://localhost:8000
```

## 📋 Требования

- Python 3.9+
- Windows 10/11
- 4GB RAM (рекомендуется)

## 🔧 Что включено

- ✅ Простая детекция лиц (OpenCV Haar Cascade)
- ✅ Кластеризация (AgglomerativeClustering)
- ✅ Веб-интерфейс
- ✅ API для интеграции
- ✅ Поддержка Windows дисков

## 📁 Структура файлов

- `main_windows_simple.py` - основной сервер
- `cluster_simple_windows.py` - простая кластеризация
- `requirements_windows_simple.txt` - зависимости
- `install_windows_simple.cmd` - установка

## 🎯 Использование

1. **Выберите папку** с фотографиями
2. **Нажмите "Обработать"**
3. **Дождитесь завершения**
4. **Найдите отсортированные папки**

## ⚠️ Ограничения

- Менее точная детекция лиц (по сравнению с advanced версией)
- Только базовые алгоритмы кластеризации
- Подходит для простых случаев

## 🔧 Устранение проблем

### Ошибка "No module named 'cv2'"
```cmd
pip install opencv-python
```

### Ошибка "No module named 'sklearn'"
```cmd
pip install scikit-learn
```

### Порт 8000 занят
Измените порт в `main_windows_simple.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

## 📞 Поддержка

Если возникают проблемы, проверьте:
1. Python 3.9+ установлен
2. Виртуальное окружение активировано
3. Все зависимости установлены
4. Порт 8000 свободен
