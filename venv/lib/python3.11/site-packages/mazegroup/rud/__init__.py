import mazegroup.commands as commands
import mazegroup.rud.interpreter as interpreter

class Command():
    def __init__(self) -> None:
        self.name = "rud"
        self.command_class = commands.Command(self.name, self.func, commands.Args([commands.Arg("sourcecode", required=True), commands.Arg("options", required=False)], overflow=True), True)
        self.command_class.register()

    def func(self, args:dict):
        argv = []
        for arg in args.values():
            argv.append(arg.active_value)
        interpreter.interprete(argv)

Command()