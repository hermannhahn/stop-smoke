import tkinter as tk
import tkinter.simpledialog as simpledialog
import time
import os
from translation import _
from database import SmokingDatabase

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
        self.master.geometry("350x120")
        # Set action when the window is closed
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        self.pack()

        # Set the path to the icon
        self.icon_path = os.path.abspath("icon.ico")

        # Create a database object
        self.db = SmokingDatabase()

        # Get the data from the database
        self.db.c.execute("SELECT * FROM smoking")
        data = self.db.c.fetchone()
        if data is None:
            # If there is no data in the database, ask the user for the initial wait time
            self.wait_time = int(simpledialog.askinteger(_("Initial wait time"), _("How many minutes do you want to wait before you can smoke again?"), parent=self.master, minvalue=1, maxvalue=1440)) * 60
            # Set the last time you smoked as the current time
            self.last_smoke = time.time() - self.wait_time
            # Insert the data into the database
            self.db.c.execute("INSERT INTO smoking VALUES (?, ?)", (self.last_smoke, self.wait_time))
            self.db.conn.commit()
        else:
            # If there is data in the database, get the last time you smoked and the wait time
            self.last_smoke = data[0]
            self.wait_time = data[1]

        # Create the widgets
        self.create_widgets()

    def create_widgets(self):
        # Create a label to show how much time is left
        self.time_left_label = tk.Label(self)
        self.time_left_label["text"] = _("Time left: {} minutes").format(int(max(0, self.last_smoke + self.wait_time - time.time()) / 60) + 1)
        self.time_left_label.pack(pady=15)

        # Create a button to smoke
        self.smoke_button = tk.Button(self)
        self.smoke_button["text"] = _("Smoke")
        self.smoke_button["state"] = "normal"
        self.smoke_button["command"] = self.smoke
        self.smoke_button.pack(pady=5)

        # Update the label and button
        self.update_screen()

    # Get the time left
    def get_time_left(self):
        time_left = int(max(0, self.last_smoke + self.wait_time - time.time()) / 60)
        return time_left
    
    # Register the time you smoked
    def smoke(self):
        # Update the last time you smoked
        self.last_smoke = time.time()

        # Update the database
        self.db.c.execute("UPDATE smoking SET last_smoke = ?, wait_time = ?", (self.last_smoke, self.wait_time))
        self.db.conn.commit()

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

    # Quit the application
    def quit(self):
        # Close the database connection
        self.db.conn.close()
        # Destroy the window
        self.master.destroy()

