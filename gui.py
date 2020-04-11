import tkinter as tk
import threading
import os
import sys
from main import *

def startWebcam():
    threading.Thread(target=findHandPos, daemon=True, args=(scaleMode.get(),)).start()

    startWebcamButton.pack_forget()
    scaleModeButton.pack_forget()
    scaleModeHeader.pack_forget()
    scaleModeStatus.pack_forget()
    # toggleColorDisplayButton.pack(padx=5, pady=5)
    stopWebcamButton.pack(padx=5, pady=5)
    quitButton.pack(padx=5, pady=5)

def toggleScaleMode():
    global scaleMode
    scaleMode.set(not scaleMode.get())

# define a window
window = tk.Tk(className = " Webcam Music!")
window.configure(background = "#002b36")

scaleMode = tk.BooleanVar()
scaleMode.set(True)

# add title
title = tk.Label(
    text = "clawdags-19 webcam music",
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 20)
)
title.pack()

# Before webcam started
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

scaleModeButton = tk.Button(
    text = "Toggle Scale Mode",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198",
    command = toggleScaleMode
)
scaleModeButton.pack(padx=5, pady=5)

scaleModeHeader = scaleModeStatus = tk.Label(
    text = "Scale Mode is currently: ",
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 10)
)
scaleModeHeader.pack(side = tk.LEFT, padx = (60, 0))

scaleModeStatus = tk.Label(
    textvariable = scaleMode,
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 10)
)
scaleModeStatus.pack(side = tk.LEFT)

# After webcam started
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

quitButton = tk.Button(
    text = "Quit",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198",
    command = lambda: window.destroy()
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
