import tkinter as tk
import threading
import os
import sys
from main import *

def startWebcam():
    threading.Thread(target=findHandPos, daemon=True, args=(True)).start()

    startWebcamButton.pack_forget()
    scaleModeButton.pack(padx=5, pady=5)
    toggleColorDisplayButton.pack(padx=5, pady=5)
    stopWebcamButton.pack(padx=5, pady=5)

# define a window
window = tk.Tk(className = " Webcam Music!")
window.configure(background = "#002b36")

# add title
title = tk.Label(
    text = "clawdags-19 webcam music",
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 20)
)
title.pack()

startWebcamButton = tk.Button(
    text = "Start Webcam",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198",
    command = startWebcam
)
startWebcamButton.pack(padx=5, pady=5)


stopWebcamButton = tk.Button(
    text = "Stop Webcam",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198",
    command = lambda: os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
)


scaleModeButton = tk.Button(
    text = "Toggle Scale Mode",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198"
)

toggleColorDisplayButton = tk.Button(
    text = "Toggle Displayed Colors",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198"
)

# begin event loop
window.mainloop()
