def importMGPackages():
    packages = ["echo", "pyexec", "pyeval", "help", "ls", "pypkg", "sc", "cd", "shell", "calc", "quit"]
    for package in packages:
        exec(f"import mazegroup.{package}", globals())
