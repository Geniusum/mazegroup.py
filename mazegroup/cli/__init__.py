import sys
import mazegroup.imports as imports
imports.importMGPackages()
import mazegroup.commands as commands
import mazegroup.utils as utils

args = sys.argv[1:]

def main():
    if len(args) >= 1:
        command = args[0]
        command_args = args[1:]
        r = commands.executeCommand(command, command_args)
        if type(r) != utils.NoError:
            print(r.message)
    else:
        print("Usage : mazegroup <command> <args>")

if __name__ == "__main__":
    main()
