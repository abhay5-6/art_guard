import subprocess
from pathlib import Path

from src.config import JPG_OUTPUT

KRITA_EXE = r"C:\Program Files\Krita (x64)\bin\krita.exe"


def _next_version(output_dir: Path, stem: str) -> int:
    """
    Find the next available version number: v001, v002, ...
    """
    existing = sorted(output_dir.glob(f"{stem}_v*.jpg"))
    if not existing:
        return 1

    last = existing[-1].stem  # e.g. APPLE1_v003
    try:
        return int(last.split("_v")[-1]) + 1
    except ValueError:
        return len(existing) + 1


def export_kra_to_versioned_jpg(kra_path: Path) -> Path:
    """
    Export a flattened JPEG from a .kra using Krita CLI.
    Creates a new versioned JPG on every call.
    """
    kra_path = Path(kra_path)

    if not kra_path.exists() or kra_path.suffix.lower() != ".kra":
        raise ValueError(f"Invalid .kra file: {kra_path}")

    artwork_name = kra_path.stem

    # Output directory for this artwork
    out_dir = JPG_OUTPUT / artwork_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Decide version
    version = _next_version(out_dir, artwork_name)
    output_jpg = out_dir / f"{artwork_name}_v{version:03d}.jpg"

    # Krita CLI command (exactly what worked in PowerShell)
    cmd = [
        KRITA_EXE,
        str(kra_path),
        "--export",
        "--export-filename",
        str(output_jpg),
    ]

    subprocess.run(cmd, check=True)

    return output_jpg
