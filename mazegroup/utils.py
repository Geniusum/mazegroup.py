import uuid
import random

class Void():
    def __new__(cls) -> None: pass

class NoError(): pass
class Error():
    def __init__(self, message:str="", id:int=0):
        self.message = message.capitalize()
        if len(self.message):
            if self.message[-1] == ".": self.message = self.message[:-1]
        self.message += "."; self.id = id

def RandIDv1():
    j = [*str(uuid.uuid1()).replace("-", "")]
    random.shuffle(j)
    for i in range(random.randint(1, 80)):
        j += hex(random.randint(1, 80)).replace("0x", "")
    random.shuffle(j)
    j = "".join(j)
    return j

def RandIDv1Tiny():
    j = [*str(uuid.uuid1()).replace("-", "")]
    random.shuffle(j)
    for i in range(random.randint(1, 80)):
        j += hex(random.randint(1, 80)).replace("0x", "")
    random.shuffle(j)
    j = "".join(j)
    return j[len(j) - 10:]