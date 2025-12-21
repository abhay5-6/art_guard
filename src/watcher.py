import time
from pathlib import Path
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.config import ART_ROOT, IGNORE_DIRS
from src.processor import export_kra_to_versioned_jpg


def placeholder_name_generator(kra_path: Path) -> str:
    """
    PLACEHOLDER for future AI-based name generation.
    For now, returns a timestamp-based name.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


class KritaSaveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)

        # Ignore non-kra files
        if path.suffix.lower() != ".kra":
            return

        # Ignore unwanted directories
        if any(part in IGNORE_DIRS for part in path.parts):
            return

        print(f"[WATCHER] Detected save: {path}")

        try:
            export_kra_to_versioned_jpg(path)
            print(f"[WATCHER] Exported JPEG for {path.name}")
        except Exception as e:
            print(f"[WATCHER] Error processing {path}: {e}")


def start_watcher():
    print(f"[WATCHER] Watching directory: {ART_ROOT}")

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
