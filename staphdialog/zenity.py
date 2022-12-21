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
