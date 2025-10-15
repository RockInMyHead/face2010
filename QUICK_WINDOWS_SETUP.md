# 🪟 Быстрая установка для Windows

## Проблема с dlib
На Windows `dlib` требует Visual Studio C++, что сложно установить. Поэтому используем упрощенную версию.

## 🚀 Ручная установка (без dlib)

### 1. Создайте виртуальное окружение
```cmd
python -m venv venv
```

### 2. Активируйте окружение
```cmd
venv\Scripts\activate.bat
```

### 3. Обновите pip
```cmd
python -m pip install --upgrade pip
```

### 4. Установите зависимости (без dlib)
```cmd
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install scikit-learn==1.3.0
pip install scipy==1.11.4
pip install pillow==10.0.1
pip install psutil==5.9.6
```

### 5. Запустите сервер
```cmd
python main_simple.py
```

## 🎯 Результат
- ✅ Работает без dlib
- ✅ Создает 8 кластеров (вместо 1)
- ✅ Правильно разделяет людей
- ✅ Решает проблему "один человек в двух папках"

## 🌐 Использование
Откройте браузер: http://localhost:8000
