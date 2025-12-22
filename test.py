from pathlib import Path
from src.processor import export_kra_to_versioned_jpg

# CHANGE THIS to any real .kra file you have
KRA_FILE = Path(r"C:\Users\abhay\Pictures\dummyroot\APPLE1.kra")

print("Exporting version 1...")
jpg1 = export_kra_to_versioned_jpg(KRA_FILE)
print("Created:", jpg1)

print("Exporting version 2...")
jpg2 = export_kra_to_versioned_jpg(KRA_FILE)
print("Created:", jpg2)
