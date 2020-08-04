# -*- coding: utf-8 -*-
"""
    Copyright (C) 2018 PPCMS
    All rights reserved

    Filename : auths.py
    Description : auths.py

    Created by mazhiyong at 2018-11-01 14:49:36

    这里采用了JWT的方式进行身份鉴权。
    随着前后端分离的趋势，基于Token的认证方式成为主流，而JWT是基于Token认证方式的一种机制，是实现单点登录认证的一种有效方法。

    基本校验流程：
    1、用户注册账号。
    2、用户登陆，成功后返回JWT token，数据库中记录token中对应的登陆时间。
    3、用户发起业务请求，header传值字段名为“Authorization”的校验字段，字段值以“JWT”开头，并与token空格隔开。
    4、服务端解析token发起校验，如果解析正确且与数据库中保存的登陆时间一致则认为校验通过

    注意：
    目前并没有对token的时效性进行校验，不排除日后进行处理。
"""

import logging
import datetime
import jwt
import time
import os
import re
from app.models.user import DBUser
from app import config
from app.util import common
from app.config import get_config
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status, Response, Depends
from passlib.context import CryptContext
from app.database import get_db_local


# create logger
logger = logging.getLogger('fastapi')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth():
    @staticmethod
    def encode_auth_token(origin_data, exp):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': exp if exp else datetime.datetime.now() + datetime.timedelta(days=7),
                'iat': datetime.datetime.now(),
                'iss': 'paperpie',
                'data': origin_data
            }

            # logger.debug('jwt encode secret_key %s', secret_key)

            encoded_jwt = jwt.encode(
                payload,
                get_config().SECRET_KEY,
                get_config().ALGORITHM
            )

            return encoded_jwt
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            secret_key = get_config().SECRET_KEY
            algorithm = get_config().ALGORITHM

            payload = jwt.decode(auth_token, secret_key, algorithms=[algorithm], options={'verify_exp': True})
            if ('data' in payload):
                return payload
            else:
                return '无效Token'
                # raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    # 校验密码
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    # 密码哈希
    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    # 用户信息校验：username和password分别校验
    @staticmethod
    def authenticate_user(username: str, password: str, db: Session):
        user = DBUser.get_by_username(db, username)
        if not user:
            return False
        if not Auth.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    def login_authenticate(username: str, password: str, db: Session):
        """
        用户登录，登录成功返回token，将登录时间写入数据库；登录失败返回失败原因
        """
        result = {}

        # 首先校验用户信息
        user = Auth.authenticate_user(username, password, db)
        if not user:
            # close db
            db.close()
            return common.falseReturn(result, '登录失败')

        # 登陆时间
        login_time = int(time.time())
        user.login_time = login_time
        DBUser.update_login_time(db, user.id, login_time)

        origin_data = {
            'user_id': user.id,
            'login_time': login_time
        }

        access_token = Auth.encode_auth_token(origin_data, None).decode()
        bearer_token = 'Bearer ' + access_token

        result['user_id'] = user.id
        result['username'] = user.username
        result['access_token'] = access_token
        result['token_type'] = "bearer"

        print(result)

        rsp = common.trueReturn(result, '登录成功')
        rsp.set_cookie(key="Bearer", value=bearer_token)
        return rsp


    @staticmethod
    def identifyAll(request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        logger.info('auth_header %s', auth_header)

        jwt_cookie = request.cookies.get('Bearer')
        logger.info('jwt_cookie %s', jwt_cookie)

        if (auth_header or jwt_cookie):
            auth_tokenArr = ''

            if(auth_header):
                auth_tokenArr = auth_header.split(" ")
                # print('auth token from auth_header. ', auth_header)
            else:
                auth_tokenArr = jwt_cookie.split(" ")
                # print('auth token from jwt_cookie. ', jwt_cookie)

            if (not auth_tokenArr or auth_tokenArr[0] != 'Bearer' or len(auth_tokenArr) != 2):
                result = common.falseContent('', '请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = Auth.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user_id = payload['data']['user_id']
                    login_time = payload['data']['login_time']

                    # get db
                    db = get_db_local()

                    user = DBUser.get_by_user_id(db, user_id)
                    if (user is None):
                        result = common.falseContent('', '找不到该用户信息')
                    else:
                        if (user.login_time == login_time):
                            returnUser = {
                                'user': user
                            }
                            result = common.trueContent(returnUser, '请求成功')
                        else:
                            result = common.falseContent('', 'Token已更改，请重新登录获取')

                    # close db
                    db.close()
                else:
                    result = common.falseContent('', payload)
        else:
            result = common.falseContent('', '没有提供认证token')

        return result
