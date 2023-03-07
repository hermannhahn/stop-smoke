"""Main module of the Stop Smoking app."""
import gui
import tkinter as tk


if __name__ == "__main__":

    root = tk.Tk()

    app = gui.StopSmokingApp(root)

    app.mainloop()
