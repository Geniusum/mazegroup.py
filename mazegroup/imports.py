def importMGPackages():
    packages = ["echo", "pyexec", "pyeval", "help", "ls"]
    for package in packages:
        exec(f"import mazegroup.{package}", globals())
