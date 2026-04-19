"""Core logic for organizing files in the Downloads folder."""

import ctypes
import logging
import shutil
import threading
from pathlib import Path

from config import DOWNLOADS, FILE_TYPES, IGNORED_FILE_NAMES, LOG_FILE, TEMP_EXTENSIONS

ORGANIZE_LOCK = threading.Lock()

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


def get_folder(extension: str) -> str:
    """Return destination folder name based on file extension."""
    ext = extension.lower()
    for folder, extensions in FILE_TYPES.items():
        if ext in extensions:
            return folder
    return "Others"


def get_unique_target(target_folder: Path, file_name: str) -> Path:
    """Build a non-conflicting destination path for duplicate filenames."""
    candidate = target_folder / file_name
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix

    copy_index = 1
    while True:
        if copy_index == 1:
            copy_name = f"{stem}_copy{suffix}"
        else:
            copy_name = f"{stem}_copy{copy_index}{suffix}"

        candidate = target_folder / copy_name
        if not candidate.exists():
            return candidate

        copy_index += 1


def is_hidden_or_system_file(file_path: Path) -> bool:
    """Return True if file has hidden or system attribute on Windows."""
    if not hasattr(ctypes, "windll"):
        return False

    attributes = ctypes.windll.kernel32.GetFileAttributesW(str(file_path))
    if attributes == -1:
        return False

    file_attribute_hidden = 0x2
    file_attribute_system = 0x4
    return bool(attributes & (file_attribute_hidden | file_attribute_system))


def should_skip_file(file_path: Path) -> bool:
    """Return True for hidden/system/temp files that should not be moved."""
    name_lower = file_path.name.lower()

    if name_lower in IGNORED_FILE_NAMES:
        return True

    if name_lower.startswith("."):
        return True

    if file_path.suffix.lower() in TEMP_EXTENSIONS:
        return True

    return is_hidden_or_system_file(file_path)


def move_with_conflict_resolution(file_path: Path, target_folder: Path) -> Path:
    """Move file without overwrite, retrying with copy suffix if needed."""
    target_path = get_unique_target(target_folder, file_path.name)

    while True:
        try:
            shutil.move(str(file_path), str(target_path))
            return target_path
        except FileExistsError:
            target_path = get_unique_target(target_folder, file_path.name)
        except shutil.Error as exc:
            if "already exists" in str(exc).lower():
                target_path = get_unique_target(target_folder, file_path.name)
                continue
            raise


def organize() -> None:
    """Move files from Downloads into category subfolders."""
    if not DOWNLOADS.exists():
        print(f"[ERROR] Downloads folder not found: {DOWNLOADS}")
        return

    with ORGANIZE_LOCK:
        for item in DOWNLOADS.iterdir():
            if not item.is_file():
                continue

            if should_skip_file(item):
                logging.info("Skipped: %s", item.name)
                continue

            folder_name = get_folder(item.suffix)
            target_folder = DOWNLOADS / folder_name
            target_folder.mkdir(exist_ok=True)

            try:
                target_path = move_with_conflict_resolution(item, target_folder)
                logging.info("Moved: %s -> %s/", target_path.name, folder_name)
                print(f"[OK] Moved: {target_path.name} -> {folder_name}/")
            except PermissionError:
                logging.info("Skipped (in use): %s", item.name)
                print(f"[WARN] Skipped in-use file: {item.name}")
            except OSError as exc:
                logging.info("Failed to move %s: %s", item.name, exc)
                print(f"[ERROR] Failed to move {item.name}: {exc}")


if __name__ == "__main__":
    organize()
