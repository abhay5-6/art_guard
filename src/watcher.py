import time
from pathlib import Path
from threading import Timer

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.logger import logger
from src.config import ART_ROOT, IGNORE_DIRS
from src.processor import export_kra_to_versioned_jpg

EXPORT_IDLE_SECONDS = 2.5


class KritaSaveHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_event_time: dict[Path, float] = {}
        self._timers: dict[Path, Timer] = {}

    def on_modified(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)

        if path.suffix.lower() != ".kra":
            return

        if any(part in IGNORE_DIRS for part in path.parts):
            return

        self._last_event_time[path] = time.time()

        logger.info(f"[EVENT] Save detected | file={path.name}")

        if path in self._timers:
            self._timers[path].cancel()
            logger.info(f"[CANCEL] Pending export canceled | file={path.name}")

        timer = Timer(
            EXPORT_IDLE_SECONDS,
            self._export_safe,
            args=(path,),
        )

        self._timers[path] = timer
        logger.info(
            f"[SCHEDULE] Export scheduled | file={path.name} | idle={EXPORT_IDLE_SECONDS}s"
        )
        timer.start()

    def _export_safe(self, path: Path):
        logger.info(f"[EXPORT] Starting | file={path.name}")

        try:
            result = export_kra_to_versioned_jpg(path)

            if result:
                logger.info(
                    f"[EXPORT] Completed | file={path.name} | output={result.name}"
                )
            else:
                logger.warning(
                    f"[EXPORT] Skipped | file={path.name} | reason=invalid or missing"
                )

        except Exception:
            logger.exception(f"[EXPORT] Unexpected failure | file={path.name}")


def start_watcher():
    logger.info("=" * 60)
    logger.info("ArtGuard watcher starting")
    logger.info(f"Watching directory: {ART_ROOT}")
    logger.info("=" * 60)

    event_handler = KritaSaveHandler()
    observer = Observer()
    observer.schedule(event_handler, str(ART_ROOT), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("ArtGuard watcher stopped manually")
        observer.stop()
    except Exception:
        logger.exception("ArtGuard watcher crashed")
        import os
        os.system(
            'powershell -command '
            '"Add-Type -AssemblyName System.Windows.Forms; '
            '[System.Windows.Forms.MessageBox]::Show('
            '\'ArtGuard watcher crashed. Check logs.\', '
            '\'ArtGuard\', '
            '\'OK\', '
            '\'Error\')"'
            )

        observer.stop()


    observer.join()


if __name__ == "__main__":
    start_watcher()
