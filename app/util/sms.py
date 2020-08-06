#  -*- coding: UTF-8 -*-
#  Copyright (c) 2014 The CCP project authors. All Rights Reserved.
#
#  Use of this source code is governed by a Beijing Speedtong Information Technology Co.,Ltd license
#  that can be found in the LICENSE file in the root of the web site.
#
#   http://www.yuntongxun.com
#
#  An additional intellectual property rights grant can be found
#  in the file PATENTS.  All contributing project authors may
#  be found in the AUTHORS file in the root of the source tree.

import hashlib
import base64
import datetime
import urllib.request
import json


class SMS:
    STATUS_SUCCESS = '000000'

    AccountSid = ''
    AccountToken = ''
    AppId = ''
    templateid = ''

    ServerIP = 'app.cloopen.com'
    ServerPort = '8883'
    SoftVersion = '2013-12-26'
    Iflog = True    # 是否打印日志
    Batch = ''    # 时间戳
    BodyType = 'xml'    # 包体格式，可填值：json 、xml

    def log(self, url, body, data):
        print('这是请求的URL：')
        print(url)
        print('这是请求包体:')
        print(body)
        print('这是响应包体:')
        print(data)
        print('********************************')

    # 发送模板短信
    # @param to  必选参数     短信接收彿手机号码集合,用英文逗号分开
    # @param datas 可选参数    内容数据
    # @param tempId 必选参数    模板Id
    def sendTemplateSMS(self, to, datas):
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")

        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        sig = hashlib.md5(signature.encode()).hexdigest().upper()

        # 拼接URL
        url = "https://" + self.ServerIP + ":" + self.ServerPort + "/" + self.SoftVersion\
            + "/Accounts/" + self.AccountSid + "/SMS/TemplateSMS?sig=" + sig
        print(url)

        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodestring(src.encode()).strip()
        req = urllib.request.Request(url)
        self.setHttpHeader(req)
        req.add_header("Authorization", auth)

        # 创建包体
        b = ''
        for a in datas:
            b += '<data>%s</data>' % (a)

        body = '<?xml version="1.0" encoding="utf-8"?><SubAccount><datas>' + b + '</datas><to>%s</to><templateId>%s</templateId><appId>%s</appId>\
            </SubAccount>\
            ' % (to, self.templateid, self.AppId)

        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            b = '['
            for a in datas:
                b += '"%s",' % (a)
            b += ']'
            body = '''{"to": "%s", "datas": %s, "templateId": "%s", "appId": "%s"}''' % (
                to, b, self.templateid, self.AppId)

        # req.add_data(body)

        data = ''
        try:
            res = urllib.request.urlopen(req, data=body.encode())
            data = res.read()
            res.close()

            if self.BodyType == 'json':
                # json格式
                locations = json.loads(data)
            else:
                # xml格式
                xtj = xmltojson()
                locations = xtj.main(data)
            if self.Iflog:
                self.log(url, body, data)
        except Exception as error:
            print('Exception------------------------')
            print(error)
            if self.Iflog:
                self.log(url, body, data)
            locations = {'172001': '网络错误'}

        # parse result
        return locations['statusCode']  # '000000' 为成功，其他为失败

    # 设置包头
    def setHttpHeader(self, req):
        if self.BodyType == 'json':
            req.add_header("Accept", "application/json")
            req.add_header("Content-Type", "application/json;charset=utf-8")

        else:
            req.add_header("Accept", "application/xml")
            req.add_header("Content-Type", "application/xml;charset=utf-8")
