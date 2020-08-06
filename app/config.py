# -*- coding: utf-8 -*-
"""
    Copyright(C) 2018 PPCMS
    All rights reserved

    Filename: config.py
    Description: config.py

    Created by mazhiyong at 2018-11-01 14:41:55
"""

import os


class Config:
    SITE_NAME = u'PPCMS'

    # Consider SQLALCHEMY_COMMIT_ON_TEARDOWN harmful
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SQLALCHEMY_POOL_RECYCLE = 10
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_ECHO = False

    MYSQL_USER = 'pony'
    MYSQL_PASS = ''
    MYSQL_HOST = 'rm-2zee5e5ytvd02o9e9no.mysql.rds.aliyuncs.com'
    MYSQL_PORT = '3306'
    MYSQL_DB = 'bookcrawl'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)


class ProductionConfig(Config):
    DEBUG = True

    # mysql configuration
    MYSQL_USER = ''
    MYSQL_PASS = ''
    MYSQL_HOST = ''
    MYSQL_PORT = '3306'
    MYSQL_DB = ''

    if (len(MYSQL_USER) > 0 and len(MYSQL_PASS) > 0 and len(MYSQL_HOST) > 0 and len(MYSQL_PORT) > 0 and len(MYSQL_DB) > 0):
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}


def get_config():
    config_name = os.getenv('FASTAPI_ENV') or 'default'
    return config[config_name]
