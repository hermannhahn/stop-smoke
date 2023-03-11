"""
Title: About Module
Author: Hermann Hahn
License: GPL-2.0
Version: 1.5.2
Description: This module contains the about GUI
"""
import tkinter as tk
import os
from modules.app_translation import _ # pylint: disable=import-error,no-name-in-module

class About:
    """About GUI class"""

    def __init__(self, master):
        """Initialize the class"""

        # Set variables
        self.master = master
        self.icon_path = os.path.abspath("icon.ico")

        # Show about
        self.show_about()


    def close(self):
        """Close the about window"""
        self.about.destroy()


    def show_about(self):
        """Show the about window"""

        # Create about window
        self.about = tk.Toplevel(self.master)
        self.about.title(_("About"))
        self.about.iconbitmap(self.icon_path)
        self.about.geometry("380x220")
        self.about.resizable(False, False)

        # Set window close function
        self.about.protocol("WM_DELETE_WINDOW", self.close)

        # Create about title
        self.about_title = tk.Label(self.about)
        self.about_title["text"] = _("STOP SMOKE")
        self.about_title["fg"] = "black"
        self.about_title["font"] = ("Arial", 20, "bold")

        # Create about label
        self.about_label = tk.Label(self.about)
        self.about_label["justify"] = "left"
        self.about_label["fg"] = "black"
        self.about_label["font"] = ("Arial", 12)

        # Set about text
        self.about_label["text"] = _("""
        Author: Hermann Hahn
        Contact: hermann.h.hahn@gmail.com
        Version: 1.5.1
        License: GNU General Public License v2.0
        Website: https://github.com/hermannhahn/stop-smoke
        Requirements: Windows 7 or higher
        """)

        # Pack title
        self.about_title.pack(padx=10, pady=10)

        # Pack label
        self.about_label.pack()
