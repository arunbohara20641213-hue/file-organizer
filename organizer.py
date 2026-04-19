"""Core logic for organizing files in the Downloads folder."""

import logging
import shutil
from pathlib import Path

from config import DOWNLOADS, FILE_TYPES, LOG_FILE

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


def organize() -> None:
    """Move files from Downloads into category subfolders."""
    if not DOWNLOADS.exists():
        print(f"[ERROR] Downloads folder not found: {DOWNLOADS}")
        return

    for item in DOWNLOADS.iterdir():
        if not item.is_file():
            continue

        folder_name = get_folder(item.suffix)
        target_folder = DOWNLOADS / folder_name
        target_folder.mkdir(exist_ok=True)

        target_path = get_unique_target(target_folder, item.name)

        try:
            shutil.move(str(item), str(target_path))
            logging.info("Moved: %s -> %s/", item.name, folder_name)
            print(f"[OK] Moved: {item.name} -> {folder_name}/")
        except PermissionError:
            logging.info("Skipped (in use): %s", item.name)
            print(f"[WARN] Skipped in-use file: {item.name}")
        except OSError as exc:
            logging.info("Failed to move %s: %s", item.name, exc)
            print(f"[ERROR] Failed to move {item.name}: {exc}")


if __name__ == "__main__":
    organize()
