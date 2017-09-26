# -*- coding: utf-8 -*-
import psycopg2
##数据库连接参数
conn=psycopg2.connect(database='mappy',user='postgres',password = '123',host='localhost',port='5432')
cur=conn.cursor()
##创建数据表及字段 map_table,layer_table,obj_table,data_table
##  map_table
cur.execute("CREATE TABLE map_table(\
            map_name character varying ,\
            layer_num integer,\
            layer_table_name character varying)")
##  layer_table
cur.execute("CREATE TABLE layer_table(\
            layer_name character varying ,\
            layer_type character varying,\
            layer_code character varying,\
            obj_num integer,\
            obj_table_name character varying)")
##  obj_table
cur.execute("CREATE TABLE obj_table(\
            obj_name character varying ,\
            p_num integer,\
            layer_name character varying,\
            data_table_name character varying)")
##  point_table
cur.execute("CREATE TABLE point_table(\
            x bigint,\
            y bigint,\
            obj_name character varying,\
            layer_name character varying,\
            point_geom geometry)")
##  polyline_table
cur.execute("CREATE TABLE polyline_table(\
            x bigint,\
            y bigint,\
            obj_name character varying,\
            layer_name character varying,\
            polyline_geom geometry)")
## polygon_table
cur.execute("CREATE TABLE polygon_table(\
            x bigint,\
            y bigint,\
            obj_name character varying,\
            layer_name character varying,\
            polygon_geom geometry)")
print("数据表创建成功")
conn.commit()
