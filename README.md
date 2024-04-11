# MazeGroup.py
MazeGroup.py is an general prupose library for Python.

---

## Installation

### With PyPi :

Use the command `pip install mazegroup`, `python -m pip install mazegroup` or `py -m pip install mazegroup` to install the Python package.

## Usage

MazeGroup.py can be imported or can be executed with the CLI command (`mazegroup` or `mg`).

### With command :

The CLI command usage : `mazegroup <command> <args>`.

All commands are registered at the initialization.

For exemple `mazegroup echo Hello, world!` will prints `Hello, world!`.

### With importation :

For import MazeGroup.py in this Python source code (essential to start) :
```py
import mazegroup as mg
```

For initialize packages (commands packages) :
```py
import mazegroup.imports as imports
imports.importMGPackages()
```

For use a command in your source code (you must do the last step) :
```py
import mazegroup.commands as commands
import mazegroup.utils as utils  # For error checking

returned = commands.executeCommand("echo", ["Hello,", "world!"])  # Echo "Hello, world!" by example

# If there is a error, shows it (optional) :
if type(returned) != utils.NoError:
	print("Error :", returned.message)
```

### Arguments

You can evaluate Python expression in using `py:` in the argument (only the actual argument will be evaluate), by example the argument `"py:5 + 5"` will returns 10, we use `"` because we also use spaces on the expression.

## Commands available :

- `echo <...>`
	- Print the textes in arguments.
- `help <...>`
	- Shows all commands available.
- `ls <path>`
	- Shows all directories and files from the selected path.
- `pyexec <...>`
	- Execute the Python code in arguments.
- `pyeval <...>`
	- Evaluate the Python expression in arguments.
