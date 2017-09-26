#!/usr/bin/env python3
# -*- coding:  utf-8 -*-

' GUI of map '

__author__ = 'Mappy Group'

from GUICom import *
from mapView import *

class MapGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, height = 600, width = 900)
        self.pMap = ''
        self.mapFile = ''

        #状态栏-sFrm
        self.sFrm = SFrm(self)

        #图层栏-lFrm
        self.lFrm = LFrm(self)
        
        #地图栏-cv
        self.cv = MapCanvas(self, self.lFrm, self.sFrm)

        #鹰眼栏-eye
        self.eye = Hawkeye(self.lFrm)
    
        #菜单栏-menuBar
        self.master.menuBar = MMenu(self.master, self.pMap, self.cv, self.eye, self.lFrm, self.sFrm, self.mapFile)

        #工具栏-tFrm
        self.tFrm = TFrm(self, self.master.menuBar)
        self.master.menuBar.setTFrm(self.tFrm)
        
        self.tFrm.pack(side = TOP, fill = X)
        self.sFrm.pack(side = BOTTOM, fill = X)
        self.eye.pack(side = BOTTOM, fill = BOTH)
        self.lFrm.pack(side = LEFT, fill = Y)
        self.cv.pack(side = TOP, fill = BOTH, expand = YES)


        
