"""
Title: Check Update
Author: Hermann Hahn
License: GPL-2.0
Version: 1.5.2
Description: This module checks if there is an update available
"""
import tkinter as tk
import urllib.request
import sys
import subprocess
from tkinter import messagebox
from modules.app_translation import _ # pylint: disable=import-error,no-name-in-module


class Update(tk.Frame):
    """The update class"""

    def __init__(self, master):
        """Initialize the update class"""

        # Initialize the frame
        super().__init__(master)

        # Set variables
        self.local_version_file = "VERSION.md"
        self.remote_version_url ="https://raw.githubusercontent.com/hermannhahn/stop-smoke/main/src/VERSION.md"

        # Get versions
        self.local_version = self.get_local_version()
        self.remote_version = self.get_remote_version()

        # Check if there is an update available
        self.update_available = self.check_for_update()

        # If there is an update available
        if self.update_available:

            # Ask the user if he wants to update
            answer = messagebox.askyesno(_("Update available"),
            _("Version {} is available. Do you want to update?").format(self.remote_version))

            # If the user answers yes, update the app, don't do anything if the user answers no
            if answer:
                self.update()


    def quit(self):
        """Quit the app"""
        sys.exit()


    def get_local_version(self):
        """Get the local version of the app"""
        with open(self.local_version_file, "r", encoding="utf-8") as file:
            local_version = file.read()
        return local_version


    def get_remote_version(self):
        """Get the remote version of the app"""
        with urllib.request.urlopen(self.remote_version_url) as response:
            remote_version = response.read().decode("utf-8")
        return remote_version


    def check_for_update(self):
        """Check if there is an update available"""
        if self.local_version != self.remote_version:
            return True
        else:
            return False


    def update(self):
        """Run update.exe and quit the app"""
        subprocess.Popen("update.exe")
        self.quit()
