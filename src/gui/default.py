"""The GUI of the app"""
import tkinter as tk
import time
import os
import sys
import datetime
from tkinter import simpledialog
import modules.update as Update
from db.database import SmokingDatabase
from modules.translation import _
from gui.instructions import Instructions
from gui.about import About
from modules.update import Update


class StopSmokingApp(tk.Frame):
    """The main class of the app"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.title(_("Stop Smoking"))
        self.master.iconbitmap(os.path.abspath("icon.ico"))
        self.master.geometry("380x120")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        self.pack()

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.language_menu = tk.Menu(self.menu)
        self.help_menu = tk.Menu(self.menu)

        self.icon_path = os.path.abspath("icon.ico")

        self.database = SmokingDatabase()
        
        # Update the app
        self.update = Update(self.master)
        self.update.check_for_update()

        first_run = self.database.first_run()

        if first_run:

            self.change_interval()

            self.show_instructions()
        else:

            data = self.database.get_data()
            self.last_smoke = data[0]
            self.wait_time = data[1]


        self.create_widgets()


        self.update_screen()


        self.master.focus_force()

        self.master.bind("<Alt_L>", self.toggle_menu)


    def create_widgets(self):
        """Create the widgets."""
        self.time_left_label = tk.Label(self)
        self.last_smoke = int(self.last_smoke)
        if self.wait_time is not None:
            self.wait_time = int(self.wait_time)
        else:
            self.wait_time = 0
        self.time_left_label["text"] = _("Time left: {} minutes").format(
            int(max(0, self.last_smoke + self.wait_time - time.time()) / 60) + 1)
        self.time_left_label.pack(pady=10)

        self.smoke_button = tk.Button(self)
        self.smoke_button["text"] = _("Smoke")
        self.smoke_button["state"] = "normal"
        self.smoke_button["command"] = self.smoke
        self.smoke_button.pack(pady=10)

        self.alt_label = tk.Label(self)
        self.alt_label["text"] = _("Press the alt key to show/hide the menu")
        self.alt_label["font"] = ("", 7)
        self.alt_label.pack(pady=10)


    def create_menu(self):
        """Create the menu."""
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.language_menu = tk.Menu(self.menu)

        self.help_menu = tk.Menu(self.menu)

        self.database = SmokingDatabase()
        self.menu.add_cascade(label=_("File"), menu=self.file_menu)
        self.file_menu.add_command(label=_("Change interval"), command=self.change_interval)
        self.file_menu.add_command(label=_("Quit"), command=self.quit)

        self.menu.add_cascade(label=_("More"), menu=self.help_menu)
        self.help_menu.add_command(label=_("Instructions"), command=self.show_instructions)
        self.help_menu.add_command(label=_("About"), command=self.show_about)

        self.menu.add_cascade(label="🌎", menu=self.language_menu)
        self.language_menu.add_command(label=("English"),
            command=lambda: self.update_language("en"))
        self.language_menu.add_command(label=("Francés"),
            command=lambda: self.update_language("fr"))
        self.language_menu.add_command(label=("Deutsch"),
            command=lambda: self.update_language("de"))
        self.language_menu.add_command(label=("Italiano"),
            command=lambda: self.update_language("it"))
        self.language_menu.add_command(label=("Portugues"),
            command=lambda: self.update_language("pt_BR"))
        self.language_menu.add_command(label=("Castelhano"),
            command=lambda: self.update_language("es"))
        self.language_menu.add_command(label=("русский язык"),
            command=lambda: self.update_language("ru"))

        self.language_menu.entryconfig(self.database.get_language_name(), state="disabled")
        self.language_menu.entryconfig(self.database.get_language_name(), label="✓ " + self.database.get_language_name())


    def toggle_menu(self, event):
        """Toggle the menu."""
        event = event
        if self.master.config("menu")[-1] != '':
            # Esconde o menu se estiver visível
            del self.menu
            self.master.config(menu='')
        else:
            # Mostra o menu se estiver escondido
            self.create_menu()

    def update_language(self, language):
        """Update the language of the app."""
        self.database.update_language(language)

        self.restart()


    def change_interval(self):
        """Change the interval."""
        self.wait_time = simpledialog.askinteger(_("Initial wait time"),
            _("How many minutes do you want to wait before you can smoke again?"),
            parent=self.master, minvalue=1, maxvalue=1440, initialvalue=90)
        if self.wait_time is not None and self.wait_time > 0:
            self.wait_time *= 60


        if self.wait_time is not None and self.wait_time > 0:
            self.last_smoke = time.time() - self.wait_time

            self.database.update_data(self.last_smoke, self.wait_time)


    def show_instructions(self):
        """Show the instructions."""
        Instructions(self.master)


    def show_about(self):
        """Show the about window."""
        About(self.master)


    def get_time_left(self):
        """Get the time left."""
        self.last_smoke = int(self.last_smoke)
        if self.wait_time is not None:
            self.wait_time = int(self.wait_time)
        else:
            self.wait_time = 0
        time_left = int(max(0, self.last_smoke + self.wait_time - time.time()) / 60)
        return time_left


    def smoke(self):
        """Smoke."""
        last_time_smoked = self.database.get_data()[0]

        last_time_smoked_day = datetime.datetime.fromtimestamp(last_time_smoked).day

        now_day = datetime.datetime.now().day

        wait_time = self.database.get_data()[1]

        if last_time_smoked_day != now_day:
            wait_time += 60


        self.last_smoke = time.time()


        self.database.update_data(self.last_smoke, wait_time)

    
        self.update_screen()


    def update_screen(self):
        """Update the screen."""
        if self.get_time_left() > 0:

            self.master.title(_("Stop Smoking"))

            self.smoke_button["state"] = "disabled"

            self.last_smoke = int(self.last_smoke)
            if self.wait_time is not None:
                self.wait_time = int(self.wait_time)
            else:
                self.wait_time = 0

            self.time_left_label["text"] = _("Time left: {} minutes").format(
                int(max(0, self.last_smoke + self.wait_time - time.time()) / 60) + 1)

        else:
            self.master.title(_("Free to Smoke"))

            self.smoke_button["state"] = "normal"

            self.time_left_label["text"] = _("You can smoke again")


        self.after(1000, self.update_screen)


    def restart(self):
        """Restart the application."""
        self.quit()

        os.execl(sys.executable, sys.executable, *sys.argv)


    def quit(self):
        """Quit the application."""
        self.database.conn.close()

        self.master.destroy()
