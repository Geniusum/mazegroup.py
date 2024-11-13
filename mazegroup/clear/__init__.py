import mazegroup.commands as commands
import os

class Command():
    def __init__(self) -> None:
        self.name = "clear"
        self.command_class = commands.Command(self.name, self.func, commands.Args(overflow=True), True)
        self.command_class.register()

    def func(self, args:dict):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

Command()