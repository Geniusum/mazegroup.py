import mazegroup.commands as commands
import os

class Command():
    def __init__(self) -> None:
        self.name = "cd"
        self.command_class = commands.Command(self.name, self.func, commands.Args([commands.Arg("path", required=True)], overflow=False), True)
        self.command_class.register()

    def func(self, args:dict):
        path = str(os.path.abspath(args[list(args.keys())[0]].active_value)).replace("\\", "/")
        os.chdir(path)
            
Command()