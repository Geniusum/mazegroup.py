import mazegroup.commands as commands

class Command():
    def __init__(self) -> None:
        self.name = "help"
        self.command_class = commands.Command(self.name, self.func, commands.Args(overflow=True), True)
        self.command_class.register()

    def func(self, args:dict):
        cmd_str = ""
        commands.loadPickleVar()
        commands_var = dict(sorted(commands.COMMANDS.items()))
        for name, command in commands_var.items():
            command = command["class"]
            _ = command.args.getArgsNames(); __ = ""
            if not len(command.args.args_) == 0:
                for arg in _: __ += f"<{arg}> "
            else:
                __ = f"<...>"
            cmd_str += f"\t{name} {__}\n"
        print(f"Commands available :\n{cmd_str}")

Command()
