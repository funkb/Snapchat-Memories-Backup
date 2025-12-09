from .download import download_and_process
from pathlib import Path



def run_gui(default_output_dir: Path = Path("downloads")):
    import tkinter as tk
    from tkinter import filedialog, messagebox

    try:
        from tkinterdnd2 import DND_FILES, TkinterDnD
        root = TkinterDnD.Tk()
        dnd_available = True
    except Exception:
        root = tk.Tk()
        dnd_available = False

    root.title("Memories Downloader + Overlay Fix")

    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill="both", expand=True)

    lbl = tk.Label(frame, text="Drag & drop your JSON here or click 'Select JSON'.")
    lbl.pack(anchor="w")

    output_var = tk.StringVar(value=str(default_output_dir))
    out_frame = tk.Frame(frame)
    out_frame.pack(fill="x", pady=(8, 8))
    tk.Label(out_frame, text="Output folder:").pack(side="left")
    out_entry = tk.Entry(out_frame, textvariable=output_var, width=40)
    out_entry.pack(side="left", padx=(6, 6))
    def choose_out():
        folder = filedialog.askdirectory()
        if folder:
            output_var.set(folder)
    tk.Button(out_frame, text="Browse", command=choose_out).pack(side="left")

    status_var = tk.StringVar(value="Waiting for input...")
    status = tk.Label(frame, textvariable=status_var, anchor="w", fg="#333")
    status.pack(fill="x", pady=(8, 4))

    progress_var = tk.StringVar(value="Files processed: 0 | Total size: 0.00 GB")
    progress = tk.Label(frame, textvariable=progress_var, anchor="w", fg="#006400")
    progress.pack(fill="x", pady=(4, 4))

    drop = tk.Label(frame, relief="solid", bd=1, height=6, text="Drop JSON here", fg="#666")
    drop.pack(fill="both", expand=True, pady=(6, 6))

  

    def run_download_with_controls(json_path: Path, output_dir: Path, status_var, progress_var):
        try:
            status_var.set("Processing…")
            download_and_process(json_path, output_dir,
                                 status_var=status_var,
                                 progress_var=progress_var,
                                 max_workers=8)
            if not stop_event.is_set():
                status_var.set("Done.")
                messagebox.showinfo("Complete", "All downloads and processing finished.")
        except Exception as e:
            status_var.set("Error.")
            messagebox.showerror("Error", str(e))


    def handle_json(json_path: Path):
        output_dir = Path(output_var.get())
        stop_event.clear()
        pause_event.set()
        threading.Thread(
            target=run_download_with_controls,
            args=(json_path, output_dir, status_var, progress_var),
            daemon=True
        ).start()

    if dnd_available:
        drop.drop_target_register(DND_FILES)
        def on_drop(event):
            print("Raw drop data:", repr(event.data))
            cleaned = event.data.strip().strip('"{}')
            json_path = Path(cleaned)
            handle_json(json_path)
        drop.dnd_bind('<<Drop>>', on_drop)

    def select_json():
        path = filedialog.askopenfilename(
            title="Select memories JSON",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if path:
            json_path = Path(path)
            handle_json(json_path)

    btn = tk.Button(frame, text="Select JSON", command=select_json)
    btn.pack(pady=(4, 4))

    # --- Pause/Resume/Stop Buttons ---
    def pause_download():
        pause_event.clear()
        status_var.set("Paused")

    def resume_download():
        pause_event.set()
        status_var.set("Resumed")

    def stop_download():
        stop_event.set()
        status_var.set("Stopped")

    ctrl_frame = tk.Frame(frame)
    ctrl_frame.pack(fill="x", pady=(6, 6))
    tk.Button(ctrl_frame, text="Pause", command=pause_download).pack(side="left", padx=4)
    tk.Button(ctrl_frame, text="Resume", command=resume_download).pack(side="left", padx=4)
    tk.Button(ctrl_frame, text="Stop", command=stop_download).pack(side="left", padx=4)

    root.geometry("540x420")
    root.mainloop()

