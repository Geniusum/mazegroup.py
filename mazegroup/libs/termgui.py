import os
import colorama
from colorama import Back, Fore

colorama.init()

def void(*args): pass

class TermGUI():
    def __init__(self) -> None:
        self.chars_map = []
        self.update_func = void
        self.width, self.height = os.get_terminal_size()

    def clear_term(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_map(self):
        map_str = ""
        map_str += Back.WHITE
        for y in self.chars_map:
            for x in y:
                map_str += " "
        print(map_str, end="")

        map_str = ""
        last1 = None
        last2 = None

        for y in self.chars_map:
            for x in y:
                if not last1:
                    last1 = x[1]
                    map_str += x[1]
                elif last1 != x[1]:
                    last1 = x[1]
                    map_str += x[1]
                if not last2:
                    last2 = x[2]
                    map_str += x[2]
                elif last2 != x[2]:
                    last2 = x[2]
                    map_str += x[2]

                map_str += x[0]
        print(map_str, end="")
    
    def fill_map(self, char:str, back):
        map = []
        for y in range(self.height):
            x_map = []
            for x in range(self.width):
                x_map.append([char, back, ""])
            map.append(x_map)
        self.chars_map = map

    def set_pixel(self, x:int, y:int, back, fore=Fore.RESET, char:str=" "):
        self.chars_map[y][x] = [char, back, fore]

    def draw_line(self, x1:int, y1:int, x2:int, y2:int, back, fore=Fore.RESET, char:str=" ", thickness:int=1):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            for i in range(-thickness // 2, (thickness + 1) // 2):
                self.set_pixel(x1, y1 + i, back, fore, char)
            
            if x1 == x2 and y1 == y2:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

            if thickness > 1:
                if dx > dy:
                    for i in range(-thickness // 2, (thickness + 1) // 2):
                        self.set_pixel(x1, y1 + i, back, fore, char)
                else:
                    for i in range(-thickness // 2, (thickness + 1) // 2):
                        self.set_pixel(x1 + i, y1, back, fore, char)
    
    def loop(self):
        self.fill_map(" ", Back.WHITE)
        while True:
            self.fill_map(" ", Back.WHITE)
            self.update_func()
            self.draw_map()
