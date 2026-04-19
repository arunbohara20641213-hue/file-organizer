"""Live watcher for organizing new files in Downloads."""

import time
import threading

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config import DEBOUNCE_SECONDS
from organizer import DOWNLOADS, organize


class DownloadHandler(FileSystemEventHandler):
    """Watch Downloads and trigger organization on file creation."""

    def __init__(self):
        super().__init__()
        self._debounce_lock = threading.Lock()
        self._debounce_timer = None

    def _schedule_organize(self):
        with self._debounce_lock:
            if self._debounce_timer is not None:
                self._debounce_timer.cancel()

            self._debounce_timer = threading.Timer(DEBOUNCE_SECONDS, organize)
            self._debounce_timer.daemon = True
            self._debounce_timer.start()

    def on_created(self, event):
        if event.is_directory:
            return

        print(f"[INFO] New file detected: {event.src_path}")
        self._schedule_organize()

    def on_moved(self, event):
        if event.is_directory:
            return

        print(f"[INFO] File moved into Downloads: {event.dest_path}")
        self._schedule_organize()


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
