"""
Title: Stop Smoke Updater
Author: Hermann Hahn
License: GPL-2.0
Version: 1.5.2
Description: Updater script for the Stop Smoke app
"""
import urllib.request
import zipfile
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from modules.app_update_translation import _

# Change this to the URL of the latest release
URL = "https://github.com/hermannhahn/stop-smoke/releases/download/latest/stopsmoke.zip"
ZIP_FILE = "stopsmoke.zip"

# Window setup
root = tk.Tk()
root.title(_("Stop Smoke Update"))
root.iconbitmap(os.path.abspath("icon.ico"))
root.geometry("300x100")
root.resizable(False, False)

# Center window
root.update_idletasks()

# Progress bar setup
progress_label = tk.Label(root, text="")
progress_label.pack(anchor="w")

progressbar = Progressbar(root, orient=tk.HORIZONTAL, length=250, mode='determinate')
progressbar.pack(pady=10)


def update_app():
    """Update the app"""

    # Update status
    progress_label.config(text=_("\n     Downloading update..."))

    # Get file size for progress bar
    with urllib.request.urlopen(URL) as response:
        file_size = int(response.info().get("Content-Length"))

    # Download file with progress bar
    with urllib.request.urlopen(URL) as response, open(ZIP_FILE, "wb") as out_file:
        data = response.read()
        downloaded_size = 0
        block_size = 1024
        while data:
            out_file.write(data)
            downloaded_size += len(data)
            progress = int((downloaded_size / file_size) * 100)
            progressbar.config(value=progress)
            root.update_idletasks()
            data = response.read(block_size)

    # Update status
    progress_label.config(text=_("\n     Extracting update..."))

    # Extract files with progress bar
    with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
        file_list = zip_ref.namelist()
        progressbar.config(maximum=len(file_list), value=0)
        for i, file in enumerate(file_list):
            zip_ref.extract(file)
            progress = int(((i + 1) / len(file_list)) * 100)
            progressbar.config(value=progress)
            root.update_idletasks()

    # Update status
    progress_label.config(text=_("\n     Removing temporary files..."))

    # Remove temporary files
    os.remove(ZIP_FILE)

    # Update status
    progress_label.config(text=_("\n     Update finished."))

    # Restart app
    messagebox.showinfo(_("Update successful"), _("Update successful. The app will now restart."))
    subprocess.Popen("stopsmoke.exe")
    close_app()


def close_app():
    """Quit the app"""
    root.destroy()
    sys.exit()

# Start update
root.after(100, update_app)
root.mainloop()

# Close app on window close
root.protocol("WM_DELETE_WINDOW", close_app)
