# Исправление проблемы со статическими файлами на Windows

## 🔧 Проблема
На Windows получаете ошибку:
```
app.js:1 Failed to load resource: the server responded with a status of 404 (Not Found)
```

## ✅ Решение

### 1. Проверьте структуру файлов
Убедитесь, что у вас есть папка `static` с файлами:
```
facesort/
├── static/
│   ├── index.html
│   └── app.js
├── main_windows_simple.py
└── cluster_simple_windows.py
```

### 2. Используйте правильный файл
Для Windows используйте:
```cmd
python main_windows_simple.py
```

**НЕ используйте:**
- `main-windows.py` (старая версия)
- `main_windows_fixed.py` (может не работать)

### 3. Проверьте тест
Запустите тест статических файлов:
```cmd
python test_static.py
```
Затем откройте: `http://localhost:8001/test`

### 4. Если проблема остается

#### Вариант A: Скопируйте файлы вручную
```cmd
mkdir static
copy static\index.html .
copy static\app.js .
```

#### Вариант B: Используйте абсолютные пути
Измените в `main_windows_simple.py`:
```python
# Вместо:
app.mount("/static", StaticFiles(directory="static"), name="static")

# Используйте:
import os
static_path = os.path.abspath("static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
```

#### Вариант C: Встроенные статические файлы
Создайте `main_windows_embedded.py` с встроенными файлами.

### 5. Альтернативное решение
Если ничего не помогает, используйте простой HTTP сервер:
```cmd
cd static
python -m http.server 8080
```
Затем откройте: `http://localhost:8080`

## 🔍 Диагностика

### Проверьте:
1. **Папка static существует?**
   ```cmd
   dir static
   ```

2. **Файлы в папке static?**
   ```cmd
   dir static\*.html
   dir static\*.js
   ```

3. **Права доступа?**
   ```cmd
   icacls static
   ```

4. **Антивирус блокирует?**
   Добавьте папку в исключения антивируса.

## 📞 Если проблема остается

1. Проверьте логи сервера
2. Откройте Developer Tools в браузере (F12)
3. Проверьте Network tab
4. Убедитесь, что файлы загружаются

## 🎯 Быстрое решение

Скачайте готовую версию с GitHub:
```cmd
git clone https://github.com/RockInMyHead/facesort.git
cd facesort
python main_windows_simple.py
```
