import jygo.lib.base.errors as errors

class Plan:
    packages = {
        "log": "jygo.package.log.pkg"
    }

    def ImportPackage(package:str) -> None:
        package = package.strip().lower()
        if package in packages.keys():
            exec(f"import {packages[package]} as {package}", globals())
        else:
            errors.Error(f"Jygo package not found : '{package}'").show()

    def ImportPackageAsName(package:str, name:str) -> None:
        package = package.strip().lower()
        if package in packages.keys():
            exec(f"import {packages[package]} as {name}", globals())
        else:
            errors.Error(f"Jygo package not found : '{package}'").show()
            return "err"

    class Inner:
        """
        Class for interact and edit packages.
        """
        def NewPackage(name:str) -> None:
            name = name.strip().lower()
            if name in packages.keys():
                errors.Error(f"Jygo package '{name}' already exists.").show()
            else:
                packages[name] = f"jygo.package.{name}.pkg"

        def VerifPackageExists(name:str) -> bool:
            try:
                r = ImportPackageAsName(name, "_VERIF_PKG_TEMP_")
                if r == "err":
                    return False
            except :
                return False
            else:
                return True

packages = Plan.packages
def ImportPackage(*args, **kwargs):
    """
    For import a Jygo package.
    """
    return Plan.ImportPackage(*args, *kwargs)
def ImportPackageAsName(*args, **kwargs):
    """
    For import a Jygo package as a name.
    """
    return Plan.ImportPackageAsName(*args, *kwargs)
Inner = Plan.Inner