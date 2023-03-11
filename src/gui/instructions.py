"""
Title: Instructions Module
Author: Hermann Hahn
License: GPL-2.0
Version: 1.5.2
Description: This module contains the instructions GUI
"""
import tkinter as tk
import os
from modules.app_translation import _ # pylint: disable=import-error,no-name-in-module

class Instructions:
    """Class to show instructions when the program is first run"""

    def __init__(self, master):
        """Initialize the instructions window"""

        # Set variables
        self.master = master
        self.icon_path = os.path.abspath("icon.ico")

        # Show instructions
        self.show_instructions()

    def close(self):
        """Close the instructions window"""
        self.instructions.destroy()

    def show_instructions(self):
        """Show the instructions window"""

        # Create instructions window
        self.instructions = tk.Toplevel(self.master)
        self.instructions.title(_("Instructions"))
        self.instructions.iconbitmap(self.icon_path)
        self.instructions.geometry("540x250")
        self.instructions.resizable(False, False)

        # Set window close function
        self.instructions.protocol("WM_DELETE_WINDOW", self.close)

        # Create instructions title
        self.instructions_title = tk.Label(self.instructions)
        self.instructions_title["text"] = _("STOP SMOKE")
        self.instructions_title["fg"] = "black"
        self.instructions_title["font"] = ("Arial", 20, "bold")

        # Create instructions label
        self.instructions_label = tk.Label(self.instructions)
        self.instructions_label["fg"] = "black"
        self.instructions_label["font"] = ("Arial", 12)
        
        # Set instructions text
        self.instructions_label["text"] = _("""
        Welcome!

        This app will help you quit smoking by increasing the wait time every day.
        Every time you smoke, click the «Smoke» button to start the timer.

        The app will say how much time you have left before you can smoke again.

        Good luck!
        """)

        # Pack instructions title
        self.instructions_title.pack(padx=10, pady=10)

        # Pack instructions label
        self.instructions_label.pack()
