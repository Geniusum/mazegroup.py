import os
try:
    import colorama
    from colorama import Fore, Back
except:
    os.system("pip install colorama")
colorama.init()

class Plan:
    class Jump():
        def __init__(self, nb:int=1) -> None:
            for jmp in range(nb):
                print()

class Jump(Plan.Jump):
    def show(self) -> None: return super().show()