#!/usr/bin/env python3
# -*- coding:  utf-8 -*-

' functions for geoobject selection '

__author__ = 'Mappy Group'

threshold = 7

#-------点选---------

def select(x, y, CurrentLayer):
    if (CurrentLayer.lType == 'POINT')or (CurrentLayer.lType == 'ANNOTATION'):
        return selectPoint(x, y, CurrentLayer)

    elif CurrentLayer.lType == 'POLYLINE':
        return selectPolyline(x, y, CurrentLayer)

    elif CurrentLayer.lType == 'POLYGON':
        return selectPolygon(x, y, CurrentLayer)

    else:
        return -1


#判断鼠标位置离点的距离小于等于阈值时为选中
def selectPoint(x, y, CurrentLayer):
    dx = abs(x-CurrentLayer.objs[0].x[0])
    dy = abs(y-CurrentLayer.objs[0].y[0])
    minlen = ((dx**2)+(dy**2))**0.5
    PointIDSelected = 0

    for i in range(CurrentLayer.oNum):
        dx = abs(x-CurrentLayer.objs[i].x[0])
        dy = abs(y-CurrentLayer.objs[i].y[0])
        len = ((dx**2) + (dy**2)) ** 0.5
        if len < minlen:
            minlen = len
            PointIDSelected = i

    if minlen < threshold:
        return PointIDSelected
    else:
        return -1



#判断鼠标位置离线的垂直距离小于等于阈值时为选中
def selectPolyline(x, y, CurrentLayer):
    #鼠标点到线段的最短距离，初始为一个较大的数（事实上大于阈值即可）
    minlen=1000000

    len = minlen
    
    PolyLinesSelectedID = -1
    
    for j in range(CurrentLayer.oNum):
        for i in range(CurrentLayer.objs[j].pNum-1):
            #如果鼠标点在线段两端点围成的矩形内部
            if(min(CurrentLayer.objs[j].x[i], CurrentLayer.objs[j].x[i+1]) <= x and x <= max(CurrentLayer.objs[j].x[i], CurrentLayer.objs[j].x[i+1])) and (min(CurrentLayer.objs[j].y[i],CurrentLayer.objs[j].y[i+1]) <= y and y <= max(CurrentLayer.objs[j].y[i], CurrentLayer.objs[j].y[i+1])):
                #如果该线段平行于X轴
                if(CurrentLayer.objs[j].y[i] == CurrentLayer.objs[j].y[i+1]):
                    len =abs(y - CurrentLayer.objs[j].y[i])
                #如果该线段平行于Y轴
                elif(CurrentLayer.objs[j].x[i] == CurrentLayer.objs[j].x[i+1]):
                    len =abs(x - CurrentLayer.objs[j].x[i])
                #如果该线段既不平行于X轴也不平行于Y轴，即斜率存在且不为0
                else:
                #先求垂足，再求两点之间的距离
                
                    #线段斜率
                    k = (CurrentLayer.objs[j].y[i+1] - CurrentLayer.objs[j].y[i])/(CurrentLayer.objs[j].x[i+1] - CurrentLayer.objs[j].x[i])
                    #垂足坐标
                    foot_x = (k*k*CurrentLayer.objs[j].x[i] + k*(y - CurrentLayer.objs[j].y[i]) + x)/(k*k+1)
                    foot_y = k*(foot_x - CurrentLayer.objs[j].x[i]) + CurrentLayer.objs[j].y[i]
                    len = ((x - foot_x)**2 + (y - foot_y)**2)**0.5
                if len <= minlen: 
                    minlen = len
                    PolyLinesSelectedID = j
                '''
                
                    A = CurrentLayer.objs[j].y[i+1] - CurrentLayer.objs[j].y[i]
                    B = CurrentLayer.objs[j].x[i] - CurrentLayer.objs[j].x[i+1]
                    C = CurrentLayer.objs[j].x[i+1] * CurrentLayer.objs[j].y[i] - CurrentLayer.objs[j].x[i] - CurrentLayer.objs[j].y[i+1]
                    len = (abs(A*x + B*y + C))/((A*A + B*B)**0.5)
                '''


    if minlen < threshold:
        return PolyLinesSelectedID
    else:
        return -1


#判断鼠标位置在多边形内时为选中
def selectPolygon(x, y, CurrentLayer):
    for i in range(CurrentLayer.oNum):
        if isPointInPolygon(x, y, CurrentLayer.objs[i]):
            return i

    return -1


def isPointInPolygon(x, y, polygon):
    PointInPolygon = False
    i = 0
    j = polygon.pNum - 1
    while(i < polygon.pNum-1):
        if(((polygon.y[i] <= y) and (polygon.y[j] >= y)) or ((polygon.y[j] <= y) and (polygon.y[i] >= y))):
            if (polygon.x[i] + (y - polygon.y[i])/(polygon.y[j] - polygon.y[i])*(polygon.x[j] - polygon.x[i]) < x):
                #有奇数个数时为true
                PointInPolygon = not PointInPolygon
                j = i
        i = i + 1

    return PointInPolygon


#----------框选----------
def selectByRect(rect, CurrentLayer):
    if(CurrentLayer.lType == 'POINT')or (CurrentLayer.lType == 'ANNOTATION'):
        return SelectPointByRect(rect,CurrentLayer)
    
    elif CurrentLayer.lType == 'POLYLINE':
        return SelectPolylineByRect(rect,CurrentLayer)

    elif CurrentLayer.lType == 'POLYGON':
        return SelectPolygonByRect(rect,CurrentLayer)

    else:
        return []


def SelectPointByRect(rect,CurrentLayer):
    PointIDSelectedList = []
    for i in range(CurrentLayer.oNum):
        if((CurrentLayer.objs[i].x[0] >= rect.lefttop_x)and(CurrentLayer.objs[i].x[0] <= rect.rightbottom_x)and(CurrentLayer.objs[i].y[0] >= rect.lefttop_y)and(CurrentLayer.objs[i].y[0] <= rect.rightbottom_y)):
            PointIDSelectedList.append(i)
    if PointIDSelectedList:
        return PointIDSelectedList
    else:
        return []
        
def SelectPolylineByRect(rect,CurrentLayer):
    PolylineIDSelectedList = []
    for j in range(CurrentLayer.oNum):
        for i in range(CurrentLayer.objs[j].pNum-1):
            if IsSegmentInRect(CurrentLayer.objs[j].x[i],CurrentLayer.objs[j].y[i],CurrentLayer.objs[j].x[i+1],CurrentLayer.objs[j].y[i+1],rect):
                PolylineIDSelectedList.append(j)
                break
    return PolylineIDSelectedList
'''
    for polyline in CurrentLayer.objs:
        for i in range(0,len(polyline)-1):
            if IsSegmentInRect(polyline[i].x,polyline[i].y,polyline[i+1].x,polyline[i+1].y,rect):
                PolylineIDSelectedList.append(CurrentLayer.objs.index(polyline))
                break
    return PolylineIDSelectedList
'''                

def IsSegmentInRect(x1,y1,x2,y2,rect):
    #转换为真除法
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    rect.lefttop_x,rect.lefttop_y,rect.rightbottom_x,rect.rightbottom_y = float(rect.lefttop_x), float(rect.lefttop_y), float(rect.rightbottom_x), float(rect.rightbottom_y)
     
    #判断矩形上边线和两点直线相交的点
    intersection_top_x = (rect.lefttop_y - y1) * (x2 - x1) / (y2 - y1) + x1
    if intersection_top_x >= rect.lefttop_x and intersection_top_x <= rect.rightbottom_x:
        return True
    #判断矩形下边线和两点直线相交的点
    intersection_bottom_x = (rect.lefttop_y - y1) * (x2 - x1) / (y2 - y1) + x1
    if intersection_bottom_x >= rect.lefttop_x and intersection_bottom_x <= rect.rightbottom_x:
        return True
     
    #判断矩形左边线和两点直线相交的点
    intersection_left_y = (rect.rightbottom_y - y1) * (rect.rightbottom_x - x1) / (x2 - x1) + y1
    if intersection_left_y >= rect.rightbottom_y and intersection_left_y <= rect.lefttop_y:
        return True
    #判断矩形右边线和两点直线相交的点
    intersection_right_y = (rect.rightbottom_y - y1) * (rect.rightbottom_x - x1) / (x2 - x1) + y1
    if intersection_right_y >= rect.rightbottom_y and intersection_right_y <= rect.lefttop_y:
        return True
     
    return False



def SelectPolygonByRect(rect,CurrentLayer):
    PolygonIDSelectedList = []
    for i in range(CurrentLayer.oNum):
        if IsPolygonIntersectRect(CurrentLayer.objs[i],rect):
            PolygonIDSelectedList.append(i)
    return PolygonIDSelectedList
    
'''
    for polygon in CurrentLayer.objs:
        if IsPolygonIntersectRect(polygon,rect):
            PolygonIDSelectedList.append(CurrentLayer.objs.index(polygon))

    return PolygonIDSelectedList
'''




def IsPolygonIntersectRect(polygon,rect):
    for i in range(0,polygon.pNum):
        if polygon.x[i] >= rect.lefttop_x and polygon.x[i] <= rect.rightbottom_x and polygon.y[i] <= rect.rightbottom_y and polygon.y[i] >= rect.lefttop_y:
            return True
    return False
