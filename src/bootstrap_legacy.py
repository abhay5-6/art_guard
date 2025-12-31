import shutil
import subprocess
from pathlib import Path

from src.config import ART_ROOT, IGNORE_DIRS, JPG_OUTPUT
from src.logger import logger
from src.models.model import generate_base_name

KRITA_EXE = r"C:\Program Files\Krita (x64)\bin\krita.exe"


def bootstrap_legacy_folder():
    logger.info("=" * 60)
    logger.info("ArtGuard legacy bootstrap started")
    logger.info(f"Source folder: {ART_ROOT}")
    logger.info("=" * 60)

    files_by_stem: dict[str, dict[str, Path]] = {}

    for path in ART_ROOT.iterdir():
        if path.is_dir():
            continue

        if path.suffix.lower() not in {".kra", ".jpg", ".jpeg"}:
            continue

        stem = path.stem.lower()
        files_by_stem.setdefault(stem, {})
        files_by_stem[stem][path.suffix.lower()] = path

    for stem, files in files_by_stem.items():
        logger.info(f"[BOOTSTRAP] Processing artwork | stem={stem}")

        temp_dir = JPG_OUTPUT / f"__bootstrap__{stem}"
        temp_dir.mkdir(parents=True, exist_ok=True)

        temp_jpg = temp_dir / "__bootstrap_v001.jpg"

        try:
            # ---- STEP 1: Create initial JPG ----
            if ".jpg" in files or ".jpeg" in files:
                jpg_path = files.get(".jpg") or files.get(".jpeg")
                shutil.copy2(jpg_path, temp_jpg)
                logger.info(
                    f"[BOOTSTRAP] Copied JPG | source={jpg_path.name}"
                )

            elif ".kra" in files:
                kra_path = files[".kra"]
                logger.info(
                    f"[BOOTSTRAP] Exporting KRA | file={kra_path.name}"
                )

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

            else:
                logger.warning(
                    f"[BOOTSTRAP] No usable source found | stem={stem}"
                )
                continue

            # ---- STEP 2: Generate semantic name ----
            base_name = generate_base_name(temp_jpg)

            final_dir = JPG_OUTPUT / base_name
            final_dir.mkdir(parents=True, exist_ok=True)

            name_file = final_dir / "name.txt"
            name_file.write_text(base_name)

            final_jpg = final_dir / f"{base_name}_v001.jpg"
            shutil.move(temp_jpg, final_jpg)

            logger.info(
                f"[BOOTSTRAP] Initialized | folder={base_name} | output={final_jpg.name}"
            )

        except Exception:
            logger.exception(
                f"[BOOTSTRAP] Failed | stem={stem}"
            )
            continue

        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

        # ---- STEP 3: Cleanup legacy JPGs ----
        for ext in (".jpg", ".jpeg"):
            if ext in files:
                try:
                    files[ext].unlink()
                    logger.info(
                        f"[CLEANUP] Removed legacy JPG | file={files[ext].name}"
                    )
                except Exception:
                    logger.warning(
                        f"[CLEANUP] Could not remove JPG | file={files[ext].name}"
                    )

    logger.info("=" * 60)
    logger.info("ArtGuard legacy bootstrap completed")
    logger.info("=" * 60)


if __name__ == "__main__":
    bootstrap_legacy_folder()
