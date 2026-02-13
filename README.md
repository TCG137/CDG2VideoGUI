![CDG2VideoGUI](img/readme.png)

Zipped MP3+G/CDG+MP3 to MP4 converter with drag-and-drop GUI written in Python.

Watch CDG2VideoGUI in action:

[![Watch Demo on YouTube](https://img.youtube.com/vi/6sXRn59I8F0/0.jpg)](https://youtu.be/6sXRn59I8F0)

---

## Features

- Drag & drop ZIP files containing MP3 + CDG.
- Select encoder: **NVENC (GPU)** for fast encoding or **libx264 (CPU)** for compatibility.
- Built-in progress bar and Windows toast notification when done.
- Standalone executable version available (FFmpeg bundled)
- Renders compact MP4 videos (~25 MB) at 1080p60 with 2,000 kb/s VBR.
--- 

## Cool, so how do I use it?

- Drag a ZIP file onto the window.
- Select encoder if needed.
- Wait for the progress bar to finish.
- MP4 will be saved in the same folder as the ZIP.

---

## Demo ZIP

A small demo ZIP file is included in this repository and in the release so you can see how the tool works without needing your own CDG files.

---

### Running the Python Script

```bash
python DragCDGGUI.py
```

## Requirements for running the script

Python 3.10+

tkinter
tkinterdnd2
win10toast (python)
ffmpeg (executable) 

If using the prebuilt executable, ffmpeg is not required.

---

## Notes
- Only ZIP files with an MP3 and a CDG file are supported.
- GPU encoding requires a compatible NVIDIA GPU. Sorry AMD users.
- Tested with FFmpeg version 8.0.1.

---

## License

This project is licensed under the MIT License
