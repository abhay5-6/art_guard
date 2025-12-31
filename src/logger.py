import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "events.log"
CONSOLE_LOG_FILE = LOG_DIR / "watcher_console.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.FileHandler(CONSOLE_LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger("artguard")
