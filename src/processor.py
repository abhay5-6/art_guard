import subprocess
from pathlib import Path

from src.logger import logger
from src.config import JPG_OUTPUT
from src.models.model import generate_base_name

KRITA_EXE = r"C:\Program Files\Krita (x64)\bin\krita.exe"


def _next_version(output_dir: Path) -> int:
    existing = sorted(output_dir.glob("*_v*.jpg"))
    if not existing:
        return 1
    last = existing[-1].stem
    return int(last.split("_v")[-1]) + 1


def _name_file(output_dir: Path) -> Path:
    return output_dir / "name.txt"


def _load_cached_name(output_dir: Path) -> str | None:
    path = _name_file(output_dir)
    if path.exists():
        return path.read_text().strip()
    return None


def _save_cached_name(output_dir: Path, name: str):
    _name_file(output_dir).write_text(name)


def export_kra_to_versioned_jpg(kra_path: Path) -> Path:
    kra_path = Path(kra_path)

    if not kra_path.exists() or kra_path.suffix.lower() != ".kra":
        raise ValueError(f"Invalid .kra file: {kra_path}")

    out_dir = JPG_OUTPUT / kra_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    version = _next_version(out_dir)

    # ---- base name resolution (CACHED) ----
    base_name = _load_cached_name(out_dir)

    if base_name is None:
        # BLIP runs ONLY ONCE in lifetime
        temp_jpg = out_dir / "__temp.jpg"

        subprocess.run(
            [
                KRITA_EXE,
                str(kra_path),
                "--export",
                "--export-filename",
                str(temp_jpg),
            ],
            check=True,
        )

        base_name = generate_base_name(temp_jpg)
        _save_cached_name(out_dir, base_name)
        temp_jpg.unlink()

    # ---- final export ----
    final_jpg = out_dir / f"{base_name}_v{version:03d}.jpg"
    logger.info(f"Running Krita export for {kra_path}")


    subprocess.run(
        [
            KRITA_EXE,
            str(kra_path),
            "--export",
            "--export-filename",
            str(final_jpg),
        ],
        check=True,
    )

    return final_jpg
