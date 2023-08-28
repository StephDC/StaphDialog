#! /usr/bin/python3 -B

import subprocess

__doc__ = """ Dialog Wrapper for Python Consumption """

def info(title: str, prompt: str, style: str = "info", timeout: int = None):
    run_command = (
        "dialog",
        "--clear",
        "--title", title,
        "--msgbox", prompt, "0", "0"
    )
    try:
        subprocess.run(run_command, check=True, timeout=timeout if style != "popup" else None)
    except subprocess.TimeoutExpired:
        return None
    else:
        return True

def question(title: str, prompt: str, timeout: int = None):
    try:
        result = subprocess.run((
            "dialog",
            "--clear",
            "--title", title,
            "--yesno", prompt, "0", "0"), check=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    else:
        return result.returncode == 0

def radio(title,prompt,options,timeout=None):
    run_command = ["dialog", "--clear", "--title", title, "--radiolist", prompt, "0", "0", "0"]
    run_command += sum(([str(item[0]+1), item[1], ("on", "off")[bool(item[0])]] for item in enumerate(options)), [])
    try:
        result = subprocess.run(run_command, stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    else:
        return options[int(result.stderr.decode("utf-8"))-1] if result.returncode==0 else None

def text(title,prompt,style="text",timeout=None):
    command = {"text": "--inputbox", "password": "--passwordbox"}
    try:
        result = subprocess.run(
            ("dialog","--clear","--title",title,command[style],prompt,"0","0"),
            stderr=subprocess.PIPE,
            encoding="utf-8",
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return None
    else:
        return result.stderr if result.returncode==0 else None

class progress():
    def __init__(self, title: str, prompt: str, maxval:int = 100):
        self.maxval = maxval
        self.process = subprocess.Popen(("dialog", "--clear", "--title", title, "--gauge", prompt, "0", "0"), stdin=subprocess.PIPE)
    def close(self):
        self.process.terminate()
        self.process = None
    def __del__(self):
        if self.process is not None:
            self.close()
    def update(self, value: int):
        if value > self.maxval:
            raise ValueError("Specified value greater than max value")
        value = str(int(100 * value / self.maxval))+"\n"
        self.process.stdin.write(value.encode("ascii"))
        self.process.stdin.flush()
    def prompt(self, value: str):
        self.process.stdin.write(b"XXX\n"+value.encode("utf-8")+b"\nXXX\n")
        self.process.stdin.flush()
    def check(self):
        return self.process.poll() is None
