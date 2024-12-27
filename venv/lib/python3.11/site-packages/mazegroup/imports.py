import os

script_path = os.path.dirname(os.path.abspath(__file__))

def find_packages(dir_path: str):
    package_names = []

    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)

        if os.path.isdir(item_path):
            if os.path.isfile(os.path.join(item_path, '__init__.py')):
                package_names.append(item)

    return package_names

def importMGPackages():
    packages = find_packages(script_path)
    for package in packages:
        exec(f"import mazegroup.{package}", globals())
