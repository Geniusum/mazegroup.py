import mazegroup.commands as commands

class Command():
    def __init__(self) -> None:
        self.name = "version"
        self.command_class = commands.Command(self.name, self.func, commands.Args(overflow=False), True)
        self.command_class.register()
        self.command_class.name = "ver"
        self.command_class.register()

    def func(self, args:dict):
        import pip
        print(f"(CC) 2024 - MazeGroup.py - Created by MazeGroup Research Institute\nSpecifications from pip :\n")
        pip.main(["show", "mazegroup"])
            
Command()