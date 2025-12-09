from snap_backup.gui import run_gui
from pathlib import Path

if __name__ == "__main__":
    run_gui(default_output_dir=Path("downloads"))
