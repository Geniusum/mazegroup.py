import mazegroup.commands as commands

class echoCommand():
    def __init__(self) -> None:
        self.name = "quit"
        self.command_class = commands.Command(self.name, self.echo, commands.Args(overflow=True), True)
        self.command_class.register()
        self.command_class.name = "exit"
        self.command_class.register()

    def echo(self, args:dict):
        exit()

echoCommand()