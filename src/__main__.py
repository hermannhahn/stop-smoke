import gui
import tkinter as tk

# Run the app
if __name__ == '__main__':
    root = tk.Tk()
    app = gui.StopSmokingApp(master=root)
    app.mainloop()
