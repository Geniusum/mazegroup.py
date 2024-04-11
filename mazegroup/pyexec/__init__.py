import mazegroup.commands as commands

class Command():
    def __init__(self) -> None:
        self.name = "pyexec"
        self.command_class = commands.Command(self.name, self.func, commands.Args(overflow=True), True)
        self.command_class.register()

    def func(self, args:dict):
        expression = ""
        for arg in args.values():
            expression += arg.active_value + " "
        try:
            exec(expression)
        except Exception as e:
            print("Pyexec exception :", e)

Command()
