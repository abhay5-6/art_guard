from pathlib import Path

#giving art root directory path
ART_ROOT = Path(r"C:\Users\abhay\Pictures\dummyroot")

#assign project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

#assign output directories path
OUTPUT_DIR = BASE_DIR / "output"
KRA_OUTPUT = OUTPUT_DIR / "kra"
JPG_OUTPUT = OUTPUT_DIR / "jpg"

#SUPPORTED FORMATS
KRA_EXT = ".kra"
JPG_EXT = [".jpg",".jpeg"]

# Ignore folders 
IGNORE_DIRS = {OUTPUT_DIR.name, "logs", "__pycache__"}

# Debounce time 
EVENT_DELAY = 1.0

