import sys
import zipfile
import subprocess
import tempfile
import re
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from win10toast import ToastNotifier

is_rendering = False

if getattr(sys, "frozen", False):
    # if this shit runs as a script then fuck outta here
    base_path = Path(sys._MEIPASS)
else:
    # otherwise if you are running this as a script then idk
    base_path = Path(__file__).parent

ffmpeg_path = base_path / "ffmpeg.exe"


def get_duration(file_path: Path):
    cmd = ["ffmpeg", "-i", str(file_path)]
    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output = result.stderr

    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", output)
    if not match:
        return None

    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = float(match.group(3))

    return hours * 3600 + minutes * 60 + seconds


def convert_zip_to_video(zip_path: Path, progress_var):
    global is_rendering
    is_rendering = True

    try:
        output_path = zip_path.with_suffix(".mp4")
        workdir = Path(tempfile.mkdtemp())

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(workdir)

        mp3_file = next(workdir.glob("*.mp3"), None)
        cdg_file = next(workdir.glob("*.cdg"), None)

        if not mp3_file or not cdg_file:
            raise RuntimeError("ZIP must contain MP3 and CDG.")

        total_duration = get_duration(mp3_file)
        if not total_duration:
            raise RuntimeError("Could not detect duration.")

        encoder = "h264_nvenc" if encoder_var.get() == "nvenc" else "libx264"

        cmd = [
            str(ffmpeg_path), "-y",
            "-i", str(mp3_file),
            "-i", str(cdg_file),
            "-vf", "scale=-1:1080:flags=neighbor,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black",
            "-r", "60",
            "-c:v", encoder,
            "-preset", "fast",
            "-qp", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            str(output_path)
        ]

        process = subprocess.Popen(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        time_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")

        while True:
            line = process.stderr.readline()
            if not line:
                break

            match = time_pattern.search(line)
            if match:
                h, m, s = match.groups()
                current = int(h) * 3600 + int(m) * 60 + float(s)
                percent = min((current / total_duration) * 100, 100)
                progress_var.set(percent)

        process.wait()
        progress_var.set(100)

        # Toast notification
        toaster = ToastNotifier()
        toaster.show_toast(
            "CD+G render finished",
            f"{output_path.name} is ready",
            duration=5,
            threaded=True
        )

        status_label.config(text="Done! Drop another .zip.")

    except Exception as e:
        status_label.config(text=f"Error: {e}")

    finally:
        is_rendering = False
        progress_var.set(0)


def start_conversion(zip_path):
    threading.Thread(
        target=convert_zip_to_video,
        args=(zip_path, progress_var),
        daemon=True
    ).start()


def drop(event):
    global is_rendering
    if is_rendering:
        status_label.config(text="Already rendering. Please wait.")
        return

    file_path = Path(event.data.strip("{}"))

    if file_path.suffix.lower() != ".zip":
        status_label.config(text="Please drop a ZIP file.")
        return

    status_label.config(text=f"Rendering: {file_path.name}")
    progress_var.set(0)
    start_conversion(file_path)

# the gooey GUI
root = TkinterDnD.Tk()
root.title("CDG2VideoGUI")
root.resizable(False, False)

progress_var = tk.DoubleVar()

encoder_var = tk.StringVar(value="nvenc")  # default to NVENC

drop_area = tk.Label(
    root,
    text="Drag and Drop your .zip here",
    relief="ridge",
    width=40,
    height=4
)
drop_area.pack(pady=15)

encoder_frame = tk.LabelFrame(root, text="Video Encoder")
encoder_frame.pack(pady=5)

tk.Radiobutton(
    encoder_frame, text="NVENC (GPU, fast)", variable=encoder_var, value="nvenc"
).pack(side=tk.LEFT, padx=5)

tk.Radiobutton(
    encoder_frame, text="CPU (libx264, slower)", variable=encoder_var, value="cpu"
).pack(side=tk.LEFT, padx=5)


drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind("<<Drop>>", drop)

progress_bar = ttk.Progressbar(
    root,
    variable=progress_var,
    maximum=100,
    length=350
)
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="Waiting for ZIP...")
status_label.pack(pady=5)

# Center the window
root.update_idletasks()
window_width = 420
window_height = 250  # adjust for drop area + progress bar
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()
