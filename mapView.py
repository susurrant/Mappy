#!/usr/bin/env python3
# -*- coding:  utf-8 -*-

' map view '

__author__ = 'Mappy Group'

from tkinter import *
from GUICom import *
from mapStruct import *
from geoSelect import *
#import AffineTrans
from AffineTrans import *

class Rect(object):
    def __init__(self, lefttop_x, lefttop_y, rightbottom_x, rightbottom_y):
        self.lefttop_x = lefttop_x
        self.lefttop_y = lefttop_y
        self.rightbottom_x = rightbottom_x 
        self.rightbottom_y = rightbottom_y

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MapCanvas(Canvas):
    def __init__(self, master, lFrm, sFrm):
        Canvas.__init__(self, master, height = 540, width = 730, bg = 'grey')
        self.pMap = ''
        self.lFrm = lFrm
        self.sFrm = sFrm
        self.objs = []
        self.tObjs = []
        self.obj = Obj(0, 'null')
        self.mousePressed = False
        self.oldMouseMode = None
        self.mouseMode = None
        self.layerEditing = None
        self.hasSelect = False

        self.datExt = [0, 0, 0, 0]
        self.disExt = [0, 0, 0, 0]
        self.winExt = [540, 730]
        self.curExt = [0, 0, 0, 0]
        self.mouseDownX = 0
        self.mouseDownY = 0
        self.affiCV = AffineTrans()
        #self.affiCV.calcScale(self.disExt, self.winExt)         
        
        def mouseDown(event):
            if self.pMap == '':
                return

            self.mousePressed = True

            if self.mouseMode == 'VIEW':
                self.mouseDownX = event.x
                self.mouseDownY = event.y

            if self.mouseMode == 'EDIT' and self.layerEditing != None:
                self.mouseDownX = event.x
                self.mouseDownY = event.y
            
            if self.mouseMode == 'DRAW' and self.layerEditing != None:
                self.obj.appendXY(event.x, event.y)
                if self.layerEditing.lType == 'POINT':
                    self.create_oval(event.x-5, event.y-5, event.x+5, event.y+5)
                    self.objs.append(self.obj)
                    self.obj = Obj(0, 'null')
                elif self.layerEditing.lType == 'POLYLINE':
                    if self.obj.pNum > 1:
                        self.invalidate()
                        self.drawObjs()
                        #画线
                        co = []
                        for i in range(self.obj.pNum):
                            co.append(self.obj.x[i])
                            co.append(self.obj.y[i])
                        self.create_line(co)
                elif self.layerEditing.lType == 'POLYGON':
                    if self.obj.pNum > 1:
                        self.invalidate()
                        self.drawObjs()
                        co = []
                        for i in range(self.obj.pNum):
                            co.append(self.obj.x[i])
                            co.append(self.obj.y[i])
                        co.append(self.obj.x[0])
                        co.append(self.obj.y[0])
                        self.create_line(co)
                elif self.layerEditing.lType == 'ANNOTATION':
                    r = WinAnnoName(self.master)
                    if r.result == None:
                        return
                    elif r.result == '':
                        messagebox.showinfo("提示", "注记名不能为空！")
                    else:
                        self.obj.setName(r.result)
                        self.create_text(event.x, event.y, text = r.result, font = ('宋体', 10))
                        self.objs.append(self.obj)
                        self.obj = Obj(0, 'null')

        def mouseUp(event):
            if self.pMap == '':
                return
            
            if self.mouseMode == 'VIEW' and self.mousePressed == True:
                for i in range(4):
                    self.disExt[i] = self.curExt[i]
                    
            if self.mouseMode == 'EDIT' and self.mousePressed == True:
                #pt1 = self.affiCV.D2L(event.x, event.y)
                #if self.layerEditing.ptInSelectObj(pt1):
                #   return
                
                #如何区分移动和选择
                self.layerEditing.clearSelectedObjs()
                self.hasSelect = False
                self.invalidate()
                p = self.affiCV.D2L(self.mouseDownX, self.mouseDownY)
                if self.mouseDownX == event.x and self.mouseDownY == event.y:
                    selectResult = select(p[0], p[1], self.layerEditing)
                    if selectResult > -1:
                        self.layerEditing.objs[selectResult].setSelected(True)
                        self.hasSelect = True
                else:
                    p1 = self.affiCV.D2L(event.x, event.y)
                    #print(p[0], p[1], p1[0], p1[1])
                    selectResults = None
                    if p[0] < p1[0]:
                        rect = Rect(p[0], p[1], p1[0], p1[1])
                        selectResults = selectByRect(rect, self.layerEditing)
                    else:
                        rect = Rect(p1[0], p1[1], p[0], p[1])
                        selectResults = selectByRect(rect, self.layerEditing)
                    
                    if len(selectResults) > 0:
                        for r in selectResults:
                            self.layerEditing.objs[r].setSelected(True)
                            self.hasSelect = True
                self.invalidate()

            self.mousePressed = False

        def mouseMove(event):
            if self.pMap == '':
                return

            self.sFrm.setCo(event.x, event.y)

            if self.mouseMode == 'VIEW' and self.mousePressed == True:
                pt0 = self.affiCV.D2L(self.mouseDownX, self.mouseDownY)
                pt1 = self.affiCV.D2L(event.x, event.y)
                DXY = [pt1[0] - pt0[0], pt1[1] - pt0[1]]
                self.curExt[0] = self.disExt[0] - DXY[0]
                self.curExt[1] = self.disExt[1] - DXY[1]
                self.curExt[2] = self.disExt[2] - DXY[0]
                self.curExt[3] = self.disExt[3] - DXY[1]
                self.affiCV.calcScale(self.curExt, self.winExt)
                self.invalidate()
                
            if self.mouseMode == 'EDIT' and self.mousePressed == True:
                if self.hasSelect:
                    p1 = self.affiCV.D2L(event.x, event.y)
                    #if not self.layerEditing.ptInSelectObj(p1):
                    p = self.affiCV.D2L(self.mouseDownX, self.mouseDownY)
                    dx = p1[0] - p[0]
                    dy = p1[1] - p[1]
                    self.layerEditing.moveX(dx)
                    self.layerEditing.moveY(dy)
                    self.mouseDownX = event.x
                    self.mouseDownY = event.y
                    self.invalidate()
                else:
                    self.invalidate()
                    self.create_rectangle(self.mouseDownX, self.mouseDownY, event.x, event.y)
                
            if self.mouseMode == 'DRAW' and self.layerEditing != None:
                if self.layerEditing.lType == 'POLYLINE':
                    if self.obj.pNum:
                        self.invalidate()
                        self.drawObjs()
                        #画线
                        co = []
                        for i in range(self.obj.pNum):
                            co.append(self.obj.x[i])
                            co.append(self.obj.y[i])
                        co.append(event.x)
                        co.append(event.y)
                        self.create_line(co)
                elif self.layerEditing.lType == 'POLYGON':
                    if self.obj.pNum:
                        self.invalidate()
                        self.drawObjs()
                        co = []
                        for i in range(self.obj.pNum):
                            co.append(self.obj.x[i])
                            co.append(self.obj.y[i])
                        co.append(event.x)
                        co.append(event.y)
                        co.append(self.obj.x[0])
                        co.append(self.obj.y[0])
                        self.create_line(co)

        def doubleLeft(event):
            if self.pMap == '':
                return

            if self.mouseMode == 'DRAW':
                if self.obj.pNum > 0:
                    if self.layerEditing.lType == 'POLYGON':
                        self.obj.appendXY(self.obj.x[0], self.obj.y[0])
            
                    self.objs.append(self.obj)
                    self.obj = Obj(0, 'null')

        def mouseScroll(event):
            if self.pMap == '':
                return            
            if (event.delta>0):
                scale = 0.9
            if (event.delta<0):
                scale = 1.1
            pt = self.affiCV.D2L(event.x, event.y)
            self.zoom(pt, scale)

        def delObj(event = None):
            print('delobj')
            if self.mouseMode == 'EDIT' and self.layerEditing != None:
                self.layerEditing.delObj()
                self.invalidate()
        
        self.bind("<Button-1>", mouseDown)
        self.bind("<Motion>", mouseMove)
        self.bind("<ButtonRelease-1>", mouseUp)
        self.bind("<Double-Button-1>", doubleLeft)
        self.bind("<MouseWheel>", mouseScroll)
        #self.bind("<Delete>", delObj)
        
    def zoom(self, pt, scale):
            self.curExt[0] = int(pt[0]-(pt[0]-self.disExt[0])*1.0/scale)
            self.curExt[1] = int(pt[1]-(pt[1]-self.disExt[1])*1.0/scale)
            self.curExt[2] = int(pt[0]-(pt[0]-self.disExt[2])*1.0/scale)
            self.curExt[3] = int(pt[1]-(pt[1]-self.disExt[3])*1.0/scale)
            self.affiCV.calcScale(self.curExt, self.winExt)
            for i in range(4):
                self.disExt[i] = self.curExt[i]
            self.invalidate()
     #      self.drawObjs()
     
    def setMap(self, pMap):
        self.pMap = pMap

        if pMap.lNum == 0:
            return

        minX = pMap.layers[0].objs[0].x[0]
        maxX = pMap.layers[0].objs[0].x[0]
        minY = pMap.layers[0].objs[0].y[0]
        maxY = pMap.layers[0].objs[0].y[0]
        for l in pMap.layers:
            for obj in l.objs:
                for i in range(obj.pNum):
                    if obj.x[i] < minX:
                        minX = obj.x[i]
                    elif obj.x[i] > maxX:
                        maxX = obj.x[i]

                    if obj.y[i] < minY:
                        minY = obj.y[i]
                    elif obj.y[i] > maxX:
                        maxY = obj.y[i]

        self.datExt[0] = minX - 10
        self.datExt[1] = minY - 10
        self.datExt[2] = maxX + 10
        self.disExt[3] = maxY + 10
        for i in range(4):
            self.disExt[i] = self.datExt[i]
        self.affiCV.calcScale(self.disExt, self.winExt)

    #重绘
    def invalidate(self):
        self.delete(ALL)
        self.pMap.draw()

    def invalidateLFrm(self):
        self.lFrm.flash()
    
    def setMouseMode(self, mm):
        self.oldMouseMode = self.mouseMode
        self.mouseMode = mm
        #print(mm)
        if mm == 'DRAW':
            self.objs = []
            self.tObjs = []
            self.obj = Obj(0, 'null')

    def setEditLayer(self, layer):
        self.layerEditing = layer

    def drawObjs(self):
        if len(self.objs):
            for o in self.objs:
                o.draw(self, self.layerEditing.lType, self.layerEditing.symbolID, self.affiCV)

    def addObjs2layer(self):
        if len(self.objs) > 0:
            for obj in self.objs:
                for i in range(obj.pNum):
                    p = self.affiCV.D2L(obj.x[i], obj.y[i])
                    obj.x[i] = p[0]
                    obj.y[i] = p[1]
            self.layerEditing.appendObjs(self.objs)
            self.objs = []
            self.tObjs = []
        self.obj = Obj(0, 'null')

    def lineCompression(self):
        if self.mouseMode == 'EDIT':
            if self.layerEditing.lType == 'POLYLINE' and self.hasSelect == True:
                r = WinThreshod(self.master)
                if r.result == None:
                    return
                elif r.result == '' or (not r.result.isdigit()):
                    messagebox.showinfo("错误", "域值必须非负数！")
                else:
                    t = float(r.result)
                    if t < 0:
                        messagebox.showinfo("错误", "域值必须非负！")
                    else:
                        self.layerEditing.lineCompression(t)
                        self.invalidate()


#************************************************************
class Hawkeye(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master, height = 150, width = 200, bg = 'Ivory')
        self.pMap = ''
        self.mousePressed = False 
        self.disExt = [0, 0, 0, 0]
        self.winExt = [150, 200]
        self.curExt = [0,0,0,0]
        self.mouseDownX = 0
        self.mouseDownY = 0
        self.affiEYE = AffineTrans()
        #self.affiEYE.calcScale(self.disExt, self.winExt)      
        
        def mouseDown(event):
            if self.pMap == '':
                return            
            self.mousePressed = True    
            self.mouseDownX = event.x
            self.mouseDownY = event.y                

        def mouseUp(event):
            if self.pMap == '':
                return
            XY0 = self.affiEYE.D2L(event.x, event.y)
            XY1 = self.affiEYE.D2L(self.mouseDownX, self.mouseDownY)
            DXY = [XY0[0]-XY1[0], XY0[1]-XY1[1]]
            self.pMap.cv.disExt[0] += DXY[0]
            self.pMap.cv.disExt[2] += DXY[0]
            self.pMap.cv.disExt[1] += DXY[1]
            self.pMap.cv.disExt[3] += DXY[1]
            self.pMap.cv.affiCV.calcScale(self.pMap.cv.disExt, self.pMap.cv.winExt)
            self.pMap.cv.invalidate()
            self.mousePressed = False
    

        def mouseMove(event):
            if self.pMap == '':
                return

            if (self.mousePressed == True):
                '''
                pt0 = self.affiEYE.D2L(self.mouseDownX, self.mouseDownY)
                pt1 = self.affiEYE.D2L(event.x, event.y)
                DXY = [pt1[0] - pt0[0], pt1[1] - pt0[1]]
                self.curExt[0] = self.disExt[0] - DXY[0]
                self.curExt[1] = self.disExt[1] - DXY[1]
                self.curExt[2] = self.disExt[2] - DXY[0]
                self.curExt[3] = self.disExt[3] - DXY[1]
                self.affiEYE.calcScale(self.curExt, self.winExt)
                self.invalidate()
                '''
                XY0 = self.affiEYE.D2L(event.x, event.y)
                XY1 = self.affiEYE.D2L(self.mouseDownX, self.mouseDownY)
                DXY = [XY0[0]-XY1[0], XY0[1]-XY1[1]]
                self.pMap.cv.disExt[0] += DXY[0]
                self.pMap.cv.disExt[2] += DXY[0]
                self.pMap.cv.disExt[1] += DXY[1]
                self.pMap.cv.disExt[3] += DXY[1]
                self.pMap.cv.affiCV.calcScale(self.pMap.cv.disExt, self.pMap.cv.winExt)
                self.pMap.cv.invalidate()

      
        self.bind("<Button-1>", mouseDown)
        self.bind("<Motion>", mouseMove)
        self.bind("<ButtonRelease-1>", mouseUp)

    def setMap(self, pMap):
        self.pMap = pMap

        if pMap.lNum == 0:
            return

        
        if pMap.lNum != 0:
            minX = pMap.layers[0].objs[0].x[0]
            maxX = pMap.layers[0].objs[0].x[0]
            minY = pMap.layers[0].objs[0].y[0]
            maxY = pMap.layers[0].objs[0].y[0]
            for l in pMap.layers:
                for obj in l.objs:
                    for i in range(obj.pNum):
                        if obj.x[i] < minX:
                            minX = obj.x[i]
                        elif obj.x[i] > maxX:
                           maxX = obj.x[i]

                        if obj.y[i] < minY:
                           minY = obj.y[i]
                        elif obj.y[i] > maxX:
                            maxY = obj.y[i]
            self.disExt[0] = minX - 10
            self.disExt[1] = minY - 10
            self.disExt[2] = maxX + 10
            self.disExt[3] = maxY + 10
        else:
            minX = 0
            maxX = 540
            minY = 0
            maxY = 730
            self.disExt[0] = minX - 10
            self.disExt[1] = minY - 10
            self.disExt[2] = maxX + 10
            self.disExt[3] = maxY + 10
       
        self.affiEYE.calcScale(self.disExt, self.winExt)

    #重绘
    def invalidate(self):
        self.delete(ALL)
        self.pMap.draw()
        
