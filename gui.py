import tkinter as tk
import threading
import os
import sys
from main import *

def startWebcam():
    threading.Thread(target=findHandPos, daemon=True, args=(scaleMode.get(),)).start()

    startWebcamButton.pack_forget()
    scaleModeButton.pack_forget()
    scaleModeHeader.place_forget()
    scaleModeStatus.place_forget()
    stopWebcamButton.pack(padx=5, pady=5)

def toggleScaleMode():
    global scaleMode
    scaleMode.set(not scaleMode.get())

# define a window
window = tk.Tk(className = " Webcam Music!")
window.configure(background = "#002b36")
window.geometry("480x480")
window.resizable(width=False, height=False)

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
scaleModeHeader.place(x=100, y=200)

scaleModeStatus = tk.Label(
    textvariable = scaleMode,
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 10)
)
scaleModeStatus.place(x=300, y=200)

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

# Always displayed
quitButton = tk.Button(
    text = "Quit",
    width = 15,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198",
    command = lambda: window.destroy()
)
quitButton.place(x=200, y=400)

# begin event loop
window.mainloop()
