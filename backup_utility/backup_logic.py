import os
import logging
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("backup.log", encoding="utf-8")
    ]
)

def create_multi_backup(sources: List[Path], destination: Path) -> str:
    """Создает ОДИН ZIP-архив, содержащий ВСЕ выбранные папки."""
    # Оставляем только те папки, которые реально существуют и не пустые
    valid_sources = []
    for src in sources:
        if src.exists():
            try:
                if any(os.scandir(src)):
                    valid_sources.append(src)
                else:
                    logging.warning(f"Папка {src.name} пуста и будет пропущена.")
            except Exception:
                pass

    if not valid_sources:
        return "Внимание: Не найдено ни одной существующей или непустой папки для бэкапа."

    destination.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = destination / f"multi_backup_{timestamp}.zip"

    EXCLUDE_DIRS = {".git", "__pycache__", "venv", ".idea", ".vscode"}
    EXCLUDE_FILES = {"backup.log"}

    try:
        has_files_to_add = False
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for source in valid_sources:
                # Проверяем, чтобы папка бэкапов не была внутри копируемой папки
                if destination == source or source in destination.parents:
                    continue

                for root, dirs, files in os.walk(source):
                    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                    for file in files:
                        if file in EXCLUDE_FILES:
                            continue
                        file_path = Path(root) / file
                        
                        # Чтобы внутри ZIP-файла папки не перемешались, 
                        # мы сохраняем имя самой исходной папки как корневое в архиве
                        arcname = Path(source.name) / file_path.relative_to(source)
                        
                        zipf.write(file_path, arcname)
                        has_files_to_add = True
                        
        if not has_files_to_add:
            archive_path.unlink(missing_ok=True)
            return "Внимание: В выбранных папках не найдено подходящих файлов."

        return f"Успех! Общий бэкап создан: {archive_path.name} (Содержит папок: {len(valid_sources)})"
    except Exception as e:
        return f"Критическая ошибка при архивации: {e}"

def clean_old_backups(destination: Path, days: int) -> str:
    """Удаляет архивы старше указанного количества дней."""
    cutoff_time = datetime.now() - timedelta(days=days)
    deleted_count = 0
    try:
        # Проверяем и backup_*, и multi_backup_*
        for pattern in ("backup_*.zip", "multi_backup_*.zip"):
            for file in destination.glob(pattern):
                file_time = datetime.fromtimestamp(file.stat().st_mtime)
                if file_time < cutoff_time:
                    file.unlink()
                    deleted_count += 1
        return f"Очистка завершена. Удалено старых архивов: {deleted_count}"
    except Exception as e:
        return f"Ошибка при очистке: {e}"
