import argparse
from pathlib import Path
from .utils import sanitize_json_path
from .download import download_and_process
from .gui import run_gui

def main():
    parser = argparse.ArgumentParser(description="Download memories and fix disguised ZIP overlays.")
    parser.add_argument("--json", type=str, help="Path to memories JSON file")
    parser.add_argument("--out", type=str, default="downloads", help="Output directory")
    parser.add_argument("--workers", type=int, default=8, help="Max concurrent downloads")
    parser.add_argument("--gui", action="store_true", help="Launch GUI")
    args = parser.parse_args()

    if args.gui or not args.json:
        run_gui(default_output_dir=Path(args.out))
    else:
        json_path = sanitize_json_path(args.json)
        download_and_process(json_path, Path(args.out), max_workers=args.workers)

if __name__ == "__main__":
    main()
