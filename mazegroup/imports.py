def importMGPackages():
    packages = ["echo", "pyexec", "pyeval", "help", "ls", "pypkg", "sc"]
    for package in packages:
        exec(f"import mazegroup.{package}", globals())
