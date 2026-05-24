import tkinter as tk
from tkinter import messagebox
import webbrowser

def open_toolbox():
    pass

def open_guide():
    pass

def open_github():
    webbrowser.open("https://github.com/Christo-Hutch/cyber-multitool")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Main Menu")
root.geometry("500x500")
root.resizable(False, False)

menu_options = [
    ("Toolbox", open_toolbox),
    ("Guide", open_guide),
    ("Source Code", open_github),
    ("Exit", exit_app)
]

for text, command in menu_options:
    button = tk.Button(root, text=text, command=command, width=20)
    button.pack(pady=10)

root.mainloop()