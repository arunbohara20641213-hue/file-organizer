"""Configuration for file type mappings and paths."""

from pathlib import Path

FILE_TYPES = {
    "PDFs": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java"],
    "Excel": [".xlsx", ".xls", ".csv"],
    "Word": [".doc", ".docx"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Others": [],
}

IGNORED_FILE_NAMES = {
    "desktop.ini",
    "thumbs.db",
}

TEMP_EXTENSIONS = {
    ".tmp",
    ".part",
    ".crdownload",
    ".download",
    ".partial",
}

DEBOUNCE_SECONDS = 2.0

DOWNLOADS = Path.home() / "Downloads"
LOG_FILE = Path(__file__).resolve().parent / "log.txt"
