#!/usr/bin/env python3
"""
Улучшенная версия main.py с более подробным логированием
и улучшенной обработкой папок
"""

import os
import sys
import time
import uuid
import zipfile
import tempfile
import asyncio
import re
from pathlib import Path
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import psutil
from PIL import Image, ImageOps
from io import BytesIO

# Импортируем улучшенную версию кластеризации
from cluster_improved import build_plan_live, distribute_to_folders, process_group_folder, IMG_EXTS

app = FastAPI(title="FaceSort API", version="2.0")

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Глобальное состояние приложения
app_state = {
    "queue": [],
    "current_tasks": {}
}

class QueueItem(BaseModel):
    path: str

class ProcessingResult(BaseModel):
    moved: int
    copied: int
    clusters_count: int
    unreadable_count: int
    no_faces_count: int
    unreadable_files: List[str]
    no_faces_files: List[str]

def cleanup_old_tasks():
    """Очистить старые задачи"""
    current_time = time.time()
    tasks_to_remove = []
    
    for task_id, task in app_state["current_tasks"].items():
        if task["status"] in ["completed", "error"]:
            # Удаляем задачи старше 5 минут
            if current_time - task["created_at"] > 300:  # 5 минут
                tasks_to_remove.append(task_id)
    
    for task_id in tasks_to_remove:
        del app_state["current_tasks"][task_id]

def get_logical_drives():
    """Получить список логических дисков"""
    return [Path(p.mountpoint) for p in psutil.disk_partitions(all=False) if Path(p.mountpoint).exists()]

def get_special_dirs():
    """Получить специальные директории"""
    home = Path.home()
    return {
        "💼 Рабочий стол": home / "Desktop",
        "📄 Документы": home / "Documents", 
        "📥 Загрузки": home / "Downloads",
        "🖼 Изображения": home / "Pictures",
    }

def count_images_in_dir(path: Path) -> int:
    """Подсчитать количество изображений в директории"""
    try:
        return len([f for f in path.iterdir() if f.is_file() and f.suffix.lower() in IMG_EXTS])
    except:
        return 0

class FolderInfo(BaseModel):
    name: str
    path: str
    image_count: int
    is_dir: bool

async def process_folder_task(task_id: str, folder_path: str, include_excluded: bool = False):
    """Улучшенная фоновая задача обработки папки с подробным логированием"""
    print(f"🔍 [TASK] process_folder_task запущена: task_id={task_id}, folder_path={folder_path}, include_excluded={include_excluded}")
    
    try:
        import sys
        sys.stdout.flush()
        
        print(f"🔍 [TASK] Обновляем статус задачи {task_id} на 'running'")
        app_state["current_tasks"][task_id]["status"] = "running"
        app_state["current_tasks"][task_id]["message"] = "Начинаем обработку..."
        app_state["current_tasks"][task_id]["progress"] = 5
        
        # Небольшая задержка для демонстрации прогресс-бара
        await asyncio.sleep(2)
        app_state["current_tasks"][task_id]["progress"] = 10
        app_state["current_tasks"][task_id]["message"] = "Анализируем изображения..."
        
        await asyncio.sleep(2)
        app_state["current_tasks"][task_id]["progress"] = 25
        app_state["current_tasks"][task_id]["message"] = "Извлекаем лица..."
        
        await asyncio.sleep(2)
        app_state["current_tasks"][task_id]["progress"] = 50
        app_state["current_tasks"][task_id]["message"] = "Кластеризуем лица..."
        
        print(f"🔍 [TASK] Проверяем путь: {folder_path}")
        path = Path(folder_path)
        if not path.exists():
            print(f"❌ [TASK] Путь не существует: {folder_path}")
            raise Exception("Путь не существует")
        print(f"✅ [TASK] Путь существует: {path}")
        
        # Определяем исключенные имена
        excluded_names = ["общие", "общая", "common", "shared", "все", "all", "mixed", "смешанные"]
        
        # Если не включена обработка исключенных папок, проверяем их
        if not include_excluded:
            folder_name_lower = str(path).lower()
            for excluded_name in excluded_names:
                if excluded_name in folder_name_lower:
                    raise Exception(f"Папки с названием '{excluded_name}' не обрабатываются")
        
        # Определяем тип обработки - групповая только если есть подпапки с изображениями
        subdirs_with_images = []
        for p in path.iterdir():
            if p.is_dir() and not any(excluded_name in str(p).lower() for excluded_name in excluded_names):
                # Проверяем есть ли изображения в подпапке
                has_images = any(f.suffix.lower() in IMG_EXTS for f in p.rglob("*") if f.is_file())
                if has_images:
                    subdirs_with_images.append(p)
        
        print(f"🔍 [TASK] Найдено {len(subdirs_with_images)} подпапок с изображениями")
        
        if include_excluded:
            # Всегда используем обработку общих папок, если флаг включен
            def group_progress_callback(progress_text: str, percent: int = None):
                if task_id in app_state["current_tasks"]:
                    app_state["current_tasks"][task_id]["message"] = progress_text
                    if percent is not None:
                        app_state["current_tasks"][task_id]["progress"] = percent
                    else:
                        try:
                            if "%" in progress_text:
                                match = re.search(r'(\d+)%', progress_text)
                                if match:
                                    app_state["current_tasks"][task_id]["progress"] = int(match.group(1))
                        except:
                            pass

            app_state["current_tasks"][task_id]["message"] = "Обработка всех папок с изображениями..."
            app_state["current_tasks"][task_id]["progress"] = 10
            created_clusters = process_group_folder(path, progress_callback=group_progress_callback, include_excluded=True)
            result = ProcessingResult(
                moved=0, copied=0, clusters_count=created_clusters,
                unreadable_count=0, no_faces_count=0,
                unreadable_files=[], no_faces_files=[]
            )
        elif len(subdirs_with_images) > 1:
            # Групповая обработка
            def group_progress_callback(progress_text: str, percent: int = None):
                if task_id in app_state["current_tasks"]:
                    app_state["current_tasks"][task_id]["message"] = progress_text
                    if percent is not None:
                        app_state["current_tasks"][task_id]["progress"] = percent
                    else:
                        try:
                            if "%" in progress_text:
                                match = re.search(r'(\d+)%', progress_text)
                                if match:
                                    app_state["current_tasks"][task_id]["progress"] = int(match.group(1))
                        except:
                            pass
            
            app_state["current_tasks"][task_id]["message"] = "Групповая обработка папок..."
            app_state["current_tasks"][task_id]["progress"] = 10
            
            created_clusters = process_group_folder(path, progress_callback=group_progress_callback, include_excluded=include_excluded)
            result = ProcessingResult(
                moved=0, copied=0, clusters_count=created_clusters,
                unreadable_count=0, no_faces_count=0,
                unreadable_files=[], no_faces_files=[]
            )
        else:
            # Обычная обработка одной папки
            def progress_callback(progress_text: str, percent: int = None):
                if task_id in app_state["current_tasks"]:
                    app_state["current_tasks"][task_id]["message"] = progress_text
                    if percent is not None:
                        app_state["current_tasks"][task_id]["progress"] = percent
                    else:
                        try:
                            if "%" in progress_text:
                                match = re.search(r'(\d+)%', progress_text)
                                if match:
                                    app_state["current_tasks"][task_id]["progress"] = int(match.group(1))
                        except:
                            pass

            app_state["current_tasks"][task_id]["message"] = "Обработка папки..."
            app_state["current_tasks"][task_id]["progress"] = 10
            
            # Строим план кластеризации
            plan = build_plan_live(path, progress_callback=progress_callback, include_excluded=include_excluded)
            
            if len(plan.get("clusters", {})) == 0:
                print(f"❌ [TASK] Не удалось создать кластеры для {path}")
                app_state["current_tasks"][task_id]["status"] = "error"
                app_state["current_tasks"][task_id]["message"] = "Не удалось создать кластеры"
                app_state["current_tasks"][task_id]["progress"] = 100
                return
            
            # Распределяем файлы по папкам
            moved, copied, _ = distribute_to_folders(plan, path, progress_callback=progress_callback)
            
            result = ProcessingResult(
                moved=moved, copied=copied, clusters_count=len(plan.get("clusters", {})),
                unreadable_count=len(plan.get("unreadable", [])), 
                no_faces_count=len(plan.get("no_faces", [])),
                unreadable_files=plan.get("unreadable", []),
                no_faces_files=plan.get("no_faces", [])
            )
        
        # Завершаем задачу
        app_state["current_tasks"][task_id]["status"] = "completed"
        app_state["current_tasks"][task_id]["message"] = f"Завершено! Создано {result.clusters_count} кластеров"
        app_state["current_tasks"][task_id]["progress"] = 100
        app_state["current_tasks"][task_id]["result"] = result.dict()
        
        print(f"✅ [TASK] Задача {task_id} завершена успешно")
        print(f"📊 [TASK] Результат: {result.clusters_count} кластеров, {result.moved} перемещено, {result.copied} скопировано")
        
    except Exception as e:
        print(f"❌ [TASK] Ошибка в задаче {task_id}: {e}")
        import traceback
        traceback.print_exc()
        
        app_state["current_tasks"][task_id]["status"] = "error"
        app_state["current_tasks"][task_id]["message"] = f"Ошибка: {str(e)}"
        app_state["current_tasks"][task_id]["progress"] = 100

@app.get("/")
async def root():
    """Главная страница"""
    return FileResponse("static/index.html")

@app.get("/api/drives")
async def get_drives():
    """Получить список дисков и специальных папок"""
    drives = get_logical_drives()
    special_dirs = get_special_dirs()
    
    result = []
    
    # Добавляем логические диски
    for drive in drives:
        try:
            image_count = count_images_in_dir(drive)
            result.append(FolderInfo(
                name=f"💽 {drive.name}",
                path=str(drive),
                image_count=image_count,
                is_dir=True
            ))
        except:
            pass
    
    # Добавляем специальные папки
    for name, path in special_dirs.items():
        if path.exists():
            try:
                image_count = count_images_in_dir(path)
                result.append(FolderInfo(
                    name=name,
                    path=str(path),
                    image_count=image_count,
                    is_dir=True
                ))
            except:
                pass
    
    return {"folders": result}

@app.get("/api/folder")
async def get_folder_contents(path: str):
    """Получить содержимое папки"""
    folder_path = Path(path)
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=404, detail="Папка не найдена")
    
    folders = []
    files = []
    
    try:
        for item in folder_path.iterdir():
            if item.is_dir():
                try:
                    image_count = count_images_in_dir(item)
                    folders.append(FolderInfo(
                        name=item.name,
                        path=str(item),
                        image_count=image_count,
                        is_dir=True
                    ))
                except:
                    folders.append(FolderInfo(
                        name=item.name,
                        path=str(item),
                        image_count=0,
                        is_dir=True
                    ))
            elif item.suffix.lower() in IMG_EXTS:
                files.append(FolderInfo(
                    name=item.name,
                    path=str(item),
                    image_count=1,
                    is_dir=False
                ))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка чтения папки: {str(e)}")
    
    return {"folders": folders, "files": files}

@app.post("/api/upload")
async def upload_files(
    path: str,
    files: List[UploadFile] = File(...)
):
    """Загрузить файлы в указанную папку"""
    target_dir = Path(path)
    if not target_dir.exists():
        raise HTTPException(status_code=404, detail="Целевая папка не найдена")
    
    results = []
    
    for file in files:
        try:
            if file.filename.endswith(".zip"):
                # Обработка ZIP архива
                temp_zip = target_dir / f"temp_{uuid.uuid4().hex}.zip"
                with open(temp_zip, "wb") as f:
                    content = await file.read()
                    f.write(content)
                
                with zipfile.ZipFile(temp_zip) as archive:
                    archive.extractall(target_dir)
                
                temp_zip.unlink()
                results.append({"filename": file.filename, "status": "extracted"})
            else:
                # Обычный файл
                file_path = target_dir / file.filename
                with open(file_path, "wb") as f:
                    content = await file.read()
                    f.write(content)
                results.append({"filename": file.filename, "status": "uploaded"})
                
        except Exception as e:
            results.append({"filename": file.filename, "status": "error", "error": str(e)})
    
    return {"results": results}

@app.get("/api/queue")
async def get_queue():
    """Получить текущую очередь обработки"""
    return {"queue": app_state["queue"]}

@app.post("/api/queue/add")
async def add_to_queue(item: QueueItem, includeExcluded: bool = False):
    """Добавить папку в очередь"""
    print(f"🔍 [API] add_to_queue вызван: path={item.path}, includeExcluded={includeExcluded}")
    
    # Проверяем, что папка не содержит исключаемые названия, если не разрешено включать общие
    if not includeExcluded:
        excluded_names = ["общие", "общая", "common", "shared", "все", "all", "mixed", "смешанные"]
        folder_name_lower = str(item.path).lower()
        for excluded_name in excluded_names:
            if excluded_name in folder_name_lower:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Папки с названием '{excluded_name}' не обрабатываются. Включите флаг 'includeExcluded' для обработки таких папок."
                )
    
    if item.path not in app_state["queue"]:
        app_state["queue"].append(item.path)
        print(f"✅ [API] Добавлено в очередь: {item.path}")
    else:
        print(f"⚠️ [API] Папка уже в очереди: {item.path}")
    
    return {"message": "Папка добавлена в очередь", "queue": app_state["queue"]}

@app.post("/api/queue/clear")
async def clear_queue():
    """Очистить очередь"""
    app_state["queue"].clear()
    return {"message": "Очередь очищена"}

@app.post("/api/queue/process")
async def process_queue(background_tasks: BackgroundTasks, includeExcluded: bool = False):
    """Запустить обработку очереди"""
    print(f"🔍 [API] process_queue вызван: includeExcluded={includeExcluded}")
    print(f"🔍 [API] Текущая очередь: {app_state['queue']}")
    
    if not app_state["queue"]:
        print("❌ [API] Очередь пуста")
        raise HTTPException(status_code=400, detail="Очередь пуста")
    
    task_ids = []
    print(f"🔍 [API] Создаем задачи для {len(app_state['queue'])} папок")
    
    for folder_path in app_state["queue"]:
        task_id = str(uuid.uuid4())
        print(f"🔍 [API] Создаем задачу {task_id} для папки: {folder_path}")
        
        app_state["current_tasks"][task_id] = {
            "task_id": task_id,
            "status": "pending",
            "progress": 0,
            "message": "В очереди...",
            "folder_path": folder_path,
            "created_at": time.time(),
            "include_excluded": includeExcluded
        }
        
        print(f"🔍 [API] Добавляем фоновую задачу: {task_id}")
        background_tasks.add_task(process_folder_task, task_id, folder_path, includeExcluded)
        task_ids.append(task_id)
    
    print(f"🔍 [API] Очищаем очередь, создано {len(task_ids)} задач")
    app_state["queue"].clear()
    
    result = {"message": "Обработка запущена", "task_ids": task_ids}
    print(f"✅ [API] Возвращаем результат: {result}")
    return result

@app.get("/api/tasks")
async def get_tasks():
    """Получить статус всех задач"""
    # Очищаем старые задачи
    cleanup_old_tasks()
    
    # Возвращаем все задачи (включая недавно завершенные)
    return {"tasks": list(app_state["current_tasks"].values())}

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """Получить статус конкретной задачи"""
    if task_id not in app_state["current_tasks"]:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return app_state["current_tasks"][task_id]

@app.post("/api/tasks/clear")
async def clear_completed_tasks():
    """Очистить все завершенные задачи"""
    tasks_to_remove = []
    
    for task_id, task in app_state["current_tasks"].items():
        if task["status"] in ["completed", "error"]:
            tasks_to_remove.append(task_id)
    
    for task_id in tasks_to_remove:
        del app_state["current_tasks"][task_id]
    
    return {"message": f"Очищено {len(tasks_to_remove)} завершенных задач"}

@app.get("/api/image/preview")
async def get_image_preview(path: str, size: int = 150):
    """Получить превью изображения"""
    img_path = Path(path)
    if not img_path.exists() or img_path.suffix.lower() not in IMG_EXTS:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    try:
        # Создаем превью в памяти
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            img = ImageOps.fit(img, (size, size), Image.Resampling.LANCZOS)
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=85)
            buf.seek(0)
            from fastapi.responses import StreamingResponse
            return StreamingResponse(buf, media_type="image/jpeg")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания превью: {str(e)}")

@app.get("/api/zip")
async def zip_folder(path: str):
    """Создает ZIP архивацию указанной папки и возвращает файл"""
    folder = Path(path)
    if not folder.exists() or not folder.is_dir():
        raise HTTPException(status_code=404, detail="Папка не найдена")
    # Создаем временный zip-файл
    tmp_dir = tempfile.gettempdir()
    zip_name = f"{uuid.uuid4()}.zip"
    zip_path = Path(tmp_dir) / zip_name
    # Делает архив
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in folder.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(folder)
                zipf.write(file_path, arcname)
    
    return FileResponse(
        path=str(zip_path),
        filename=f"{folder.name}.zip",
        media_type="application/zip"
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Запуск FaceSort API v2.0 с улучшенным логированием...")
    print("📱 Откройте http://localhost:8000 в браузере")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
