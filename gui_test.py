import mazegroup.libs.termgui as termgui
import random as rd

def update():
    ins.draw_line(0, 3, ins.width - 1, 3, termgui.Back.GREEN, thickness=3)
    """ins.draw_line(10, rd.randint(1, ins.height - 1), ins.width - 10, rd.randint(1, ins.height - 1), termgui.Back.BLUE)"""

ins = termgui.TermGUI()
ins.update_func = update
ins.loop()
