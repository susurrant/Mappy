#!/usr/bin/env python3
# -*- coding:  utf-8 -*-

' dialogs '

__author__ = 'Mappy Group'

from tkinter import *
import tkinter.ttk as ttk

class WinCreateLayer(simpledialog.Dialog):
    def body(self, master):
        self.title('新建图层')
        self.var0 = StringVar()
        self.var0.set('')
        Label(master, text = "请输入图层名：").grid(row = 0)
        self.nLayer = Entry(master, textvariable = self.var0)
        self.nLayer.grid(row = 0, column = 1)

        self.var1 = StringVar()
        self.var1.set('点')
        Label(master, text = '请选择图层类型：').grid(row = 1)
        self.tLayer = ttk.Combobox(master, textvariable = self.var1, values = ['点', '线', '面', '注记'], state = 'readonly', width = 10)
        self.tLayer.grid(row = 1, column = 1)

        Label(master, text = '请图层符号：').grid(row = 2)
        self.sLayer = ttk.Combobox(master, state = 'readonly', width = 10)
        self.var2 = StringVar()
        self.var2.set('火车站：101')
        self.sLayer['values'] = ['火车站：101', '机场：102', '市政府：103']
        self.sLayer['textvariable'] = self.var2
        self.sLayer.grid(row = 2, column = 1)
        
        self.tLayer.bind("<<ComboboxSelected>>", self.comSelected)
        
        return self.nLayer

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text = "创建", width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = "取消", width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        layerName = self.var0.get()
        layerType = 'POINT'
        if self.var1.get() == '点':
            layerType = 'POINT'
        elif self.var1.get() == '线':
            layerType = 'POLYLINE'
        elif self.var1.get() == '面':
            layerType = 'POLYGON'
        elif self.var1.get() == '注记':
            layerType = 'ANNOTATION'
        layerSymbol = self.var2.get()
        self.result = layerName, layerType, layerSymbol

    def comSelected(self, event = None):
        if self.var1.get() == '点':
            self.var2.set('火车站：101')
            self.sLayer['values'] = ['火车站：101', '机场：102', '市政府：103']
        elif self.var1.get() == '线':
            self.var2.set('公路：201')
            self.sLayer['values'] = ['公路：201', '铁路：202', '河流：203']
        elif self.var1.get() == '面':
            self.var2.set('房屋：301')
            self.sLayer['values'] = ['房屋：301', '草地：302', '公园：303']
        elif self.var1.get() == '注记':
            self.var2.set('水系注记：401')
            self.sLayer['values'] = ['水系注记：401', '其他注记：401']


class WinDeleteLayer(simpledialog.Dialog):
    def body(self, master):
        self.title('删除图层')
        self.pMap = self.master.pMap
        self.var = StringVar()
        self.var.set('1 : ' + self.pMap.layers[0].name)
        v = []
        for i in range(self.pMap.lNum):
            v.append(str(i+1) + ' : ' + self.pMap.layers[i].name)
        Label(master, text = '请选择要删除的图层：').grid(row = 0)
        self.dLayer = ttk.Combobox(master, textvariable = self.var, values = v, state = 'readonly', width = 10)
        self.dLayer.grid(row = 0, column = 1)
        
        return self.dLayer

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text = "删除", width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = "取消", width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        layerNo = self.var.get()
        self.result = layerNo

class WinEditLayer(simpledialog.Dialog):
    def body(self, master):
        self.title('图层编辑')
        self.pMap = self.master.pMap
        self.var = StringVar()
        self.var.set('1 : ' + self.pMap.layers[0].name)
        v = []
        for i in range(self.pMap.lNum):
            v.append(str(i+1) + ' : ' + self.pMap.layers[i].name)
        Label(master, text = '请选择要编辑的图层：').grid(row = 0)
        self.dLayer = ttk.Combobox(master, textvariable = self.var, values = v, state = 'readonly', width = 10)
        self.dLayer.grid(row = 0, column = 1)
        
        return self.dLayer

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text = "确认", width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = "取消", width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        layerNo = self.var.get()
        self.result = layerNo

class LCBtn(Checkbutton):
    def __init__(self, master, layer, no):
        Checkbutton.__init__(self, master, text = layer.name)
        self.layer = layer
        self.var = IntVar()
        self.var.set(0)
        self['variable'] = self.var
        self.pack()

class WinSelectLayer(simpledialog.Dialog):
    def body(self, master):
        self.title('输出图层')
        Label(self, text = '请选择要导出的图层：').pack(side = TOP)
        self.v = []
        for i in range(self.master.pMap.lNum):
            lcBtn = LCBtn(self, self.master.pMap.layers[i], i)
            self.v.append(lcBtn)
        
        return self.v[0]

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text = "确认", width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = "取消", width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        r = []
        for btn in self.v:
            if btn.var.get():
                r.append(btn.layer)
        if len(r) > 0:
            self.result = r

class WinMapName(simpledialog.Dialog):
    def body(self, master):
        self.title('新建地图')
        self.var = StringVar()
        self.var.set('')
        Label(master, text = "请输入新地图名：").grid(row = 0)
        self.nMap = Entry(master, textvariable = self.var)
        self.nMap.grid(row = 0, column = 1)
        
        return self.nMap

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text = "确认", width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = "取消", width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        mapName = self.var.get()
        self.result = mapName

class WinAnnoName(simpledialog.Dialog):
    def body(self, master):
        self.title('添加注记')
        self.var = StringVar()
        self.var.set('')
        Label(master, text = "请输入新注记名：").grid(row = 0)
        self.nMap = Entry(master, textvariable = self.var)
        self.nMap.grid(row = 0, column = 1)
        
        return self.nMap

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text = "确认", width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = "取消", width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        mapName = self.var.get()
        self.result = mapName

class WinThreshod(simpledialog.Dialog):
    def body(self, master):
        self.title('s设定压缩阈值')
        self.var = StringVar()
        self.var.set('')
        Label(master, text = "请输入阈值：").grid(row = 0)
        self.nMap = Entry(master, textvariable = self.var)
        self.nMap.grid(row = 0, column = 1)
        
        return self.nMap

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text = "确认", width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = "取消", width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        mapName = self.var.get()
        self.result = mapName

