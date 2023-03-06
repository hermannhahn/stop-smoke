import gui
import tkinter as tk

# __main__ module
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Create the app
    app = gui.StopSmokingApp(master=root)
    # Start the app
    app.mainloop()
