import argparse
import os
import re
from time import sleep
from typing import Optional, Any

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

# model >>>
import argparse
import numpy as np
import sys
import os
import json
from pathlib import Path
import shutil

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import mysql.connector

# 连接到 MySQL 数据库
conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='admin',
    database='school_map'
)

class Item(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None


class PinLun(BaseModel):
    pid: Optional[int] = None
    pinlun: Optional[str] = None

class ZhuCe(BaseModel):
    usr: Optional[str] = None
    pwd: Optional[str] = None
    loginForm: Optional[Any] = None


class HuaTi(BaseModel):
    # pid: Optional[int] = None
    name: Optional[str] = None
    huati: Optional[str] = None
    url: Optional[str] = None


# 定义添加用户的接口
@app.post("/userAdd")
def admin_add(zhuce: ZhuCe):
    # 创建游标对象
    cursor = conn.cursor()
    kwargs = jsonable_encoder(zhuce)
    print("kwargs", kwargs)
    values = kwargs.get("loginForm")
    values = values.get("usr"),values.get("usr"), values.get("pwd")
    print("values", values)
    sql = "INSERT INTO admin(admin_name,admin_nickname,admin_password) VALUES (%s, %s, %s);"
    values = list(values)
    print("values", type(values), values)
    # 执行SQL语句
    num = conn.cursor().execute(sql, values)
    last_insert_id = cursor.lastrowid
    print("插入的id为：", last_insert_id)
    # 提交事务
    conn.commit()
    # 关闭游标对象
    cursor.close()

# 定义添加活动的接口
@app.post("/huodongAdd")
def huodong_add(item: Item):
    # 创建游标对象
    cursor = conn.cursor()
    kwargs = jsonable_encoder(item)
    print("kwargs >>>", kwargs)
    values = kwargs.get("name"), kwargs.get("content")
    print("values", values)
    sql = "INSERT INTO huodong(name,content) VALUES (%s, %s);"
    values = list(values)
    print("values", type(values), values)
    # 执行SQL语句
    num = conn.cursor().execute(sql, values)
    last_insert_id = cursor.lastrowid
    print("插入的id为：", last_insert_id)
    # 提交事务
    conn.commit()
    # 关闭游标对象
    cursor.close()


# 定义添加评论的接口
@app.post("/pinlunAdd")
def pinlun_add(pinlun: PinLun):
    # 创建游标对象
    cursor = conn.cursor()
    kwargs = jsonable_encoder(pinlun)
    print("kwargs", kwargs)
    values = kwargs.get("pid"), kwargs.get("pinlun")
    print("values", values)
    sql = "INSERT INTO pinlun(pid,content) VALUES (%s, %s);"
    values = list(values)
    print("values", type(values), values)
    # 执行SQL语句
    num = conn.cursor().execute(sql, values)
    last_insert_id = cursor.lastrowid
    print("插入的id为：", last_insert_id)
    # 提交事务
    conn.commit()
    # 关闭游标对象
    cursor.close()



# 定义添加话题评论的接口
@app.post("/pinlunHuaTiAdd")
def pinlunHuaTiAdd(pinlun: PinLun):
    # 创建游标对象
    cursor = conn.cursor()
    kwargs = jsonable_encoder(pinlun)
    print("kwargs", kwargs)
    values = kwargs.get("pid"), kwargs.get("pinlun")
    print("values", values)
    sql = "INSERT INTO huatipinlun(pid,content) VALUES (%s, %s);"
    values = list(values)
    print("values", type(values), values)
    # 执行SQL语句
    num = conn.cursor().execute(sql, values)
    last_insert_id = cursor.lastrowid
    print("插入的id为：", last_insert_id)
    # 提交事务
    conn.commit()
    # 关闭游标对象
    cursor.close()


# 定义添加话题的接口
@app.post("/huatiAdd")
def huati_add(huati: HuaTi):
    # 创建游标对象
    cursor = conn.cursor()
    kwargs = jsonable_encoder(huati)
    print("kwargs 话题Add", kwargs)
    values = kwargs.get("name"), kwargs.get("huati"), kwargs.get("url")
    print("values", values)
    sql = "INSERT INTO huati(name,huati,url) VALUES (%s, %s, %s);"
    values = list(values)
    print("values", type(values), values)
    # 执行SQL语句
    num = conn.cursor().execute(sql, values)
    last_insert_id = cursor.lastrowid
    print("插入的id为：", last_insert_id)
    # 提交事务
    conn.commit()
    # 关闭游标对象
    cursor.close()


@app.delete("/huodongDel/{id}", summary="")
async def huodongDel(id: int):
    # 创建游标对象
    cursor = conn.cursor()
    print("id >>> ", id)
    sql = """delete from huodong 
                           WHERE id=%s;"""
    conn.cursor().execute(sql, (id,))
    # 提交事务
    conn.commit()
    # 关闭游标对象
    cursor.close()


@app.delete("/pinlunDel/{id}", summary="")
async def pinlunDel(id: int):
    # 创建游标对象
    cursor = conn.cursor()
    print("id >>> ", id)
    sql = """delete from pinlun 
                           WHERE id=%s;"""
    conn.cursor().execute(sql, (id,))
    # 提交事务
    conn.commit()
    # 关闭游标对象
    cursor.close()


@app.get("/huodongList", summary="huodongList")
async def huodongList():
    # 创建游标对象
    cursor = conn.cursor()
    # 执行 SQL 查询
    query = "SELECT * FROM huodong"
    cursor.execute(query)
    # 获取查询结果
    result = cursor.fetchall()
    print("result 活动>>>", result)
    list = []
    for row in result:
        map = {}
        print(row)
        map['id'] = row[0]
        map['name'] = row[1]
        map['content'] = row[2]
        list.append(map)
    print("list", list)
    # 关闭游标对象
    cursor.close()
    return list


@app.get("/huatiList", summary="huodongList")
async def huatiList():
    # 创建游标对象
    cursor = conn.cursor()
    # 执行 SQL 查询
    query = "SELECT * FROM huati"
    cursor.execute(query)
    # 获取查询结果
    result = cursor.fetchall()
    print("result 活动>>>", result)
    list = []
    for row in result:
        map = {}
        print(row)
        map['id'] = row[0]
        map['name'] = row[1]
        map['huati'] = row[2]
        map['url'] = row[3]
        list.append(map)
    print("list", list)
    # 关闭游标对象
    cursor.close()
    return list


@app.get("/pinlunList/{id}", summary="弹出框评论列表")
async def pinlunList(id: int):
    # 创建游标对象
    cursor = conn.cursor()
    # 执行 SQL 查询
    query = "SELECT * FROM pinlun where pid = %s;"
    cursor.execute(query, (id,))
    # 获取查询结果
    result = cursor.fetchall()
    print("result 评论>>>", result)
    list = []
    for row in result:
        map = {}
        print(row)
        map['id'] = row[0]
        map['content'] = row[2]
        list.append(map)
    print("list", list)
    # 关闭游标对象
    cursor.close()
    return list


@app.get("/huatipinlunList/{id}", summary="弹出框话题评论列表")
async def huatipinlunList(id: int):
    # 创建游标对象
    cursor = conn.cursor()
    # 执行 SQL 查询
    query = "SELECT * FROM huatipinlun where pid = %s;"
    cursor.execute(query, (id,))
    # 获取查询结果
    result = cursor.fetchall()
    print("result 话题评论>>>", result)
    list = []
    for row in result:
        map = {}
        print(row)
        map['id'] = row[0]
        map['content'] = row[2]
        list.append(map)
    print("list", list)
    # 关闭游标对象
    cursor.close()
    return list


@app.get("/pinlunList", summary="后台管理-评论")
async def pinlunList():
    # 创建游标对象
    cursor = conn.cursor()
    # 执行 SQL 查询
    query = "SELECT * FROM pinlun;"
    cursor.execute(query)
    # 获取查询结果
    result = cursor.fetchall()
    print("result 后台管理-评论>>>", result)
    list = []
    for row in result:
        map = {}
        print(row)
        map['id'] = row[0]
        map['content'] = row[2]
        list.append(map)
    print("list", list)
    # 关闭游标对象
    cursor.close()
    return list


@app.get("/bb", summary="地区")
async def bb():
    # 创建游标对象
    cursor = conn.cursor()
    # 执行 SQL 查询
    query = "SELECT * FROM diqu"
    cursor.execute(query)

    # 获取查询结果
    result = cursor.fetchall()
    print("result 地区 >>>", result)
    name = []
    value = []
    for row in result:
        print(row)
        name.append(row[1])
        value.append(row[2])
    # 关闭游标对象
    cursor.close()
    return {"code": 200, "name": name, "value": value}


uvicorn.run(app, host="127.0.0.1", port=8096)

# if __name__ == '__main__':
#     backendApi("model 预热")
#     # 启动创建的实例app，设置启动ip和端口号
#     uvicorn.run(app, host="127.0.0.1", port=8069)
