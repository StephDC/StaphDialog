# StaphDialog
A minimal glue library to show GUI prompts that interacts with users using different backends

## Usage
```python
import staphdialog

staphdialog.api.info("My Title", "My info")
staphdialog.api.question("My Title", "My question")
staphdialog.api.text("My Title", "My prompt")
staphdialog.api.radio("My Title", "My prompt", ("a", "bunch", "of", "options"))
```

For a return value of None, it means user cancelled the interaction, the interaction timed out, or the user did not make a choice.

## Dependencies
Currently these backends are supported:

1. kdialog
1. zenity
1. tk
1. dialog

During import, the first one from the list that looks available to use would be imported and aliased as `staphdialog.api`.

For this reason, it shall provide a pretty decent appearance on most linux and other desktop OSes.

These processes would be spawned and executed, and results returned back.

## Want to help?

PRs are very welcomed. I also hope that this could be potentially adapted for other backends to interact with user.
