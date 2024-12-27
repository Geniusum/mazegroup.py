import mazegroup.commands as commands
import mazegroup.cli as cli
import os
import colorama
from colorama import Fore, Back

colorama.init()

class Command():
    def __init__(self) -> None:
        self.options_available = {
            "nocolor": ["-nc", "--nocolor"]
        }

        self.shell_mode = ""

        self.name = "shell"
        self.command_class = commands.Command(self.name, self.func, commands.Args([commands.Arg("options", required=False)], overflow=True), True)
        self.command_class.register()

    def optionOn(self, options:list, args:dict, option_type:str) -> bool:
        for option in options:
            arg = args[option]

            if arg.active_value in self.options_available[option_type]: return True
            return False

    def func(self, args:dict):
        print(Fore.LIGHTRED_EX + "MazeGroup.py " + Fore.BLACK + Back.LIGHTRED_EX + " Shell " + Fore.RESET + Back.RESET)
        print(Fore.WHITE + "For system shell commands, use before `§` the command.")
        print("For calc expressions, use before `%` the command." + Fore.RESET)
        while True:
            s = ""
            if self.shell_mode == "shell":
                s = "§ "
            elif self.shell_mode == "calc":
                s = "% "
            print(f"{Fore.LIGHTWHITE_EX}{Back.BLUE} MG {Back.LIGHTWHITE_EX} {Fore.BLACK}{os.getcwd()} {Back.RESET}{Fore.LIGHTBLUE_EX} > {s}{Fore.RESET}{Fore.LIGHTWHITE_EX}", end="")
            command = input().strip()
            cmd = command
            if self.shell_mode == "shell":
                command = "§ " + command
            elif self.shell_mode == "calc":
                command = "% " + command
            try:
                if len(cmd):
                    if command[0] == "§":
                        self.shell_mode = "shell"
                        if len(command[1:]):
                            os.system(command[1:])
                    elif command[0] == "%":
                        self.shell_mode = "calc"
                        if len(command[1:]):
                            args = command.strip().split()
                            if len(args) >= 1:
                                command_args_ = args
                                command_args = []
                                for arg in command_args_:
                                    command_args.append(arg.replace("\\s", " "))
                                r = cli.commands.executeCommand("calc", command_args)
                                if type(r) != cli.utils.NoError:
                                    print(f"{Fore.RED}{r.message}{Fore.RESET}")
                    else:
                        args = command.strip().split()
                        if len(args) >= 1:
                            command = args[0]
                            command_args_ = args[1:]
                            command_args = []
                            for arg in command_args_:
                                command_args.append(arg.replace("\\s", " "))
                            r = cli.commands.executeCommand(command, command_args)
                            if type(r) != cli.utils.NoError:
                                print(f"{Fore.RED}{r.message}{Fore.RESET}")
                        else:
                            print(f"{Fore.RED}Usage : <command> <args>{Fore.RESET}")
                else:
                    self.shell_mode = ""
            except Exception as e:
                print(f"{Fore.RED}Exception : {e}{Fore.RESET}")
Command()
