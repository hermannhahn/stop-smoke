"""
Title: Stop Smoke
Author: Hermann Hahn
License: GPL-3.0
Version: 1.5.2
Date: 2021-03-21
Description: Stop Smoke main script
"""
import tkinter as tk
import gui.app as app

if __name__ == "__main__":

    root = tk.Tk()

    app = app.StopSmokingApp(root)

    app.mainloop()
