"""
# MazeGroup.py
MazeGroup.py is an general prupose library for Python.
"""

import mazegroup.imports as imports
import mazegroup.commands as commands

commands.delPickleVar()
commands.savePickleVar()

imports.importMGPackages()

class Greet():
    def __init__(self) -> None: print("Hello! Welcome in MazeGroup.py")