import time
from pathlib import Path
from src.logger import logger


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.config import ART_ROOT, IGNORE_DIRS
from src.processor import export_kra_to_versioned_jpg

DEBOUNCE_SECONDS = 1.0


def wait_until_stable(path: Path, checks=3, delay=0.3) -> bool:
    """
    Wait until file size stops changing.
    Prevents reading half-written .kra files.
    """
    last_size = -1

    for _ in range(checks):
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return False

        if size == last_size:
            return True

        last_size = size
        time.sleep(delay)

    return True


class KritaSaveHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_event_time = {}

    def on_modified(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)

        # Only care about .kra files
        if path.suffix.lower() != ".kra":
            return

        # Ignore unwanted directories
        if any(part in IGNORE_DIRS for part in path.parts):
            return

        now = time.time()
        last_time = self._last_event_time.get(path)

        # Debounce
        if last_time and (now - last_time) < DEBOUNCE_SECONDS:
            return

        self._last_event_time[path] = now

        print(f"[WATCHER] Save detected: {path.name}")
        logger.info(f"Save detected: {path}")

        # Wait for file to finish writing
        if not wait_until_stable(path):
            print("[WATCHER] File not stable, skipping")
            return

        try:
            export_kra_to_versioned_jpg(path)
            print("[WATCHER] Export complete")
        except Exception as e:
            print(f"[WATCHER] Error: {e}")
            logger.error(f"Export failed for {path}: {e}")


def start_watcher():
    print(f"[WATCHER] Watching: {ART_ROOT}")
    

    event_handler = KritaSaveHandler()
    observer = Observer()
    observer.schedule(event_handler, str(ART_ROOT), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_watcher()
