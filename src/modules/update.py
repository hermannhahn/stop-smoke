import tkinter as tk
import urllib.request
import zipfile
import sys
import subprocess
import os

class Update(tk.Frame):
    """The update class"""
    def __init__(self, master):
        super().__init__(master)
        self.local_version_file = "VERSION.md"
        self.remote_version_url = "https://github.com/hermannhahn/stop-smoke/raw/main/VERSION.md"
        self.latest_release_url = "dist.zip"
        self.local_version = self.get_local_version()
        self.remote_version = self.get_remote_version()
        self.update_available = self.check_for_update()
        if self.update_available:
            self.update()

    def get_local_version(self):
        """Get the local version of the app"""
        with open(self.local_version_file, "r") as file:
            return file.read().strip()

    def get_remote_version(self):
        """Get the remote version of the app"""
        with urllib.request.urlopen(self.remote_version_url) as response:
            return response.read().decode("utf-8").strip()

    def check_for_update(self):
        """Check if an update is available"""
        return self.local_version != self.remote_version

    def update(self):
        """Ask the user if they want to update the app"""
        if tk.messagebox.askyesno("Update available", "An update is available. Do you want to update?"):
            self.download_update()
            self.extract_update()

    def download_update(self):
        """Download the update"""
        with urllib.request.urlopen(self.latest_release_url) as response:
            with open("update.zip", "wb") as file:
                file.write(response.read())

    def extract_update(self):
        """Extract the update and replace current files"""
        # Fecha o programa principal
        self.restart_program()
        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall()
        # Executa o arquivo update_helper.py para atualizar os arquivos
        subprocess.call([sys.executable, "update_helper.py"])

    def restart_program(self):
        """Restart the program"""
        # Obter o caminho completo do programa em execução
        command = [sys.executable] + sys.argv
        # Substituir o processo atual pelo novo
        os.execl(command[0], *command)
            
