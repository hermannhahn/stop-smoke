"""Module to show instructions when the program is first run"""
import tkinter as tk
import os
from translation import _


class Instructions:
    """Class to show instructions when the program is first run"""
    def __init__(self, master):

        self.master = master
        self.icon_path = os.path.abspath("icon.ico")


        self.show_instructions()

    def close(self):
        """Close the instructions window"""
        self.instructions.destroy()

    def show_instructions(self):
        """Show the instructions window"""
        self.instructions = tk.Toplevel(self.master)
        self.instructions.title(_("Instructions"))
        self.instructions.iconbitmap(self.icon_path)
        self.instructions.geometry("540x300")
        self.instructions.resizable(False, False)
        self.instructions.protocol("WM_DELETE_WINDOW", self.close)


        self.instructions_title = tk.Label(self.instructions)
        self.instructions_title.pack(pady=15, padx=15)

        self.instructions_title["text"] = _("STOP SMOKE")

        self.instructions_title["font"] = ("Arial", 20, "bold")

        self.instructions_title["fg"] = "black"


        self.instructions_label = tk.Label(self.instructions)
        self.instructions_label.pack(pady=15)

        self.instructions_label["text"] = _(
"Welcome to Stop Smoke! (v1.5.0)\n"
"\n"
"This app will help you quit smoking by increasing the wait time every day.\n"
"\n"
"Every time you smoke, click the «Smoke» button to start the timer.\n"
"\n"
"The app will say how much time you have left before you can smoke again.\n"
"\n"
"Good luck!"
)
