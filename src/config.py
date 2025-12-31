from pathlib import Path

# --------------------------------------------------
# Project base directory
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# Art root (user workspace)
# --------------------------------------------------
# Change this if needed by the user
ART_ROOT = Path(r"C:\Users\abhay\Pictures\sketch")


# --------------------------------------------------
# Output directories (gitignored, auto-created)
# --------------------------------------------------
OUTPUT_DIR = BASE_DIR / "output"
JPG_OUTPUT = OUTPUT_DIR / "jpg"
KRA_OUTPUT = OUTPUT_DIR / "kra"


# --------------------------------------------------
# Logs directory (gitignored, auto-created)
# --------------------------------------------------
LOG_DIR = BASE_DIR / "logs"


# --------------------------------------------------
# Supported formats
# --------------------------------------------------
KRA_EXT = ".kra"
JPG_EXT = {".jpg", ".jpeg"}


# --------------------------------------------------
# Ignore directories (by name, not path)
# --------------------------------------------------
IGNORE_DIRS = {
    OUTPUT_DIR.name,
    LOG_DIR.name,
    "__pycache__",
}


# --------------------------------------------------
# Timing / behavior constants
# --------------------------------------------------
EVENT_DELAY = 1.0


# --------------------------------------------------
# Ensure required directories exist
# --------------------------------------------------
for directory in (OUTPUT_DIR, JPG_OUTPUT, KRA_OUTPUT, LOG_DIR):
    directory.mkdir(parents=True, exist_ok=True)
