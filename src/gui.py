import tkinter as tk
import tkinter.simpledialog as simpledialog
import time
import os
import sys
import datetime
from translation import _
from database import SmokingDatabase
from instructions import Instructions
from about import About

# Default App class
class StopSmokingApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # Set the title of the window
        self.master.title(_("Stop Smoking"))
        # Set the icon of the window
        self.master.iconbitmap(os.path.abspath("icon.ico"))
        # Set the size of the window
        self.master.geometry("380x120")
        # Set resizable
        self.master.resizable(False, False)
        # Set action when the window is closed
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        # Hide the menu and show it again when the user presses the alt key
        self.master.bind("<Alt_L>", self.show_menu)
        # tearoff=False removes the dashed line from the menu
        self.master.option_add("*tearOff", False)
        # Pack the frame
        self.pack()
        # Set the path to the icon
        self.icon_path = os.path.abspath("icon.ico")
        # Create a database object
        self.db = SmokingDatabase()
        # Check if this is the first run
        first_run = self.db.first_run()
        # If this is the first run, set the initial values      
        if first_run:
                # Set initial interval between smokes
                self.change_interval()
                # Show the instructions
                self.show_instructions()
        else:
            # If there is data in the database, get the last time you smoked and the wait time
            data = self.db.get_data()
            self.last_smoke = data[0]
            self.wait_time = data[1]

        # Create the widgets
        self.create_widgets()

        # Update the label and button
        self.update_screen()

        # Focus when the window is opened
        self.master.focus_force()

    # Create the menu
    def create_menu(self):
        # Create a menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        # Create a file menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_("File"), menu=self.file_menu)
        self.file_menu.add_command(label=_("Change interval"), command=self.change_interval)
        self.file_menu.add_command(label=_("Quit"), command=self.quit)
        # Create a language menu and mark the current language
        self.language_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_("Language"), menu=self.language_menu)
        self.language_menu.add_command(label=_("English"), command=lambda: self.update_language("en"))
        self.language_menu.add_command(label=_("French"), command=lambda: self.update_language("fr"))
        self.language_menu.add_command(label=_("German"), command=lambda: self.update_language("de"))
        self.language_menu.add_command(label=_("Italian"), command=lambda: self.update_language("it"))
        self.language_menu.add_command(label=_("Portuguese"), command=lambda: self.update_language("pt_BR"))
        self.language_menu.add_command(label=_("Russian"), command=lambda: self.update_language("ru"))
        self.language_menu.add_command(label=_("Spanish"), command=lambda: self.update_language("es"))
        # Mark with a checkmark the current language
        self.language_menu.entryconfig(self.db.get_language_name(), label="✓ " + self.language_menu.entrycget(self.db.get_language_name(), "label"))
        # Create a help menu
        self.help_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label=_("More"), menu=self.help_menu)
        self.help_menu.add_command(label=_("Instructions"), command=self.show_instructions)
        self.help_menu.add_command(label=_("About"), command=self.show_about)

    # Update the language in database and restart the app
    def update_language(self, language):
        # Update the language in the database
        self.db.update_language(language)
        # Restart the app
        self.restart()

    # Hide the menu and show it again when the user presses the alt key
    def show_menu(self, event):
        # Create the menu if it doesn't exist
        if not hasattr(self, "menu"):
            self.create_menu()
        else:
            # Remove the menu
            self.remove_menu()
    # Remove the menu
    def remove_menu(self):
        # Hide the menu
        self.master.config(menu="")
        # Delete the menu
        del self.menu
    
    # Change interval between smokes
    def change_interval(self):
        # Ask the user how long they want to wait before they can smoke again, if they don't enter a number, set the wait time to 0
        self.wait_time = int(simpledialog.askinteger(_("Initial wait time"), _("How many minutes do you want to wait before you can smoke again?"), parent=self.master, minvalue=1, maxvalue=1440)) * 60

        # If the wait time is greater than 0, insert the data into the database
        if self.wait_time > 0:
            # Set the last time you smoked as the current time
            self.last_smoke = time.time() - self.wait_time
            # Update the data into the database
            self.db.update_data(self.last_smoke, self.wait_time)
            
    # Show the instructions
    def show_instructions(self):
        Instructions(self.master)
    
    # Show the about window
    def show_about(self):
        About(self.master)
    
    # Create widgets
    def create_widgets(self):
        # Create a label to show how much time is left
        self.time_left_label = tk.Label(self)
        self.time_left_label["text"] = _("Time left: {} minutes").format(int(max(0, self.last_smoke + self.wait_time - time.time()) / 60) + 1)
        self.time_left_label.pack(pady=10)
        # Create a button to smoke
        self.smoke_button = tk.Button(self)
        self.smoke_button["text"] = _("Smoke")
        self.smoke_button["state"] = "normal"
        self.smoke_button["command"] = self.smoke
        self.smoke_button.pack(pady=10)
        # Create a small text label to instruct the user to press the alt key to show the menu
        self.alt_label = tk.Label(self)
        self.alt_label["text"] = _("Press the alt key to show/hide the menu")
        self.alt_label["font"] = ("", 7)
        self.alt_label.pack(pady=10)

    # Get the time left
    def get_time_left(self):
        time_left = int(max(0, self.last_smoke + self.wait_time - time.time()) / 60)
        return time_left
    
    # Register the time you smoked
    def smoke(self):
        # Get data from the database
        last_time_smoked = self.db.get_data()[0]
        # Get day from last time you smoked
        last_time_smoked_day = datetime.datetime.fromtimestamp(last_time_smoked).day
        # Get day from now
        now_day = datetime.datetime.now().day
        # Get wait time from the database
        wait_time = self.db.get_data()[1]
        # If the day is different, increase wait time by 1 minute
        if last_time_smoked_day != now_day:
            wait_time += 60
            
        # Update the last time you smoked
        self.last_smoke = time.time()
                
        # Update the database
        self.db.update_data(self.last_smoke, wait_time)
        
        # Update the label and button
        self.update_screen()

    # Update what is displayed on the screen
    def update_screen(self):

        if self.get_time_left() > 0:
            # Update the window title
            self.master.title(_("Stop Smoking"))
            # Update the smoke button state
            self.smoke_button["state"] = "disabled"
            # Display the time left message in the system language
            self.time_left_label["text"] = _("Time left: {} minutes").format(int(max(0, self.last_smoke + self.wait_time - time.time()) / 60) + 1)
        else:
            # Update the window title
            self.master.title(_("Free to Smoke"))
            # Update the smoke button state
            self.smoke_button["state"] = "normal"
            # Display the message that you can smoke again in the system language
            self.time_left_label["text"] = _("You can smoke again")

        # Update the screen every second
        self.after(1000, self.update_screen)

    # Restart the application
    def restart(self):
        self.quit()
        # Restart the application
        os.execl(sys.executable, sys.executable, *sys.argv)

    # Quit the application
    def quit(self):
        # Close the database connection
        self.db.conn.close()
        # Destroy the window
        self.master.destroy()
