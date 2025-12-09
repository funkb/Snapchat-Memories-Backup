import re, string, random, threading
from pathlib import Path

files_processed = 0
total_bytes = 0
progress_lock = threading.Lock()

def generate_unique_string(length=4):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def sanitize_json_path(raw: str) -> Path:
    cleaned = raw.strip().strip('"').strip("{}")
    return Path(cleaned)

def safe_mkdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def update_progress(filepath: Path, status_var, progress_var):
    global files_processed, total_bytes
    with progress_lock:
        files_processed += 1
        try:
            total_bytes += filepath.stat().st_size
        except Exception:
            pass
        gb = total_bytes / (1024**3)
        progress_var.set(f"Files processed: {files_processed} | Total size: {gb:.2f} GB")
        status_var.set("Processing…")
