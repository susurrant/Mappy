#!/usr/bin/env python3
# -*- coding:  utf-8 -*-

' file operations '

__author__ = 'Mappy Group'

from mapStruct import *
#连接数据的模块
import psycopg2
import string

def readData(fName):
    f = open(fName, 'r')
    wrongData = False
    line = f.readline()
    #创建地图
    if line.strip() == 'MAP':
        mName = f.readline().strip()
        lNum = int(f.readline().strip())
        pMap = Map(mName, lNum)

        #创建图层
        for i in range(lNum):
            line = f.readline()
            if line.strip() == 'LAYER':
                lName = f.readline().strip()
                lType = f.readline().strip()
                lSymbol = f.readline().strip()
                oNum = int(f.readline().strip())
                layer = Layer(lName, lType, lSymbol, oNum)
                
                #创建对象
                #注意引用传递问题
                for j in range(oNum):
                    line = f.readline()
                    if line.strip() == 'OBJ':
                        oName = f.readline().strip()
                        pNum = int(f.readline().strip())
                        obj = Obj(pNum, oName)
                        for k in range(pNum):
                            co = f.readline().strip().split()
                            obj.appendXY(int(co[0]), int(co[1]))
                        line = f.readline().strip()
                        if line != 'ENDOBJ':
                            wrongData = True
                            break
                        layer.appendObj(obj)
                    else:
                        wrongData = True
                        break

                line = f.readline().strip()
                if line != 'ENDLAYER' or wrongData:
                    wrongData = True
                    break
                pMap.appendLayer(layer)
            else:
                wrongData = True
                break
            
        line = f.readline().strip()
        if line != 'ENDMAP':
            wrongData = True
    else:
        wrongData = True

    f.close()
    
    if wrongData:
        return 'ERRORFILE'
    else:    
        return pMap

def saveData(fName, pMap):
    saved = True
    try:
        f = open(fName, 'w')
        f.write('MAP\n')
        f.write('\t' + str(pMap.name) + '\n')
        f.write('\t' + str(pMap.lNum) + '\n')
        for i in range(pMap.lNum):
            f.write('\t\tLAYER\n')
            f.write('\t\t\t' + str(pMap.layers[i].name) + '\n')
            f.write('\t\t\t' + pMap.layers[i].lType + '\n')
            f.write('\t\t\t' + str(pMap.layers[i].symbolID) + '\n')
		
            #输出对象及坐标点
            f.write('\t\t\t' + str(pMap.layers[i].oNum) + '\n')
            for j in pMap.layers[i].objs:
                f.write('\t\t\t\tOBJ\n')
                f.write('\t\t\t\t\t' + str(j.name) + '\n')
                f.write('\t\t\t\t\t' + str(j.pNum) + '\n')
                for k in range(j.pNum):
                    f.write('\t\t\t\t\t' + str(j.x[k]) + ' ' + str(j.y[k]) + '\n')	
                f.write('\t\t\t\tENDOBJ\n')
			
            f.write('\t\tENDLAYER\n')

        f.write('ENDMAP\n')
        f.close()
    except:
        saved = False
    finally:
        return saved
    

def exportLayerData(fName, layers):
    exported = True
    try:
        f = open(fName, 'w')
        f.write(str(len(layers)) + '\n')
        for layer in layers:
            f.write('\tLAYER\n')
            f.write('\t\t' + str(layer.name) + '\n')
            f.write('\t\t' + layer.lType + '\n')
            f.write('\t\t' + str(layer.symbolID) + '\n')
            f.write('\t\t' + str(layer.oNum) + '\n')
            for obj in layer.objs:
                f.write('\t\t\tOBJ\n')
                f.write('\t\t\t\t' + str(obj.name) + '\n')
                f.write('\t\t\t\t' + str(obj.pNum) + '\n')
                for k in range(obj.pNum):
                    f.write('\t\t\t\t'+ str(obj.x[k]) + ' ' + str(obj.y[k]) + '\n')
                f.write('\t\t\tENDOBJ\n')
            f.write('\tENDLAYER\n')
        f.close()
    except:
        exported = False
    finally:
        return exported


def importLayerData(fName, pMap):
    f = open(fName, 'r')
    wrongData = False
    #文件所含图层数
    lNum = f.readline()
    
    if lNum.strip().isdigit():
        #遍历每个图层
        for i in range(int(lNum.strip())):
            line = f.readline()
            if line.strip() == 'LAYER':
                lName = f.readline().strip()
                lType = f.readline().strip()
                lSymbol = f.readline().strip()
                oNum = int(f.readline().strip())
                layer = Layer(lName, lType, lSymbol, oNum)

                #创建对象
                for j in range(oNum):
                    line = f.readline()
                    if line.strip() == 'OBJ':
                        oName = f.readline().strip()
                        pNum = int(f.readline().strip())
                        obj = Obj(pNum, oName)
                        for k in range(pNum):
                            co = f.readline().strip().split()
                            obj.appendXY(int(co[0]), int(co[1]))
                        line = f.readline().strip()
                        if line != 'ENDOBJ':
                            wrongData = True
                            break
                        layer.appendObj(obj)
                    else:
                        wrongData = True
                        break

                line = f.readline().strip()
                if line != 'ENDLAYER' or wrongData:
                    wrongData = True
                    break
                pMap.appendLayer(layer)
            else:
                wrongData = True
    else:
        wrongData = True

    f.close()
        
    if wrongData:
        return False
    else:
        return True
def exportData2database(pMap):
    #数据库连接参数
    conn=psycopg2.connect(database='mappy',user='postgres',password = '123',host='localhost',port='5432')
    cur=conn.cursor()

    ##清空数据表中的所有内容
    cur.execute("delete  from map_table")
    cur.execute("delete  from layer_table")
    cur.execute("delete  from obj_table")
    cur.execute("delete  from point_table")
    cur.execute("delete  from polyline_table")
    cur.execute("delete  from polygon_table")
    
    cur.execute("INSERT INTO map_table(map_name,layer_num,layer_table_name)\
                 VALUES(%r,%d,'layer_table')"%(pMap.name,pMap.lNum))
    for i in range(pMap.lNum):
        cur.execute("INSERT INTO layer_table(layer_name,layer_type,layer_code,obj_num,obj_table_name)\
                     VALUES(%r,%r,%r,%d,'obj_table')" \
                    %(pMap.layers[i].name,pMap.layers[i].lType,pMap.layers[i].symbolID,pMap.layers[i].oNum))
        if (pMap.layers[i].lType == 'POINT'):
            for j in pMap.layers[i].objs:
                cur.execute("INSERT INTO obj_table(obj_name,p_num,layer_name,data_table_name)\
                             VALUES(%r,%d,%r,'point_table')" %(j.name,j.pNum,pMap.layers[i].name))
                for k in range(j.pNum):
                    cur.execute("INSERT INTO point_table(x,y,obj_name,layer_name)\
                                 VALUES(%d,%d,%r,%r)"%(j.x[k],j.y[k],j.name,pMap.layers[i].name))
        if (pMap.layers[i].lType=="POLYLINE"):
            for j in pMap.layers[i].objs:
                cur.execute("INSERT  INTO obj_table(obj_name,p_num,layer_name,data_table_name)\
                             VALUES(%r,%d,%r,'polyline_table')" %(j.name,j.pNum,pMap.layers[i].name))
                for k in range(j.pNum):
                    cur.execute("INSERT INTO polyline_table(x,y,obj_name,layer_name)\
                                 VALUES(%d,%d,%r,%r)"%(j.x[k],j.y[k],j.name,pMap.layers[i].name))
        if (pMap.layers[i].lType=="POLYGON"):
            for j in pMap.layers[i].objs:
                cur.execute("INSERT INTO obj_table(obj_name,p_num,layer_name,data_table_name)\
                             VALUES(%r,%d,%r,'polygon_table')" %(j.name,j.pNum,pMap.layers[i].name))
                for k in range(j.pNum):
                    cur.execute("INSERT INTO polygon_table(x,y,obj_name,layer_name)\
                                 VALUES(%d,%d,%r,%r)"%(j.x[k],j.y[k],j.name,pMap.layers[i].name))
        if (pMap.layers[i].lType == 'ANNOTATION'):
            for j in pMap.layers[i].objs:
                cur.execute("INSERT  INTO obj_table(obj_name,p_num,layer_name,data_table_name)\
                             VALUES(%r,%d,%r,'point_table')" %(j.name,j.pNum,pMap.layers[i].name))
                for k in range(j.pNum):
                    cur.execute("INSERT INTO point_table(x,y,obj_name,layer_name)\
                                 VALUES(%d,%d,%r,%r)"%(j.x[k],j.y[k],j.name,pMap.layers[i].name))
            
                    
    conn.commit()
    return True
def importDataFromdatabase(mapTableName):
    #数据库连接参数
    conn=psycopg2.connect(database='mappy',user='postgres',password = '123',host='localhost',port='5432')
    cur=conn.cursor()

    ##创建地图
    selectSql = "SELECT map_name,layer_num,layer_table_name FROM %s " %(str(mapTableName))
    cur.execute(selectSql)
    records = cur.fetchall()
    for record in records:
        mName = record[0]
        lNum = record[1]
        pMap = Map(mName,lNum)
        layerTableName = str(record[2])

        ##创建图层
        selectSql = "SELECT layer_name,layer_type,layer_code,obj_num,\
                    obj_table_name FROM %s" %(layerTableName)
        cur.execute(selectSql)
        records = cur.fetchall()
        for record in records:
            lName = record[0]
            lType = record[1]
            lSymbol = record[2]
            oNum = record[3]
            layer = Layer(lName, lType, lSymbol, oNum)
            objTableName = str(record[4])
            ##创建对象
            selectSql = "SELECT obj_name,p_num,layer_name,data_table_name FROM %s"%(objTableName)
            cur.execute(selectSql)
            records = cur.fetchall()
            for record in records:
                oName = record[0]
                pNum = record[1]
                obj = Obj(pNum,oName)
                layer_name = record[2]
                dataTableName = str(record[3])
                ##创建点，未区分点、线、面数据表
                selectSql = "SELECT x, y, obj_name, layer_name FROM %s"%(dataTableName)
                cur.execute(selectSql)
                records = cur.fetchall()
                for record in records:
                    x = int(record[0])
                    y = int(record[1])
                    point_obj_name = record[2]
                    point_layer_name = record[3]
                    if str(point_obj_name)==str(oName) and str(point_layer_name)==str(layer_name):
                        obj.appendXY(x,y)

                if(str(layer_name)==str(lName)):
                    layer.appendObj(obj)            
                   
            pMap.appendLayer(layer)
            
    return pMap

