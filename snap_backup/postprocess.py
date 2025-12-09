import shutil, zipfile, time
from pathlib import Path
from PIL import Image
from .utils import generate_unique_string, safe_mkdir

def overlay_images(base_path: Path, overlay_path: Path, output_path: Path):
    base = Image.open(base_path).convert("RGBA").copy()
    overlay = Image.open(overlay_path).convert("RGBA").copy()
    if overlay.size != base.size:
        overlay = overlay.resize(base.size)
    combined = Image.alpha_composite(base, overlay)
    combined.convert("RGB").save(output_path, "JPEG")

def fix_disguised_archive(downloaded_path: Path):
    if downloaded_path.suffix.lower() != ".jpg":
        return
    try:
        with open(downloaded_path, 'rb') as f:
            if f.read(4) != b'PK\x03\x04':
                return
    except Exception:
        return

    original_base = downloaded_path.with_suffix("")
    zip_path = original_base.with_suffix(".zip")
    temp_dir = downloaded_path.parent / f"temp_extract_{generate_unique_string(6)}"
    safe_mkdir(temp_dir)

    try:
        time.sleep(0.2)
        downloaded_path.rename(zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(temp_dir)

        extracted_files = [p for p in temp_dir.iterdir() if p.is_file()]
        base_file = next((p for p in extracted_files if p.name.lower().endswith("-main.jpg")), None)
        overlay_file = next((p for p in extracted_files if p.name.lower().endswith("-overlay.png")), None)

        output_jpg = original_base.with_suffix(".jpg")

        if base_file and overlay_file:
            overlay_images(base_file, overlay_file, output_jpg)
        elif base_file:
            shutil.move(str(base_file), str(output_jpg))
        else:
            zip_path.rename(output_jpg)
    finally:
        if zip_path.exists():
            zip_path.unlink(missing_ok=True)
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
