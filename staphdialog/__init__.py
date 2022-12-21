#!/usr/bin/python3

import shutil
api = None

def init():
    global api
    if shutil.which("zenity") is not None:
        from . import zenity
        api = zenity
    elif shutil.which("kdialog") is not None:
        from . import kdialog
        api = kdialog
    else:
        try:
            from . import tk
        except Exception:
            raise ImportError("ERROR: Either zenity or kdialog is required as dialog backend")
        else:
            api = tk

init() ## Run this when importing the library
