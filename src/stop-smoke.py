"""Main module of the Stop Smoke app"""
import tkinter as tk
import gui.default as default

if __name__ == "__main__":

    root = tk.Tk()

    app = default.StopSmokingApp(root)

    app.mainloop()
