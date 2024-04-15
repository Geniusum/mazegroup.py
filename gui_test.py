import mazegroup.libs.termgui as termgui
import random as rd

def update():
    ins.draw_line(10, rd.randint(1, ins.height), ins.width - 10, rd.randint(1, ins.height), termgui.Back.BLUE)

ins = termgui.TermGUI()
ins.update_func = update
ins.loop()
