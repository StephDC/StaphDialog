#!/usr/bin/python3

import threading
import time
import tkinter.ttk

class Window(tkinter.Tk):
    def __init__(self, timeout=None, **kwargs):
        super().__init__(**kwargs)
        self.gone = None # Return value when window is closed
        if timeout is not None:
            super().after(timeout*1000, self.destroy)
        super().columnconfigure(0, weight=1)
        super().rowconfigure(0, weight=1)
    def suicide(self, result=True):
        self.gone = result
        self.destroy()

def info(title,prompt,style="info",timeout=None):
    mainWindow = Window(timeout=timeout)
    mainWindow.title(title)
    frame = tkinter.ttk.Frame(mainWindow, padding=10)
    frame.grid(sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1) # The label can expand
    tkinter.ttk.Label(frame, text=prompt).grid(column=0, row=0, sticky=tkinter.NW)
    tkinter.ttk.Button(frame, text="OK", command=mainWindow.suicide).grid(column=0, row=1, sticky=tkinter.SE)
    mainWindow.mainloop()
    return mainWindow.gone

def question(title,prompt,timeout=None):
    mainWindow = Window(timeout=timeout)
    mainWindow.title(title)
    frame = tkinter.ttk.Frame(mainWindow, padding=10)
    frame.grid(sticky="nsew")
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1) # The label can expand
    tkinter.ttk.Label(frame, text=prompt).grid(column=0, row=0, columnspan=2, sticky=tkinter.NW)
    tkinter.ttk.Button(frame, text="Yes", command=mainWindow.suicide).grid(column=0, row=1, sticky=tkinter.SE)
    tkinter.ttk.Button(frame, text="No", command=lambda:mainWindow.suicide(False)).grid(column=1, row=1, sticky=tkinter.SE)
    mainWindow.mainloop()
    return mainWindow.gone

def radio(title,prompt,options,timeout=None):
    mainWindow = Window(timeout=timeout)
    mainWindow.title(title)
    frame = tkinter.ttk.Frame(mainWindow, padding=10)
    frame.grid(sticky=(tkinter.N, tkinter.S, tkinter.E, tkinter.W))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1) # Only listInput
    tkinter.ttk.Label(frame, text=prompt).grid(column=0, row=0, columnspan=2, sticky=tkinter.NW)
    listInput = tkinter.ttk.Treeview(frame, selectmode="browse")
    listInput.grid(column=0, row=1, columnspan=2, sticky=(tkinter.N, tkinter.S, tkinter.E, tkinter.W))
    for item in options:
        listInput.insert("", "end", item, text=item)
    tkinter.ttk.Button(frame, text="Submit", command=lambda: mainWindow.suicide(listInput.selection())).grid(column=0, row=2, sticky=tkinter.SE)
    tkinter.ttk.Button(frame, text="Cancel", command=mainWindow.destroy).grid(column=1, row=2, sticky=tkinter.SE)
    mainWindow.mainloop()
    if type(mainWindow.gone) is tuple:
        if not mainWindow.gone:
            return None
        else:
            return mainWindow.gone[0]
    return mainWindow.gone

def text(title,prompt,style="text",timeout=None):
    mainWindow = Window(timeout=timeout)
    mainWindow.title(title)
    frame = tkinter.ttk.Frame(mainWindow, padding=10)
    frame.grid()
    frame.grid(sticky=(tkinter.N, tkinter.S, tkinter.E, tkinter.W))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    tkinter.ttk.Label(frame, text=prompt).grid(column=0, row=0, columnspan=2, sticky=tkinter.NW)
    if style == "password":
        textInput = tkinter.ttk.Entry(frame, show="*")
    else:
        textInput = tkinter.ttk.Entry(frame)
    textInput.grid(column=0, row=1, columnspan=2, sticky="NWE")
    tkinter.ttk.Button(frame, text="Submit", command=lambda: mainWindow.suicide(textInput.get())).grid(column=0, row=2, sticky=tkinter.SE)
    tkinter.ttk.Button(frame, text="Cancel", command=mainWindow.destroy).grid(column=1, row=2, sticky=tkinter.SE)
    mainWindow.mainloop()
    return mainWindow.gone
