import mazegroup.commands as commands

class echoCommand():
    def __init__(self) -> None:
        self.name = "echo"
        self.command_class = commands.Command(self.name, self.echo, commands.Args(overflow=True), True)
        self.command_class.register()

    def echo(self, args:dict):
        for arg in args.values():
            print(arg.active_value, end=" ")
        print()

echoCommand()
