#!/usr/bin/python3 -B

import subprocess

__doc__ = """ KDialog Wrapper for Python Consumption """

def info(title,prompt,style="info",timeout=None):
    command = {"info": "--msgbox", "warning": "--sorry", "error": "--error", "popup": "--passivepopup"}
    runConfig = ("kdialog", "--title", title, command[style], prompt)
    if style == "popup":
        runConfig += (str(timeout),)
    try:
        result = subprocess.run(runConfig, timeout=timeout if style != "popup" else None)
    except subprocess.TimeoutExpired:
        return None
    else:
        return True

def question(title,prompt,timeout=None):
    try:
        result = subprocess.run(("kdialog", "--title", title, "--yesno", prompt), timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    else:
        return result.returncode == 0

def radio(title,prompt,options,timeout=None):
    runConfig = ("kdialog", "--title", title, "--radiolist", prompt)
    for item in range(len(options)):
        runConfig += (str(item),options[item],("on","off")[bool(item)])
    try:
        result = subprocess.run(runConfig, stdout=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    else:
        return options[int(result.stdout.decode("utf-8"))] if result.returncode==0 else None

def text(title,prompt,style="text",timeout=None):
    command = {"text": "--inputbox", "password": "--password"}
    try:
        result = subprocess.run(
            ("kdialog","--title",title,command[style],prompt),
            stdout=subprocess.PIPE,
            encoding="UTF-8",
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return None
    else:
        return result.stdout if result.returncode==0 else None

class progress():
    def __init__(self, title: str, prompt: str, maxval:int = 100):
        self.maxval = maxval
        self.process = subprocess.check_output(("kdialog", "--title", title, "--progressbar", prompt, str(self.maxval)))[:-1].decode("utf-8").split(" ")
    def close(self):
        subprocess.run(["qdbus"]+ self.process + ["close"])
        self.process = None
    def _req(self, cmd:list):
        if self.process is None:
            raise IOError("I am not running")
        try:
            subprocess.run(["qdbus"]+self.process+cmd, check=True)
        except subprocess.CalledProcessError:
            self.close()
            raise IOError("Error during request")
    def __del__(self):
        if self.process is not None:
            self.close()
    def update(self, value: int):
        if value > self.maxval:
            raise ValueError("Specified value greater than max value")
        self._req(["Set","" ,"value", str(value)])
    def prompt(self, value: str):
        self._req(["setLabelText", value])
    def check(self):
        if self.process is not None:
            try:
                self._req(["wasCancelled"])
            except IOError:
                pass
            else:
                return True
        return False
