# -*- encoding: utf-8 -*-
"""
    Copyright(C) 2018-2019 TEST
    All rights reserved

    File : database.py
    Time : 2020/08/01 20:21:48
    Author : mazhiyong
    Version : 1.0
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import get_config


# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine(get_config().SQLALCHEMY_DATABASE_URI)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(bind=engine)


# db Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_local():
    return SessionLocal()
