# Snap Backup (Snapchat Memories Downloader)

Snap Backup is a Python project that helps you download and organize your Snapchat Memories from the exported JSON file. It can fix disguised ZIP overlays, track progress, and provides both a GUI and CLI interface.

---

## ✨ Features
- 📥 Download media files from Snapchat Memories JSON
- 🖼️ Fix disguised ZIP archives containing base + overlay images
- ⏸️ Pause, ▶️ Resume, and ⏹️ Stop downloads
- 🖥️ GUI with drag-and-drop support
- 🛠️ CLI for batch automation
- 🧪 Lightweight tests with `pytest`

---

## 📦 Installation

Clone the repo and install dependencies:


```
git clone https://github.com/yourusername/snap_backup.git
cd snap_backup
pip install -r requirements.txt
```

## 🚀 Usage
GUI Mode:

```
python -m snap_backup.cli --gui
```

- Drag and drop your memories_history.json file into the window, or select it manually.
- Choose an output folder (default: downloads).

CLI Mode:
```
python -m snap_backup.cli --json path/to/memories_history.json --out downloads
```
--workers N : number of concurrent downloads (default 8)
--out PATH : output directory (default downloads)
--gui : launch GUI instead of CLI