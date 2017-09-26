#!/usr/bin/env python3
# -*- coding:  utf-8 -*-

' main program '

__author__ = 'Mappy Group'

from tkinter import *
import time
from GUI import *

def tick():
    global time1
    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
        time1 = time2
        gui.sFrm.clock.config(text = time2)
    gui.sFrm.clock.after(200, tick)

def delObj(event = None):
    #print(event.keysym)
    if gui.cv.mouseMode == 'EDIT' and gui.cv.layerEditing != None:
        gui.cv.layerEditing.delObj()
        gui.cv.invalidate()
        
def moveObj(event = None):
    #print(event.keysym)
    if gui.cv.mouseMode == 'EDIT' and gui.cv.layerEditing != None:
        d = 0
        if event.keysym == 'Up' or event.keysym == 'Left':
            d = -5
        elif event.keysym == 'Down' or event.keysym == 'Right':
            d = 5

        if event.keysym == 'Up' or event.keysym == 'Down':
            gui.cv.layerEditing.moveY(d)
        elif event.keysym == 'Left' or event.keysym == 'Right':
            gui.cv.layerEditing.moveX(d)
        gui.cv.invalidate()

          
#主程序
root = Tk()
root.title("Mappy")
root.geometry('900x600')
gui = MapGUI(root)
gui.pack(expand = YES, fill = BOTH)

root.bind('<Delete>', delObj)
root.bind('<Up>', moveObj)
root.bind('<Down>', moveObj)
root.bind('<Left>', moveObj)
root.bind('<Right>', moveObj)

time1 = ''
tick()

root.mainloop()
