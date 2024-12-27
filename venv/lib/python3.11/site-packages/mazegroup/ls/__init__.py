import mazegroup.commands as commands
import os

class Command():
    def __init__(self) -> None:
        self.name = "ls"
        self.command_class = commands.Command(self.name, self.func, commands.Args([commands.Arg("path", required=False)], overflow=False), True)
        self.command_class.register()

    def func(self, args:dict):
        if args[list(args.keys())[0]].active_value == None:
            path = os.getcwd()
        else:
            path = args[list(args.keys())[0]].active_value
        items = os.listdir(path)
        items.sort()
        for i, p in enumerate(items):
            if os.path.isdir(os.path.abspath(p)):
                items[i] += "/"
        ls = "\n".join(items)
        print(f"Path : {path}\n{ls}")
            
Command()
