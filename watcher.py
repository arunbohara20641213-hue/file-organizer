"""Live watcher for organizing new files in Downloads."""

import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from organizer import DOWNLOADS, organize


class DownloadHandler(FileSystemEventHandler):
    """Watch Downloads and trigger organization on file creation."""

    def on_created(self, event):
        if event.is_directory:
            return

        print(f"[INFO] New file detected: {event.src_path}")
        # Brief wait helps avoid moving partially downloaded files.
        time.sleep(1)
        organize()


if __name__ == "__main__":
    print(f"[INFO] Watching: {DOWNLOADS}")

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, str(DOWNLOADS), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print("[INFO] Stopped watching.")

    observer.join()
