#!/usr/bin/python3

import os
import shutil
api = None

__doc__ = "init the library by searching for a compatible backend and bind it to api"

def init():
    " Detect the dialog backend and import it to api "
    global api
    if "DISPLAY" not in os.environ:
        from . import dialog
        api = dialog
    elif shutil.which("zenity") is not None:
        from . import zenity
        api = zenity
    elif shutil.which("kdialog") is not None:
        from . import kdialog
        api = kdialog
    else:
        try:
            from . import tk
        except Exception:
            raise ImportError(
                "ERROR: Cannot find a compatible dialog backend."
                "Maybe consider installing Zenity for Gnome or Kdialog for KDE?"
            )
        else:
            api = tk

init() ## Run this when importing the library
