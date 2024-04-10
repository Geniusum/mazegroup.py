# MazeGroup.py
MazeGroup.py is an general prupose library for Python.

---

## Installation

### With PyPi :

Use the command `pip install mazegroup`, `python -m pip install mazegroup` or `py -m pip install mazegroup` to install the Python package.

## Usage

MazeGroup.py can be imported or can be executed with the CLI command (`mazegroup` or `mg`).

### With command :

The CLI command usage : `mazegroup <command> <args>`
All commands are registered at the initialization.

For exemple `mazegroup echo Hello, world!` will prints `Hello, world!`.

### With importation :

For import MazeGroup.py in this Python source code (essential to start):
```py
import mazegroup as mg
```

For initialize packages (commands packages) :
```py
import mazegroup.imports as imports
imports.importMGPackages()
```

For use a command in your source code (you must do the last step):
```py
import mazegroup.commands as commands
import mazegroup.utils as utils  # For error checking

returned = commands.executeCommand("echo", ["Hello,", "world!"])  # Echo "Hello, world!" by example

# If there is a error, shows it (optional) :
if type(returned) != utils.NoError:
	print("Error :", returned)
```

## Commands available :

- echo <...>
	- Print the textes in arguments.
