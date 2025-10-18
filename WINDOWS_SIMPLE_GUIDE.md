# 🪟 FaceSort для Windows (Упрощенная версия)

## Проблема с dlib на Windows

На Windows установка `dlib` требует Visual Studio C++ Build Tools, что может быть сложно. Поэтому мы создали упрощенную версию без `dlib`.

## 🚀 Быстрая установка

### Вариант 1: Автоматическая установка
```cmd
install_windows_simple.cmd
```

### Вариант 2: Ручная установка
```cmd
# 1. Создать виртуальное окружение
python -m venv venv

# 2. Активировать окружение
venv\Scripts\activate.bat

# 3. Обновить pip
python -m pip install --upgrade pip

# 4. Установить зависимости
pip install -r requirements-windows-simple.txt
```

## 🎯 Запуск

```cmd
# Активировать окружение
venv\Scripts\activate.bat

# Запустить сервер
python main_simple.py
```

## 📋 Что включено

- ✅ **FastAPI** - веб-сервер
- ✅ **OpenCV** - детекция лиц (Haar Cascade)
- ✅ **scikit-learn** - кластеризация
- ✅ **NumPy, SciPy** - математические операции
- ✅ **Pillow** - обработка изображений

## 🔧 Отличия от полной версии

- ❌ Нет `dlib` (проблемы с установкой на Windows)
- ❌ Нет `face_recognition` (зависит от dlib)
- ✅ Использует OpenCV Haar Cascade для детекции лиц
- ✅ Использует упрощенную кластеризацию
- ✅ Работает стабильно на Windows

## 🎯 Результат

Система создает **8 кластеров** для лучшего разделения людей, что решает проблему "один человек в двух папках".

## 🆘 Если что-то не работает

1. Убедитесь, что Python 3.9+ установлен
2. Проверьте, что виртуальное окружение активировано
3. Попробуйте обновить pip: `python -m pip install --upgrade pip`
