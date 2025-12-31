import subprocess
from pathlib import Path
import shutil
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
    return path.read_text().strip() if path.exists() else None


def _save_cached_name(output_dir: Path, name: str):
    _name_file(output_dir).write_text(name)

"""
def export_kra_to_versioned_jpg(kra_path: Path) -> Path | None:
    kra_path = Path(kra_path)

    if not kra_path.exists() or kra_path.suffix.lower() != ".kra":
        logger.warning(f"[EXPORT] Invalid path skipped | file={kra_path}")
        return None

    try:
        out_dir = JPG_OUTPUT / kra_path.stem
        out_dir.mkdir(parents=True, exist_ok=True)

        version = _next_version(out_dir)
        base_name = _load_cached_name(out_dir)

        if base_name is None:
            logger.info(f"[NAMING] Generating semantic name | file={kra_path.name}")

            temp_jpg = out_dir / "__temp.jpg"

            subprocess.run(
                [KRITA_EXE, str(kra_path), "--export", "--export-filename", str(temp_jpg)],
                check=True,
            )

            base_name = generate_base_name(temp_jpg)
            _save_cached_name(out_dir, base_name)
            temp_jpg.unlink(missing_ok=True)

            logger.info(
                f"[NAMING] Name resolved | file={kra_path.name} | name={base_name}"
            )

        final_jpg = out_dir / f"{base_name}_v{version:03d}.jpg"

        logger.info(
            f"[EXPORT] Running Krita export | file={kra_path.name} | version=v{version:03d}"
        )

        subprocess.run(
            [KRITA_EXE, str(kra_path), "--export", "--export-filename", str(final_jpg)],
            check=True,
        )

        logger.info(
            f"[EXPORT] Success | file={kra_path.name} | output={final_jpg.name}"
        )

        return final_jpg

    except Exception:
        logger.exception(f"[EXPORT] Failed | file={kra_path.name}")
        return None
"""
def export_kra_to_versioned_jpg(kra_path: Path) -> Path | None:
    kra_path = Path(kra_path)

    if not kra_path.exists() or kra_path.suffix.lower() != ".kra":
        logger.warning(f"[EXPORT] Invalid path skipped | file={kra_path}")
        return None

    try:
        # --------------------------------------------------
        # STEP 1: Temporary working directory (by kra stem)
        # --------------------------------------------------
        temp_dir = JPG_OUTPUT / f"__work__{kra_path.stem}"
        temp_dir.mkdir(parents=True, exist_ok=True)

        name_file = temp_dir / "name.txt"

        # --------------------------------------------------
        # STEP 2: Resolve base name (cached OR BLIP)
        # --------------------------------------------------
        base_name = None

        if name_file.exists():
            base_name = name_file.read_text().strip()
        else:
            logger.info(f"[NAMING] Generating semantic name | file={kra_path.name}")

            temp_jpg = temp_dir / "__temp.jpg"

            subprocess.run(
                [KRITA_EXE, str(kra_path), "--export", "--export-filename", str(temp_jpg)],
                check=True,
            )

            base_name = generate_base_name(temp_jpg)
            name_file.write_text(base_name)
            temp_jpg.unlink(missing_ok=True)

            logger.info(
                f"[NAMING] Name resolved | file={kra_path.name} | name={base_name}"
            )

        # --------------------------------------------------
        # STEP 3: Final directory = semantic name
        # --------------------------------------------------
        final_dir = JPG_OUTPUT / base_name
        final_dir.mkdir(parents=True, exist_ok=True)

        # Move name.txt once
        final_name_file = final_dir / "name.txt"
        if not final_name_file.exists():
            shutil.move(name_file, final_name_file)

        # --------------------------------------------------
        # STEP 4: Versioning
        # --------------------------------------------------
        version = _next_version(final_dir)
        final_jpg = final_dir / f"{base_name}_v{version:03d}.jpg"

        logger.info(
            f"[EXPORT] Running Krita export | file={kra_path.name} | version=v{version:03d}"
        )

        subprocess.run(
            [KRITA_EXE, str(kra_path), "--export", "--export-filename", str(final_jpg)],
            check=True,
        )

        logger.info(
            f"[EXPORT] Success | folder={base_name} | output={final_jpg.name}"
        )

        # --------------------------------------------------
        # STEP 5: Cleanup temp dir
        # --------------------------------------------------
        shutil.rmtree(temp_dir, ignore_errors=True)

        return final_jpg

    except Exception:
        logger.exception(f"[EXPORT] Failed | file={kra_path.name}")
        return None
