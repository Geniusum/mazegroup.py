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

# If there is an error, shows it (optional) :
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
- `calc <...>`
	- Evaluate expression in arguments with the Shaft parser.
- `cd <path>`
	- Choose the working directory, work only on MazeGroup.py shell.
- `exit <...>`
	- Exit the program, for MazeGroup.py shell.
- `quit <...>`
	- Exit the program, for MazeGroup.py shell.
- `pypkg <name> <options>`
	- Make a Python package. Options :
		- `-f` or `--full` for a full generation.
		- `info:{'name': ...}` for set package informations (a python dictionnary), keys available :
			- `name` -> `str`
			- `description` -> `str`
			- `author` -> `str`
			- `license` -> `str`
			- `url` -> `str`
			- `date` -> `str`
- `sc <...>`
	- SC for Secure Compress, it's a encrypted compression who works with a password, a increment level and a tar level.
	- Usage : `mazegroup sc <compress/decompress> <path> <!* output path> <!* password> <!* increments> <!* tar>`
	- The default output is in the MazeGroup.py Python package directory, on the part of this command, either `mazegroup/sc/out`.
- `shell <...>`
	- The MazeGroup.py shell. There are modes available, use their start char for enter on it :
		- The system shell mode : `§ <...>`
		- The calc mode : `% <...>`, equivalant of the command `calc` but this mode lock the MazeGroup.py shell for expressions.
	- Once you enter in a mode, the rest of commands of after will be locked on this mode, for return to the MazeGroup.py shell, you must enter a empty command.
	- In command arguments (only on the MazeGroup.py shell), the `\s` will provoks a space.
- `rud <sourcecode> <options>`
	- RUD interpreter, a minimal stack-based programming language. No documentation available.