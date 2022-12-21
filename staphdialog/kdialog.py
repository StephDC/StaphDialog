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
        result = subprocess.run(("kdialog","--title",title,command[style],prompt), timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    else:
        return result.stdout.decode("utf-8") if result.returncode==0 else None
