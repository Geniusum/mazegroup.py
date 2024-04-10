"""
# MazeGroup.py
MazeGroup.py is an general prupose library for Python.
"""

import mazegroup.imports as imports
import os
#import mazegroup.commands as commands

#commands.delPickleVar()
#commands.savePickleVar()

script_path = os.path.dirname(os.path.abspath(__file__))
pth = os.path.join(script_path, "saves", "commands.pkl")
if os.path.exists(pth): os.remove(pth)

class Greet():
    def __init__(self) -> None: print("Hello! Welcome in MazeGroup.py")
