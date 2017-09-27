#!/usr/bin/env python3
# -*- coding:  utf-8 -*-

' GUI components '

__author__ = 'Mappy Group'

from tkinter import *
from tkinter import filedialog
from mapStruct import *
from mapFile import *
from dialog import *
import datetime
import sys
sys.path.append('.\\icons')
import icons

class CBtn(Checkbutton):
    def __init__(self, master, layer):
        Checkbutton.__init__(self, master, text = layer.name, bg = 'LightYellow', command = self.setVisible)
        self.layer = layer
        if self.layer.onEdit:
            self['fg'] = 'blue'
        self.var = IntVar()
        self.var.set(1)
        self['variable'] = self.var
        self.select()
        self.pack(anchor = W)
        self.y = None
        self.bind('<Button-1>', self.sPos)
        self.bind('<ButtonRelease-1>', self.ePos)

    def setVisible(self):
        if self.var.get():
            self.layer.setVisible(True)
        else:
            self.layer.setVisible(False)

        self.master.master.cv.invalidate()

    def sPos(self, event):
        self.y = event.y
        
    def ePos(self, event):
        d = int((event.y - self.y) / 25)
        if d:
            self.master.pMap.moveLayer(self.layer, d)

class IconButton(Button):
    def __init__(self, master, **kwargs):
        Button.__init__(self, master, **kwargs)

    def set_icon(self, iconname, **kwargs):
        tk_img = icons.get(iconname,
                           width=kwargs.get("width"),
                           height=kwargs.get("height"))
        self.config(image=tk_img, **kwargs)
        if not kwargs.get("anchor"): kwargs["anchor"] = "center"
        if kwargs.get("compound"):
            def expand():
                self["width"] += tk_img.width()
                self["height"] += tk_img.height() / 2
            self.after(100, expand)
        self.tk_img = tk_img



class LFrm(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg = 'LightYellow')
        Label(self, text="--------------图层--------------", bg = 'LightYellow', width = '20').pack()
        self.pMap = ''
        self.chkLayers = []

    def setMap(self, pMap):
        self.pMap = pMap
        
    def flash(self):
        if self.pMap == '':
            return
        
        for cb in self.chkLayers:
            cb.destroy()
        self.chkLayers = []
        for layer in self.pMap.layers:
            chk = CBtn(self, layer)
            self.chkLayers.append(chk)



class TFrm(Frame):
    def __init__(self, master, menubar):
        Frame.__init__(self, master, bg = 'LightCyan')

        self.open_file = IconButton(self, text = 'open file', command = menubar.openFile)
        self.open_file.set_icon('open.png', width = 20, height = 20)
        self.open_file.pack(side = "left", padx = 2, pady = 2)

        self.save_file = IconButton(self, text = 'save file', state = 'disabled', command = menubar.saveFile)
        self.save_file.set_icon('save.png', width = 20, height = 20)
        self.save_file.pack(side = "left", padx = 2, pady = 2)
                
        self.new_layer = IconButton(self, text = 'create layer', state = 'disabled', command = menubar.newLayer)
        self.new_layer.set_icon('create layer.png', width = 20, height = 20)
        self.new_layer.pack(side = "left", padx = 2, pady = 2)

        self.del_layer = IconButton(self, text = 'delete layer', state = 'disabled', command = menubar.delLayer)
        self.del_layer.set_icon('del layer.png', width = 20, height = 20)
        self.del_layer.pack(side = "left", padx = 2, pady = 2)

        Label(self, text = '  ', bg = 'LightCyan').pack(side = LEFT)

        self.pan = IconButton(self, text = 'pan', state = 'disabled', command = menubar.pan)
        self.pan.set_icon('pan.png', width = 20, height = 20)
        self.pan.pack(side = "left", padx = 2, pady = 2)

        self.zoom_in = IconButton(self, text = 'zoom in', state = 'disabled', command = menubar.zoomIn)
        self.zoom_in.set_icon('zoom in.png', width = 20, height = 20)
        self.zoom_in.pack(side = "left", padx = 2, pady = 2)

        self.zoom_out = IconButton(self, text = 'zoom out', state = 'disabled', command = menubar.zoomOut)
        self.zoom_out.set_icon('zoom out.png', width = 20, height = 20)
        self.zoom_out.pack(side = "left", padx = 2, pady = 2)

        self.zoom_to_global = IconButton(self, text = 'zoom to global', state = 'disabled', command = menubar.zoomToGlobal)
        self.zoom_to_global.set_icon('zoom to global.png', width = 20, height = 20)
        self.zoom_to_global.pack(side = "left", padx = 2, pady = 2)

        Label(self, text = '  ', bg = 'LightCyan').pack(side = LEFT)

        self.edit_layer = IconButton(self, text = 'edit layer', state = 'disabled', command = menubar.editLayer)
        self.edit_layer.set_icon('edit layer.png', width = 20, height = 20)
        self.edit_layer.pack(side = "left", padx = 2, pady = 2)

        Label(self, text = '  ', bg = 'LightCyan').pack(side = LEFT)
        
        self.draw = IconButton(self, text = 'draw', state = 'disabled', command = menubar.draw)
        self.draw.set_icon('draw.png', width = 20, height = 20)
        self.draw.pack(side = "left", padx = 2, pady = 2)

        self.redo = IconButton(self, text = 'redo', state = 'disabled', command = menubar.redo)
        self.redo.set_icon('redo.png', width = 20, height = 20)
        self.redo.pack(side = "right", padx = 2, pady = 2)
        
        self.undo = IconButton(self, text = 'undo', state = 'disabled', command = menubar.undo)
        self.undo.set_icon('undo.png', width = 20, height = 20)
        self.undo.pack(side = "right", padx = 2, pady = 2)

        self.exit = IconButton(self, text = 'exit', command = menubar.exit)
        self.exit.set_icon('exit.png', width = 20, height = 20)
        self.exit.pack(side = "right", padx = 2, pady = 2)

        self.setFileDisabled(False)
        self.setViewDisabled(False)
        self.setEditDisabled(False)
        self.setDrawDisabled(False)

    def setFileDisabled(self, b):
        #不启用按钮
        if b:
            self.save_file['state'] = 'disabled'
            self.new_layer['state'] = 'disabled'
            self.del_layer['state'] = 'disabled'
        #启用按钮
        else:
            self.new_layer['state'] = 'normal'
            self.del_layer['state'] = 'normal'
            self.save_file['state'] = 'normal'

    def setViewDisabled(self, b):
        if b:
            self.pan['state'] = 'disabled'
            self.zoom_in['state'] = 'disabled'
            self.zoom_out['state'] = 'disabled'
            self.zoom_to_global['state'] = 'disabled'
        else:
            self.pan['state'] = 'normal'
            self.zoom_in['state'] = 'normal'
            self.zoom_out['state'] = 'normal'
            self.zoom_to_global['state'] = 'normal'

    def setEditDisabled(self, b):
        if b:
            self.edit_layer['state'] = 'disabled'
        else:
            self.edit_layer['state'] = 'normal'

    def setDrawDisabled(self, b):
        if b:
            self.draw['state'] = 'disabled'
            self.redo['state'] = 'disabled'
            self.undo['state'] = 'disabled'
        else:
            self.draw['state'] = 'normal'
            self.redo['state'] = 'normal'
            self.undo['state'] = 'normal'
        


class MMenu(Menu):
    def __init__(self, master, pMap, cv, eye, lFrm, sFrm, mapFile):
        Menu.__init__(self, master)
        self.pMap = pMap
        self.cv = cv
        self.eye = eye
        self.lFrm = lFrm
        self.sFrm = sFrm
        self.tFrm = None
        self.mapFile = mapFile
        fileMenu = Menu(self)
        viewMenu = Menu(self)
        editMenu = Menu(self)
        generalizeMenu = Menu(self)

        fileMenu.add_command(label = '打开', command = self.openFile)
        fileMenu.add_command(label = '新建', command = self.newMap)
        fileMenu.add_command(label = '保存', command = self.saveFile)
        fileMenu.add_command(label = '另存为', command = self.saveFileAs)
        fileMenu.add_separator()
        fileMenu.add_command(label = '导入', command = self.importLayer)
        fileMenu.add_command(label = '导出', command = self.exportLayer)
        fileMenu.add_command(label = '导出到数据库', command = self.exportData)
        fileMenu.add_command(label = '从数据库读取', command = self.importData)
        self.add_cascade(label = '文件', menu = fileMenu)

        viewMenu.add_command(label = '漫游', command = self.pan)
        viewMenu.add_command(label = '放大', command = self.zoomIn)
        viewMenu.add_command(label = '缩小', command = self.zoomOut)
        viewMenu.add_command(label = '缩放至全地图', command = self.zoomToGlobal)
        self.add_cascade(label = '视图', menu = viewMenu)
        
        editMenu.add_command(label = '新建图层', command = self.newLayer)
        editMenu.add_command(label = '删除图层', command = self.delLayer)
        editMenu.add_command(label = '图层编辑', command = self.editLayer)
        self.add_cascade(label = '编辑', menu = editMenu)

        self.add_cascade(label = '数据压缩', menu = generalizeMenu)
        generalizeMenu.add_command(label = '线压缩', command = self.lineCompression)
        self.master['menu'] = self

    def setTFrm(self, tFrm):
        self.tFrm = tFrm


    def openFile(self):
        fName = filedialog.askopenfilename(filetypes = (("mpy", "*.mpy"), ("All files", "*.*")))

        if fName != '':
            self.pMap = readData(fName)
            self.master.pMap = self.pMap
            self.mapFile = fName

        if self.pMap == 'ERRORFILE':
            messagebox.showinfo("失败", "打开文件失败！")
        elif self.pMap == '':
            return
        else:
            self.sFrm.setState('  ')
            self.pMap.setCv(self.cv)
            self.cv.setMap(self.pMap)
            self.pMap.setHawkeye(self.eye) 
            self.eye.setMap(self.pMap) 
            self.eye.invalidate() 
            self.cv['bg'] = 'white'
            self.cv.oldMouseState = 'VIEW'
            self.lFrm.setMap(self.pMap)
            self.cv.invalidate()
            self.cv.invalidateLFrm()


    def newMap(self):
        r = WinMapName(self.master)
        if r.result == None:
            return

        self.pMap = Map(r.result, 0)
        self.master.pMap = self.pMap
        self.mapFile = ''
        
        self.sFrm.setState('  ')
        self.pMap.setCv(self.cv)
        self.cv.setMap(self.pMap)
        self.pMap.setHawkeye(self.eye) 
        self.eye.setMap(self.pMap) 
        self.eye.invalidate() 
        self.cv['bg'] = 'white'
        self.cv.oldMouseState = 'VIEW'
        self.lFrm.setMap(self.pMap)
        self.cv.invalidate()
        self.cv.invalidateLFrm()

    def saveFile(self):
        if self.mapFile != '' and self.pMap != '':
            if saveData(self.mapFile, self.pMap):
                messagebox.showinfo("成功", "保存文件成功！")
            else:
                messagebox.showinfo("失败", "保存文件失败！")         


    def saveFileAs(self):
        if self.pMap == '':
            return
        
        fName = filedialog.asksaveasfilename(filetypes = (("mpy", "*.mpy"), ("All files", "*.*")))
        print(fName)
        if fName != '':
            if not fName.endswith('.mpy'):
                fName += '.mpy'
                
            if saveData(fName, self.pMap):
                messagebox.showinfo("成功", "保存文件成功！")
                self.mapFile = fName
            else:
                messagebox.showinfo("失败", "保存文件失败！")

    def importData(self):
        ##传入存储地图的数据表名称
        mapTable = 'map_table'
        self.pMap = importDataFromdatabase(mapTable)
        self.master.pMap = self.pMap
        if self.pMap:
            messagebox.showinfo("成功", "从数据库读取成功！")
            
        if self.pMap == '':
            messagebox.showinfo("失败", "数据表文件为空！")
            return
        else:
            self.sFrm.setState('  ')
            self.pMap.setCv(self.cv)
            self.cv.setMap(self.pMap)
            self.pMap.setHawkeye(self.eye) 
            self.eye.setMap(self.pMap) 
            self.eye.invalidate() 
            self.cv['bg'] = 'white'
            self.cv.oldMouseState = 'VIEW'
            self.lFrm.setMap(self.pMap)
            self.cv.invalidate()
            self.cv.invalidateLFrm()
		
    def exportData(self):
        if self.pMap == '':
            return
        if exportData2database(self.pMap):
            messagebox.showinfo("成功", "导出文件到数据库成功！")

    def draw(self):
        if self.pMap == '':
            return
        self.pMap.clearSelectedObjs()
        self.cv.hasSelect = False
        
        if self.cv.mouseMode == 'EDIT':
            self.cv.setMouseMode('DRAW')
            self.sFrm.setState('图层编辑-绘图')
        elif self.cv.mouseMode == 'DRAW':
            self.cv.setMouseMode('EDIT')
            if messagebox.askyesno("保存", "是否保存绘制？"):
                self.cv.addObjs2layer()
            self.sFrm.setState('图层编辑')

        self.cv.invalidate()
            
            
    def newLayer(self):
        if self.pMap == '':
            return

        layerConfig = WinCreateLayer(self.master)
        if layerConfig.result == None:
            return
            
        if layerConfig.result[0] == '':
            layerName = '未命名'
        else:
            layerName = layerConfig.result[0]

        layer = Layer(layerName, layerConfig.result[1], layerConfig.result[2][-3:], 0)
        self.pMap.appendLayer(layer)
        self.cv.invalidateLFrm()


    def delLayer(self):
        delfailed = False
        
        if self.pMap == '':
            return

        r = WinDeleteLayer(self.master)
        if r.result == None:
            return

        layerNo = r.result[0:2].strip()
        if layerNo.isdigit():
            if self.pMap.delLayer(int(layerNo)-1):
                self.cv.invalidate()
                self.cv.invalidateLFrm()
                delFailed = True
        if delFailed == False:
            messagebox.showinfo("失败", "删除图层失败！")


    def editLayer(self):
        if self.pMap == '':
            return
        if self.cv.mouseMode != 'EDIT':
            if self.cv.mouseMode == 'DRAW':
                if len(self.cv.objs) > 0:
                    if messagebox.askyesno("保存", "是否保存绘制？"):
                        self.cv.addObjs2layer()
            else:
                r = WinEditLayer(self.master)
                if r.result == None:
                    return

                layerNo = r.result[0:2].strip()
                if layerNo.isdigit():
                    self.cv.setMouseMode('EDIT')
                    self.pMap.layers[int(layerNo)-1].setEdit(True)
                    self.cv.setEditLayer(self.pMap.layers[int(layerNo)-1])
                    self.sFrm.setState('图层编辑')
        else:
            self.cv.setMouseMode(None)
            if self.cv.layerEditing != None:
                self.cv.layerEditing.setEdit(False)
                self.cv.layerEditing.clearSelectedObjs()
                self.cv.hasSelect = False
            self.cv.setEditLayer(None)
            self.cv.invalidate()
            self.sFrm.setState('  ')

        #self.cv.invalidateLFrm()


    def importLayer(self):
        if self.pMap == '':
            return

        fName = filedialog.askopenfilename(filetypes = (("lpy", "*.lpy"), ("All files", "*.*")))
        if fName != '':   
            if importLayerData(fName, self.pMap):
                self.cv.invalidate()
                self.cv.invalidateLFrm()
            else:
                messagebox.showinfo("失败", "导入图层文件失败！")


    def exportLayer(self):
        if self.pMap == '':
            return
        if self.pMap.lNum == 0:
            messagebox.showinfo("错误", "当前地图没有图层！")
            return
        
        r = WinSelectLayer(self.master)
        if r.result == None:
            return

        fName = filedialog.asksaveasfilename(filetypes = (("lpy", "*.lpy"), ("All files", "*.*")))
        if fName != '':
            if not fName.endswith('.lpy'):
                fName += '.lpy'
                
            if exportLayerData(fName, r.result):
                messagebox.showinfo("成功", "导出图层文件成功！")
            else:
                messagebox.showinfo("失败", "导出图层文件失败！")

    def pan(self):
        if self.pMap == '':
            return
        if not self.cv.mouseMode == 'EDIT' and not self.cv.mouseMode == 'DRAW':
            self.sFrm.setState('视图')
        self.cv.setMouseMode('VIEW')
        

    def zoomIn(self):
        if self.pMap == '':
            return
        pt = [0, 0]
        pt[0] = (self.cv.curExt[0] + self.cv.curExt[2])*1.0/2
        pt[1] = (self.cv.curExt[1] + self.cv.curExt[3])*1.0/2
        self.cv.zoom(pt, 1.1)

    def zoomOut(self):
        if self.pMap == '':
            return
        pt = [0, 0]
        pt[0] = (self.cv.curExt[0] + self.cv.curExt[2])*1.0/2
        pt[1] = (self.cv.curExt[1] + self.cv.curExt[3])*1.0/2
        self.cv.zoom(pt, 0.9)

    def zoomToGlobal(self):
        if self.pMap == '':
            return
        for i in range(4):
                    self.cv.disExt[i] = self.cv.datExt[i]
        self.cv.affiCV.calcScale(self.cv.disExt, self.cv.winExt)
        self.cv.invalidate()

    def undo(self):
        if self.pMap == '':
            return
        
        if self.cv.mouseMode == 'DRAW' and len(self.cv.objs) > 0:
            self.cv.tObjs.append(self.cv.objs.pop())
            self.cv.obj = Obj(0, 'null')
            self.cv.invalidate()
            self.cv.drawObjs()
                
    def redo(self):
        if self.pMap == '':
            return
        
        if self.cv.mouseMode == 'DRAW' and len(self.cv.tObjs) > 0:
            self.cv.objs.append(self.cv.tObjs.pop())
            self.cv.obj = Obj(0, 'null')
            self.cv.invalidate()
            self.cv.drawObjs()
            
    def exit(self):
        if self.pMap == '':
            return
        
        #从视图状态退出，如果之前状态为编辑或绘制，继续之前状态;否则退出视图状态
        if self.cv.mouseMode == 'VIEW':
            if self.cv.oldMouseMode == 'EDIT' or self.cv.oldMouseMode == 'DRAW':
                self.cv.setMouseMode(self.cv.oldMouseMode)
            else:
                self.cv.setMouseMode(None)
                self.sFrm.setState('  ')
            
        #从编辑或者绘制状态退出至无状态
        elif self.cv.mouseMode == 'EDIT' or self.cv.mouseMode == 'DRAW':
            if self.cv.mouseMode == 'DRAW':
                if len(self.cv.objs) > 0:
                    if messagebox.askyesno("保存", "是否保存绘制？"):
                        self.cv.addObjs2layer()
            if self.cv.layerEditing != None:
                self.cv.layerEditing.setEdit(False)
                self.cv.layerEditing.clearSelectedObjs()
                self.cv.hasSelect = False
            self.cv.setMouseMode(None)
            self.cv.setEditLayer(None)
            self.cv.invalidate()
            self.sFrm.setState('  ')
            self.cv.invalidateLFrm()

    def lineCompression(self):
        if self.pMap == '':
            return

        self.cv.lineCompression()

        
class SFrm(Frame):
    def __init__(self, master):
        Frame.__init__(self, bg = 'LightBlue')
        
        self.clock = Label(self, font=('times', 10, 'bold'), bg='LightBlue')
        self.clock.pack(side = RIGHT)

        dateNow = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date = Label(self, text = dateNow, font=('times', 10, 'bold'), bg='LightBlue')
        self.date.pack(side = RIGHT)

        self.co = Label(self, text = '', font=('times', 10), bg='LightBlue')
        self.co.pack(side = LEFT)

        Label(self, text = '        ', bg='LightBlue').pack(side = LEFT)
        
        self.state = Label(self, text = '', font=('times', 8), bg='LightBlue')
        self.state.pack(side = LEFT)
        
    def setState(self, t):
        self.state['text'] = t
        
    def setCo(self, x, y):
        coStr = 'x = ' + str(x) + ',   y = ' + str(y)
        self.co['text'] = coStr

        
        
