"""
Title: App Module
Author: Hermann Hahn
License: GPL-2.0
Version: 1.5.2
Description: This module contains the main app GUI
"""
import tkinter as tk
import time
import os
import sys
import datetime
from tkinter import simpledialog
from db.database import SmokingDatabase # pylint: disable=import-error,no-name-in-module
from gui.instructions import Instructions # pylint: disable=import-error,no-name-in-module
from gui.about import About # pylint: disable=import-error,no-name-in-module
from modules.app_translation import _ # pylint: disable=import-error,no-name-in-module



class StopSmokingApp(tk.Frame):
    """The main class of the app"""

    def __init__(self, master):
        """Initialize the app"""

        # Initialize the frame
        super().__init__(master)
        self.master = master

        # Initialize the database
        self.database = SmokingDatabase()

        # Set the window
        self.master.title(_("Stop Smoking"))
        self.master.iconbitmap(os.path.abspath("icon.ico"))
        self.master.geometry("380x120")
        self.master.resizable(False, False)

        # Set window close function
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        # Pack the frame
        self.pack()

        # Get the last smoke time and the wait time from the database
        data = self.database.get_data()
        self.last_smoke = data[0]
        self.wait_time = data[1]

        # Get the languages from a list
        self.languages = self.get_languages()

        # Create the widgets
        self.create_widgets()

        # Update the screen
        self.update_screen()

        # Focus the window on startup
        self.master.focus_force()

        # Bind the alt key to show/hide the menu
        self.master.bind("<Alt_L>", self.toggle_menu)


    def create_widgets(self):
        """Create the widgets."""

        # Create the title
        self.time_left_label = tk.Label(self)

        # Convert the last smoke time to an integer
        self.last_smoke = int(self.last_smoke)

        # Calculate the time left and set the text
        self.time_left_label["text"] = _("Time left: {} minutes").format(
            self.time_left())

        # Pack the time left label
        self.time_left_label.pack(pady=10)

        # Create the smoke button
        self.smoke_button = tk.Button(self)
        self.smoke_button["text"] = _("Smoke")
        self.smoke_button["state"] = "normal"
        self.smoke_button["command"] = self.smoke

        # Pack the smoke button
        self.smoke_button.pack(pady=10)

        # Create the alt label
        self.alt_label = tk.Label(self)
        self.alt_label["text"] = _("Press the alt key to show/hide the menu")
        self.alt_label["font"] = ("", 7)

        # Pack the alt label
        self.alt_label.pack(pady=10)


    def create_menu(self):
        """Create the menu"""

        # Create the menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        # Add the menu items
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.language_menu = tk.Menu(self.menu)
        self.help_menu = tk.Menu(self.menu)


        # Add the file menu items
        self.menu.add_cascade(label=_("File"), menu=self.file_menu)
        self.file_menu.add_command(label=_("Change interval"), command=self.change_interval)
        self.file_menu.add_command(label=_("Quit"), command=self.quit)

        # Add the help menu items
        self.menu.add_cascade(label=_("More"), menu=self.help_menu)
        self.help_menu.add_command(label=_("Instructions"), command=self.show_instructions)
        self.help_menu.add_command(label=_("About"), command=self.show_about)

        # Add the language menu items
        self.menu.add_cascade(label="🌎", menu=self.language_menu)

        # Add the languages to the menu
        for language in self.languages:

            self.language_menu.add_command(label=self.database.get_language_name(language),
                command=lambda language=language: self.update_language(language))

        # Get the current language
        current_language = self.database.get_language()[0]
        current_language_name = self.database.get_language_name(current_language)
        # Disable the current language
        self.language_menu.entryconfig(current_language_name, state="disabled")

        # Add a checkmark to the current language
        self.language_menu.entryconfig(current_language_name, label="✓ " + current_language_name)


    def time_left(self):
        """Calculate the time left."""
        return int((self.last_smoke + self.wait_time - time.time()) / 60)


    def get_languages(self):
        """Get all folders names in the locales folder and return them as a list."""    
        # Get the locales directory
        locales_dir = os.path.abspath("locales")

        # Get all folders in the locales directory
        languages = os.listdir(locales_dir)

        # Remove files from the list
        for language in languages:
            if not os.path.isdir(os.path.join(locales_dir, language)):
                languages.remove(language)
        for language in languages:
            if not os.path.isdir(os.path.join(locales_dir, language)):
                languages.remove(language)

        # Return the languages
        return languages


    def toggle_menu(self, event):
        """Toggle the menu."""

        # Print event to avoid errors
        print(event)

        # Hide and show the menu
        if self.master.config("menu")[-1] != '':

            # Esconde o menu se estiver visível
            del self.menu
            self.master.config(menu='')

        else:

            # Mostra o menu se estiver escondido
            self.create_menu()


    def update_language(self, language):
        """Update the language of the app."""

        # Update the language in the database
        self.database.update_language(language)

        # Restart the app
        self.restart()


    def change_interval(self):
        """Change the interval."""

        # Ask for the initial wait time
        self.wait_time = simpledialog.askinteger(_("Initial wait time"),
            _("Set the initial wait time in minutes:"),
            parent=self.master, minvalue=1, initialvalue=90)

        # Convert the wait time to seconds
        if self.wait_time is not None and self.wait_time > 0:
            self.wait_time *= 60

        # If the wait time is greater than 0
        if self.wait_time is not None and self.wait_time > 0:

            # Update the last smoke time
            self.last_smoke = time.time() - self.wait_time

            # Update the database
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

        # Get the last time smoked
        last_time_smoked = self.database.get_data()[0]

        # Get the day of the last time smoked
        last_time_smoked_day = datetime.datetime.fromtimestamp(last_time_smoked).day

        # Get the current day
        now_day = datetime.datetime.now().day

        # Get the wait time
        wait_time = self.database.get_data()[1]

        # If the last time smoked is not from today, increase the wait time in 1 minute
        if last_time_smoked_day != now_day:
            wait_time += 60

        # Update the last time smoked
        self.last_smoke = time.time()

        # Update the database
        self.database.update_data(self.last_smoke, wait_time)

        # Update the screen
        self.update_screen()


    def update_screen(self):
        """Update the screen."""

        # If the time left is greater than 0, disable the smoke button
        if self.get_time_left() > 0:

            # Update the title
            self.master.title(_("Stop Smoking"))

            # Disable the smoke button
            self.smoke_button["state"] = "disabled"

            # Convert the last smoke and wait time to int
            self.last_smoke = int(self.last_smoke)
            if self.wait_time is not None:
                self.wait_time = int(self.wait_time)
            else:
                self.wait_time = 0

            # Update the time left label
            self.time_left_label["text"] = _("Time left: {} minutes").format(
                self.get_time_left())

        else:

            # Update the title
            self.master.title(_("Free to Smoke"))

            # Enable the smoke button
            self.smoke_button["state"] = "normal"

            # Update the time left label
            self.time_left_label["text"] = _("You can smoke again")

        # Update the screen every second
        self.after(1000, self.update_screen)


    def restart(self):
        """Restart the application."""

        # Close the database connection
        self.database.conn.close()

        # Close the application
        self.quit()

        # Restart the application
        os.execl(sys.executable, sys.executable, *sys.argv)


    def quit(self):
        """Quit the application."""

        # Close the database connection
        self.database.conn.close()

        # Close the application
        self.master.destroy()
