"""
Module that contains the main program logic for Stop Smoke, an app that helps smokers quit smoking.

Usage:
    python stop_smoke.py
"""
import tkinter as tk
import os
from translation import _


class About:
    """
    Class responsible for displaying information about the program when it is first run.
    """

    def __init__(self, master):
        """
        Creates a new window to display information about the program.

        :param master: Tkinter object
        """
        self.master = master
        self.icon_path = os.path.abspath("icon.ico")


        self.show_about()


    def close(self):
        """
        Closes the program window.
        """
        self.about.destroy()


    def show_about(self):
        """
        Creates a new window to display information about the program.
        """
        self.about = tk.Toplevel(self.master)
        self.about.title(_("About"))
        self.about.iconbitmap(self.icon_path)
        self.about.geometry("380x220")
        self.about.resizable(False, False)

        self.about.protocol("WM_DELETE_WINDOW", self.close)


        self.about_title = tk.Label(self.about)
        self.about_title.pack(pady=10, padx=10)


        self.about_title["text"] = _("STOP SMOKE")

        self.about_title["font"] = ("Arial", 20, "bold")

        self.about_title["fg"] = "black"


        self.about_label = tk.Label(self.about)
        self.about_label.pack(pady=10, padx=10)

        self.about_label["justify"] = "left"

        self.about_label["text"] = _("""
        Author: Hermann Hahn
        Contact: hermann.h.hahn@gmail.com
        Version: 1.5.0
        License: GNU General Public License v2.0
        Website: https://github.com/hermannhahn/stop-smoke
        Requirements: Windows 7 or higher
       
""")
