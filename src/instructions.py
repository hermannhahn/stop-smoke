import tkinter as tk
import os
from translation import _

# Class to show instructions when the program is first run
class Instructions:
    def __init__(self, master):
        # Create a new window
        self.master = master
        self.icon_path = os.path.abspath("icon.ico")

        # Show alert
        self.show_instructions()

    # Close the window
    def close(self):
        self.instructions.destroy()

    # Show the instructions
    def show_instructions(self):
        # Create a new window
        self.instructions = tk.Toplevel(self.master)
        self.instructions.title(_("Instructions"))
        self.instructions.iconbitmap(self.icon_path)
        self.instructions.geometry("540x300")
        self.instructions.resizable(False, False)
        self.instructions.protocol("WM_DELETE_WINDOW", self.close)

        # Create a label with a big text to title of instructions
        self.instructions_title = tk.Label(self.instructions)
        self.instructions_title.pack(pady=15, padx=15)
        # Set the text of the label
        self.instructions_title["text"] = _("STOP SMOKE")
        # Set font and bold
        self.instructions_title["font"] = ("Arial", 20, "bold")
        # Set color black
        self.instructions_title["fg"] = "black"        

        # Create a label to show the instructions
        self.instructions_label = tk.Label(self.instructions)
        self.instructions_label.pack(pady=15)
        # Set the text of the label
        self.instructions_label["text"] = _(
"Welcome to Stop Smoke! (v1.4)\n"
"\n"
"This app will help you quit smoking by increasing the wait time every day.\n"
"\n"
"The app will show you how much time you have left before you can smoke "
"again.\n"
"Every time you smoke, click the «Smoke» button to start the timer.\n"
"\n"
"The app will say how much time you have left before you can smoke again.\n"
"\n"
"Good luck!"
)
