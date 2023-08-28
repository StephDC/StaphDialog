#!/usr/bin/python3 -B

import subprocess

__doc__ = " Zenity wrapper for python consumption "

def popup(title,prompt, timeout=None):
    runConfig = ("zenity", "--notification", "--window-icon=info", "--text="+title+":\n"+prompt)
    if timeout is not None:
        runConfig += ("--timeout="+str(timeout),)
    result = subprocess.run(runConfig)
    return result.returncode == 0 or None

def info(title,prompt,style="info",timeout=None):
    if style == "popup":
        return popup(title,prompt,timeout)
    command = {"info": "--info", "warning": "--warning", "error": "--error"}
    runConfig=("zenity", "--title="+title, command[style],"--text="+prompt)
    if timeout is not None:
        runConfig += ("--timeout="+str(timeout),)
    result = subprocess.run(runConfig)
    return result.returncode == 0 or (None if result.returncode == 5 else False)

def question(title,prompt,timeout=None):
    runConfig = ("zenity", "--title="+title, "--question", "--text="+prompt)
    if timeout is not None:
        runConfig += ("--timeout="+str(timeout),)
    result = subprocess.run(runConfig)
    return result.returncode == 0 or (None if result.returncode==5 else False)

def radio(title,prompt,options,timeout=None):
    runConfig = ("zenity", "--title="+title, "--list", "--column=Choose one")
    if timeout is not None:
        runConfig += ("--timeout="+str(timeout),)
    runConfig += tuple(options)
#    for item in options:
#        runConfig += ("",item)
    result = subprocess.run(runConfig, stdout=subprocess.PIPE)
    if result.returncode != 0:
        return None
    else:
        return result.stdout[:-1].decode("utf-8")

def text(title,prompt,style="text",timeout=None):
    command = {"text": "--entry", "password": "--password"}
    runConfig = ("zenity", "--title="+title, command[style], "--text="+prompt)
    result = subprocess.run(runConfig, stdout=subprocess.PIPE)
    if result.returncode != 0:
        return None
    else:
        return result.stdout[:-1].decode("utf-8")

class progress():
    def __init__(self, title: str, prompt: str, maxval: int = 100):
        self.maxval = maxval
        self.process = subprocess.Popen(("zenity", "--title="+title, "--text="+prompt), stdin=subprocess.PIPE)
    def close(self):
        self.process.terminate()
        self.process = None
    def __del__(self):
        if self.process is not None:
            self.close()
    def update(self, value: int):
        if value > self.maxval:
            raise ValueError("Specified value greater than max value")
        value = str(100 * self.maxval / value)+"\n"
        try:
            self.process.communicate(value.encode("ascii"), 0.1)
        except TimeoutError:
            pass
        else:
            raise IOError("Broken communication")
    def prompt(self, value: str):
        try:
            self.process.communicate(b"#" + value.encode("utf-8")+"\n")
        except TimeoutError:
            pass
        else:
            raise IOError("Broken communication")
    def check(self):
        return self.process.poll() is None
