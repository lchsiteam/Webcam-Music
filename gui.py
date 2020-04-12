import tkinter as tk
import threading
import os
import sys
from main import *
import sd_testing
import builtins
import data


def startWebcam():
    data.run = True
    threading.Thread(target=findHandPos, daemon=True, args=(scaleMode.get(),)).start()
    threading.Thread(target=sd_testing.run, daemon=True).start() 

    startWebcamButton.pack_forget()
    scaleModeButton.pack_forget()
    scaleModeHeader.place_forget()
    scaleModeStatus.place_forget()
    stopWebcamButton.pack(padx=5, pady=5)
    captureBackgroundButton.pack(padx=5, pady=5)
    toggleOctiveButton.pack(padx=5, pady=5)
    currentOctiveHeader.place(x=100, y=250)
    currentOctiveStatus.place(x=300, y=250)

def stopWebcam():
    data.run = False

    startWebcamButton.pack(padx=5, pady=5)
    scaleModeButton.pack(padx=5, pady=5)
    scaleModeHeader.place(x=100, y=200)
    scaleModeStatus.place(x=300, y=200)

    toggleOctiveButton.pack_forget()
    currentOctiveHeader.place_forget()
    currentOctiveStatus.place_forget()
    captureBackgroundButton.pack_forget()
    stopWebcamButton.pack_forget()

def toggleScaleMode():
    global scaleMode
    scaleMode.set(not scaleMode.get())
    if scaleMode.get():
        scaleModeString.set("enabled")
    else:
        scaleModeString.set("disabled")

def captureBackground():
    data.captureBackground = True

def toggleOctive():
    if data.currentOctive == 2:
        data.currentOctive = 3
    elif data.currentOctive == 3:
        data.currentOctive = 1
    elif data.currentOctive == 1:
        data.currentOctive = 2

    tkCurrentOctive.set(data.currentOctive)

# define a window
window = tk.Tk(className = " Webcam Music!")
window.configure(background = "#002b36")
window.geometry("480x480")
window.resizable(width=False, height=False)

data.run = True
scaleMode = tk.BooleanVar()
scaleMode.set(True)
scaleModeString = tk.StringVar()
scaleModeString.set("enabled")
tkCurrentOctive = tk.IntVar()
tkCurrentOctive.set(2)

# add title
title = tk.Label(
    text = "clawdawgs-19 titanhacks 2020!",
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

scaleModeHeader = tk.Label(
    text = "Scale Mode is currently: ",
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 10)
)
scaleModeHeader.place(x=100, y=200)

scaleModeStatus = tk.Label(
    textvariable = scaleModeString,
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 10)
)
scaleModeStatus.place(x=300, y=200)

# After webcam started
captureBackgroundButton = tk.Button(
    text = "Set/Reset Background",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198",
    command = captureBackground
)

stopWebcamButton = tk.Button(
    text = "Stop Webcam",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198",
    command = stopWebcam
)

toggleOctiveButton = tk.Button(
    text = "Toggle Current Octive",
    width = 25,
    height = 2,
    fg = "#268bd2",
    bg = "#073642",
    font = ('Cascadia Code PL', 15),
    borderwidth = 0,
    activebackground = "#2aa198",
    command = toggleOctive
)

currentOctiveHeader = scaleModeStatus = tk.Label(
    text = "The current octive is: ",
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 10)
)

currentOctiveStatus = tk.Label(
    textvariable = tkCurrentOctive,
    fg = "#268bd2",
    bg = "#002b36",
    font = ('Cascadia Code PL', 10)
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
