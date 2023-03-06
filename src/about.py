import tkinter as tk
import os
from translation import _

# Class to show about when the program is first run
class About:
    def __init__(self, master):
        # Create a new window
        self.master = master
        self.icon_path = os.path.abspath("icon.ico")

        # Show alert
        self.show_about()

    # Close the window
    def close(self):
        self.about.destroy()

    # Show the about
    def show_about(self):
        # Create a new window
        self.about = tk.Toplevel(self.master)
        self.about.title(_("About"))
        self.about.iconbitmap(self.icon_path)
        self.about.geometry("380x220")
        self.about.resizable(False, False)
        self.about.protocol("WM_DELETE_WINDOW", self.close)

        # Create a label with a big text to title of about
        self.about_title = tk.Label(self.about)
        self.about_title.pack(pady=10, padx=10)
        # Set the text of the label
        self.about_title["text"] = _("STOP SMOKE")
        # Set font and bold
        self.about_title["font"] = ("Arial", 20, "bold")
        # Set color black
        self.about_title["fg"] = "black"        

        # Create a label to show the about
        self.about_label = tk.Label(self.about)
        self.about_label.pack(pady=10, padx=10)
        # Align the text to the left
        self.about_label["justify"] = "left"
        # Set the text of the label
        self.about_label["text"] = _("""
        Author: Hermann Hahn
        Contact: hermann.h.hahn@gmail.com
        Version: 1.5.0
        License: GNU General Public License v2.0
        Website: https://github.com/hermannhahn/stop-smoke
        Requirements: Windows 7 or higher
        
""")
