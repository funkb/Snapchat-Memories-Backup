## Snapchat Memories Downloader

This is a Python project that helps you download and organize your Snapchat Memories from the exported JSON file. It can fix disguised ZIP overlays, track progress, and provides both a GUI and CLI interface.

When requesting your data to be exported from Snapchat, make sure to 'include JSON files' with your download. 

## ✨ Features
- 📥 Download media files from Snapchat Memories JSON
- 🖼️ Fix disguised ZIP archives containing base + overlay images
- ⏸️ Pause, ▶️ Resume, and ⏹️ Stop downloads
- 🖥️ GUI with drag-and-drop support
- 🛠️ CLI for batch automation
- 🧪 Lightweight tests with `pytest`

## 📦 Installation
Clone the repo and install dependencies:
```
git clone https://github.com/yourusername/snap_backup.git
cd snap_backup
pip install -r requirements.txt
```

Dependencies:
- requests
- Pillow
- tkinterdnd2

## 🚀 Usage

## GUI Mode
```
python -m snap_backup.cli --gui
```
- Drag and drop your `memories_history.json` file into the window, or select it manually.
- Choose an output folder (default: downloads).
- Use the buttons to Pause, Resume, or Stop downloads.

## CLI Mode
```
python -m snap_backup.cli --json path/to/memories_history.json --out downloads
```
```
Options:
--workers N : number of concurrent downloads (default 8)
--out PATH : output directory (default downloads)
--gui : launch GUI instead of CLI
```

## 🗂 Project Structure
```
snap_backup/
├── snap_backup/
│   ├── __init__.py
│   ├── cli.py
│   ├── gui.py
│   ├── download.py
│   ├── postprocess.py
│   ├── utils.py
│   └── events.py
├── tests/
│   └── test_download.py
├── requirements.txt
└── README.md
```

## 🧪 Running Tests
Install pytest if needed:
```
pip install pytest
```
Run tests from the project root:
```
pytest
```

## 🏗 Building Executables
You can create standalone binaries with PyInstaller:
```
pip install pyinstaller
```

```
pyinstaller --onefile --windowed snap_backup/gui_entry.py --name SnapBackup
```
This produces dist/SnapBackup.exe which launches the GUI directly when double‑clicked.


## 📄 License
MIT License
