"""
Module to show about when the user
clicks on the instructions button
"""
import tkinter as tk
import os
from modules.translation import _

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
        self.about_label = tk.Label(self.about)

        self.about_title["fg"] = "black"
        self.about_title["font"] = ("Arial", 20, "bold")
        self.about_label["justify"] = "left"

        self.about_title["text"] = _("STOP SMOKE")
        self.about_label["text"] = _("""
        Author: Hermann Hahn
        Contact: hermann.h.hahn@gmail.com
        Version: 1.5.1
        License: GNU General Public License v2.0
        Website: https://github.com/hermannhahn/stop-smoke
        Requirements: Windows 7 or higher
        """)

        self.about_title.pack(padx=10, pady=10)
        self.about_label.pack()
