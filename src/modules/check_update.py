"""The update module update files in the app directory"""
import tkinter as tk
import urllib.request
import sys
import subprocess
from tkinter import messagebox
from modules.app_translation import _


class Update(tk.Frame):
    """The update class"""
    def __init__(self, master):
        super().__init__(master)

        self.local_version_file = "VERSION.md"
        self.remote_version_url = "https://github.com/hermannhahn/stop-smoke/raw/main/VERSION.md"

        self.local_version = self.get_local_version()
        self.remote_version = self.get_remote_version()
        self.update_available = self.check_for_update()

        if self.update_available:
            # Ask the user if he wants to update
            answer = messagebox.askyesno(_("Update available"),
                                         _("A new version of the app is available. Do you want to update?"))

            # If the user answers yes, update the app
            if answer:
                self.update()


    def quit(self):
        """Quit the app"""
        sys.exit()


    def get_local_version(self):
        """Get the local version of the app"""
        with open(self.local_version_file, "r") as file:
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
        """Run update.exe"""
        subprocess.Popen("update.exe")
        self.quit()
