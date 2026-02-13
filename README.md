![CDG2VideoGUI](img/readme.png)

Zipped MP3+G/CDG+MP3 to MP4 converter with drag-and-drop GUI written in Python.

---

## Features

- Drag & drop ZIP files containing MP3 + CDG.
- Select encoder: **NVENC (GPU)** for fast encoding or **libx264 (CPU)** for compatibility.
- Built-in progress bar and Windows toast notification when done.
- Standalone executable version available (FFmpeg bundled)

--- 

## Cool, so how do I use it?

- Drag a ZIP file onto the window.
- Select encoder if needed.
- Wait for the progress bar to finish.
- MP4 will be saved in the same folder as the ZIP.

---

### Running the Python Script

```bash
python DragCDGGUI.py
```

## Requirements for running the script

Python 3.10+

tkinter
tkinterdnd2
win10toast
ffmpeg

If using the prebuilt executable, ffmpeg is not required.
