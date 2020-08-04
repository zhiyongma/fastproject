# -*- encoding: utf-8 -*-
"""
    Copyright(C) 2018-2019 TEST
    All rights reserved

    File : common.py
    Time : 2020/08/03 11:46:23
    Author : mazhiyong
    Version : 1.0
"""

from fastapi.responses import JSONResponse


def trueReturn(data, msg):
    """ 操作成功结果 """
    result = {
        "status": True,
        "data": data,
        "msg": msg
    }
    return JSONResponse(content=result)


def falseReturn(data, msg):
    """ 操作成功结果 """
    result = {
        "status": False,
        "data": data,
        "msg": msg
    }
    return JSONResponse(content=result)


def trueContent(data, msg):
    """ 操作成功结果 """
    result = {
        "status": True,
        "data": data,
        "msg": msg
    }
    return result


def falseContent(data, msg):
    """ 操作成功结果 """
    result = {
        "status": False,
        "data": data,
        "msg": msg
    }
    return result
