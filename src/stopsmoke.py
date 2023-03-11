"""
Title: Stop Smoke
Author: Hermann Hahn
License: GPL-2.0
Version: 1.5.2
Description: Stop Smoke main script
"""
import tkinter as tk
import gui.app as app

# App Main script
if __name__ == "__main__":

    # Create window
    root = tk.Tk()

    # Create app
    app = app.StopSmokingApp(root)

    # Start app
    app.mainloop()
