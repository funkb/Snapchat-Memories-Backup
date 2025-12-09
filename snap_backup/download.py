import os, requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from .postprocess import fix_disguised_archive
from .utils import sanitize_filename, update_progress, safe_mkdir
from .events import pause_event, stop_event

def decide_extension(url_ext: str, media_type: str) -> str:
    if url_ext:
        return url_ext
    if media_type and media_type.lower() == "image":
        return ".jpg"
    if media_type and media_type.lower() == "video":
        return ".mp4"
    return ".zip"

def download_one(entry: dict, output_dir: Path, session: requests.Session,
                 status_var=None, progress_var=None, timeout: int = 30) -> Path | None:
    date = entry.get("Date")
    url = entry.get("Media Download Url")
    media_type = entry.get("Media Type")

    if not date or not url:
        return None

    safe_date = sanitize_filename(date)
    url_ext = os.path.splitext(url)[1]
    ext = decide_extension(url_ext, media_type)
    filepath = output_dir / f"{safe_date}{ext}"

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        with session.get(url, stream=True, headers=headers, timeout=timeout) as resp:
            resp.raise_for_status()
            with open(filepath, "wb") as f_out:
                for chunk in resp.iter_content(chunk_size=8192):
                    if stop_event.is_set():
                        return None
                    pause_event.wait()
                    if chunk:
                        f_out.write(chunk)
        if status_var and progress_var:
            update_progress(filepath, status_var, progress_var)
        return filepath
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def process_entry(entry, output_dir, session, status_var=None, progress_var=None):
    if stop_event.is_set():
        return
    path = download_one(entry, output_dir, session, status_var, progress_var)
    if path and not stop_event.is_set():
        try:
            fix_disguised_archive(path)
        except Exception as e:
            print(f"Post-process failed for {path.name}: {e}")

def download_and_process(json_file: Path, output_dir: Path,
                         status_var=None, progress_var=None, max_workers: int = 8):
    safe_mkdir(output_dir)
    import json
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("Saved Media", []) if isinstance(data, dict) else data
    session = requests.Session()
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for entry in entries:
            if stop_event.is_set():
                break
            futures.append(executor.submit(process_entry, entry, output_dir, session,
                                           status_var, progress_var))
        for fut in as_completed(futures):
            exc = fut.exception()
            if exc:
                print(f"Task failed: {exc}")
    if stop_event.is_set():
        print("Download stopped by user.")
        return
    print("All downloads and post-processing complete.")
