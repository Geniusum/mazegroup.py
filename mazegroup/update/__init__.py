import mazegroup.commands as commands

class Command():
    def __init__(self) -> None:
        self.name = "update"
        self.command_class = commands.Command(self.name, self.update, commands.Args(overflow=True), True)
        self.command_class.register()

    def update(self, args:dict):
        import pip
        print("Updating to the last version...\n")
        pip.main(["install", "mazegroup", "-U"])
        print("\nDone.")

Command()