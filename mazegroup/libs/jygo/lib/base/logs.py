import os
try:
    import colorama
    from colorama import Fore, Back
except:
    os.system("pip install colorama")
colorama.init()

class Plan:
    class Log():
        def __init__(self, text:str) -> None:
            self.text = text
        
        def show(self) -> None:
            print(Back.LIGHTWHITE_EX + Fore.BLACK + " LOG : " + Back.LIGHTBLACK_EX, self.text, Fore.RESET + Back.RESET)

class Log(Plan.Log):
    def show(self) -> None: return super().show()