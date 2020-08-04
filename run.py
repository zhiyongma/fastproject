# -*- encoding: utf-8 -*-
"""
    Copyright(C) 2018-2019 PAPERPIE
    All rights reserved

    File : run.py
    Time : 2019/03/20 16:21:11
    Author : mazhiyong
    Version : 1.0
"""

from app import create_app
import logging
from fastapi.logger import logger as fastapi_logger
from logging.handlers import RotatingFileHandler

app = create_app()


# 将日志保存到文件中
formatter = logging.Formatter(
    "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
handler = RotatingFileHandler('/data/log/abc.log', backupCount=0)
logging.getLogger().setLevel(logging.NOTSET)
fastapi_logger.addHandler(handler)
handler.setFormatter(formatter)

fastapi_logger.info('****************** Starting Server *****************')
