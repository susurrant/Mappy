#!/usr/bin/env python3
# -*- coding:  utf-8 -*-

' map data structure '

__author__ = 'Mappy Group'

from tkinter import *
from AffineTrans import *
import lineCompression

class Obj(object):
    def __init__(self, pNum, name):
        self.pNum = pNum
        self.isSelected = False
        self.name = name
        self.x = []
        self.y = []

    def appendXY(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.pNum = len(self.x)

    def setSelected(self, b):
        self.isSelected = b

    def setName(self, name):
        self.name = name

    def moveX(self, d):
        for i in range(self.pNum):
            self.x[i] += d
            
    def moveY(self, d):
        for i in range(self.pNum):
            self.y[i] += d
    
    def pprint(self):
        print(self.pNum)
        for i in range(self.pNum):
            print(self.x[i],self.y[i])
            
    def draw(self, cv, lType, symbolID, affineTrans):
        ol = 'black'
        if self.isSelected:
            ol = 'blue'
            
        if lType == 'POINT':
            point = affineTrans.L2D(self.x[0], self.y[0])
            cv.create_oval(point[0]-5, point[1]-5, point[0]+5, point[1]+5, outline = ol)
            #cv.create_oval(self.x[0]-5, self.y[0]-5, self.x[0]+5, self.y[0]+5, outline = ol)
        elif lType == 'POLYLINE':
            co = []
            for i in range(self.pNum):
                point = affineTrans.L2D(self.x[i], self.y[i])
                co.append(point[0])
                co.append(point[1])
                #co.append(self.x[i])
                #co.append(self.y[i])
            cv.create_line(co, fill = ol)
        elif lType == 'POLYGON':
            co = []
            for i in range(self.pNum):
                point = affineTrans.L2D(self.x[i], self.y[i])
                co.append(point[0])
                co.append(point[1])
                #co.append(self.x[i])
                #co.append(self.y[i])
            cv.create_line(co, fill = ol)
        elif lType == 'ANNOTATION':
            point = affineTrans.L2D(self.x[0], self.y[0])
            cv.create_text(point[0], point[1], text = self.name, font = ('宋体', 10), fill = ol)
            #cv.create_text(self.x[0], self.y[0], text = self.name, font = ('宋体', 10))

class Layer(object):
    def __init__(self, name, lType, symbolID, oNum):
        self.name = name
        self.lType = lType
        self.symbolID = symbolID
        self.oNum = oNum
        self.objs = []
        self.visible = True
        self.onEdit = False

    def setSymbolID(self, symbolID):
        self.symbolID = symbolID

    def setName(self, name):
        self.name = name

    def setVisible(self, v):
        self.visible = v

    def setEdit(self, b):
        self.onEdit = b

    def appendObj(self, obj):
        self.objs.append(obj)
        self.oNum = len(self.objs)
        
    def appendObjs(self, objs):
        for obj in objs:
            self.appendObj(obj)

    def delObj(self):
        delIndex = []
        for i in range(self.oNum):
            if self.objs[i].isSelected:
                delIndex.append(i)
        for j in delIndex:
            del self.objs[j]
        self.oNum = len(self.objs)

    def ptInSelectObj(self, pt):
        minX = float('Inf')
        maxX = float('-Inf')
        minY = float('Inf')
        maxY = float('-Inf')
        for obj in self.objs:
            if obj.isSelected:
                for i in range(obj.pNum):
                    if obj.x[i] < minX:
                        minX = obj.x[i]
                    if obj.x[i] > maxX:
                        maxX = obj.x[i]
                    if obj.y[i] < minY:
                        minY = obj.y[i]
                    if obj.y[i] > maxY:
                        maxY = obj.y[i]
        if pt[0] <= maxX and pt[0] >= minX and pt[1] <= maxY and pt[1] >= minY:
            return True
        else:
            return False
            
        
    def moveX(self, d):
        for obj in self.objs:
            if obj.isSelected:
                obj.moveX(d)
            
    def moveY(self, d):
        for obj in self.objs:
            if obj.isSelected:
                obj.moveY(d)
        
    def draw(self, cv, affineTrans):
        if self.visible:
            for obj in self.objs:
                obj.draw(cv, self.lType, self.symbolID, affineTrans)

    def clearSelectedObjs(self):
        for obj in self.objs:
            obj.setSelected(False)

    def pprint(self):
        print(self.name)
        #print(self.lType)
        #print(self.symbolID)
        #print(self.oNum)
        #for obj in self.objs:
        #   obj.pprint()

    def lineCompression(self, threshod):
        for obj in self.objs:
            if obj.isSelected:
                lineCompression.compress(obj, 0, obj.pNum - 1, threshod)
                obj.pNum = len(obj.x)
                if obj.pNum < 2:
                    print('error!')
                    
    
        
class Map(object):  
    def __init__(self, name, lNum):
        self.name = name
        self.lNum = lNum
        self.layers = []
        self.cv = ''
        self.eye = ''
        
    def setCv(self, cv):
        self.cv = cv

    def setHawkeye(self, eye):
        self.eye = eye
    
    def draw(self):
        if self.cv == '':
            return
        if self.cv != '':
            for i in range(self.lNum):
                self.layers[self.lNum - i -1].draw(self.cv, self.cv.affiCV)

        self.eye.delete(ALL)
        if self.eye != '':
            for i in range(self.lNum):
                self.layers[self.lNum - i -1].draw(self.eye, self.eye.affiEYE)
                
        ptt0 = self.cv.affiCV.D2L(0, 0)
        #ptt1 = self.cv.affiCV.D2L(self.cv.winExt[0], self.cv.winExt[0])
        ptt1 = self.cv.affiCV.D2L(695, 546)
        pt0 = self.eye.affiEYE.L2D(ptt0[0], ptt0[1])
        pt1 = self.eye.affiEYE.L2D(ptt1[0], ptt1[1])
        co = [pt0[0] + 2, pt0[1] + 2, pt1[0], pt0[1] + 2, pt1[0], pt1[1], pt0[0] + 2, pt1[1], pt0[0] + 2, pt0[1] + 2]
        self.eye.create_line(co, fill = 'blue', width = 2)
        

    def appendLayer(self, layer):
        self.layers.append(layer)
        self.lNum = len(self.layers)

    def delLayer(self, n):
        if n < len(self.layers):
            del self.layers[n]
            self.lNum -= 1
            return 1

        return 0

    def pprint(self):
        print(self.name)
        #print(self.lNum)
        for l in self.layers:
            l.pprint()

    def moveLayer(self, layer, n):
        pos = self.layers.index(layer)
        self.layers.remove(layer)
        self.layers.insert(pos + n, layer)
        self.cv.invalidate()
        self.cv.invalidateLFrm()

    def clearSelectedObjs(self):
        for l in self.layers:
            for obj in l.objs:
                obj.setSelected(False)
        


