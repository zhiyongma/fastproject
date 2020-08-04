# -*- coding: utf-8 -*-
"""
    Copyright (C) 2018 PPCMS
    All rights reserved

    Filename : dateencoder.py
    Description : 处理datetime类型数据json转化异常问题.
                  ex:datetime.datetime is not JSON serializable

    Created by mazhiyong at 2018-11-01 14:42:26
"""

import datetime
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            print(obj.strftime('%Y-%m-%d %H:%M:%S'))
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)



