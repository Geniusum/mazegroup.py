import os
try:
    import colorama
    from colorama import Fore, Back
except:
    os.system("pip install colorama")
colorama.init()

class Plan:
    class Init():
        def __init__(self, name:str, script_path:str) -> None:
            self.name = name
            self.script_path = script_path
        
        def show(self) -> None:
            print(Back.LIGHTWHITE_EX + Fore.BLACK + " INIT : " + Back.LIGHTBLACK_EX + Fore.LIGHTWHITE_EX, self.name, Fore.WHITE + "in" + Fore.LIGHTWHITE_EX, self.script_path, Fore.RESET + Back.RESET)

class Init(Plan.Init):
    def show(self) -> None: return super().show()