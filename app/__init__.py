# -*- encoding: utf-8 -*-
"""
    Copyright(C) 2018-2019 TEST
    All rights reserved

    File : __init__.py
    Time : 2020/07/27 15:04:35
    Author : mazhiyong
    Version : 1.0
"""

import time
import logging
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from .routers import items, users
from app.auth.auths import Auth
from fastapi.responses import JSONResponse


def create_app():
    """Create and configure an instance of the Flask application."""
    app = FastAPI()

    # create logger
    logger = logging.getLogger('fastapi')

    async def get_token_header(x_token: str = Header(...)):
        if x_token != "fake-super-secret-token":
            raise HTTPException(status_code=400, detail="X-Token header invalid")

    app.include_router(users.router)
    app.include_router(
        items.router,
        prefix="/items",
        tags=["items"],
        dependencies=[Depends(get_token_header)],
        responses={404: {"description": "Not found"}},
    )

    @app.middleware("http")
    async def process_authorization(request: Request, call_next):
        """
            在这个函数里统一对访问做权限token校验。
            1、如果是用户注册、登陆，那么不做token校验，由路径操作函数具体验证
            2、如果是其他操作，则需要从header或者cookie中取出token信息，解析出内容
               然后对用户身份进行验证，如果用户不存在则直接返回
               如果用户存在则将用户信息附加到request中，这样在后续的路径操作函数中可以直接使用。
        """
        start_time = time.time()

        # print(request.url)
        # print(request.url.path)

        if request.url.path == '/login' or request.url.path == '/register':
            logger.info('no jwt verify.')
        else:
            logger.info('jwt verify.')

            result = Auth.identifyAll(request)
            if result['status'] and result['data']:
                user = result['data']['user']

                logger.info('jwt verify success. user: %s ' % user.username)

                # state中记录用户基本信息
                request.state.user = user
            else:
                return JSONResponse(content=result)

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    return app
