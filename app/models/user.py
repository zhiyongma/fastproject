## -*- encoding: utf-8 -*-
"""
    Copyright(C) 2018-2019 TEST
    All rights reserved

    File : user
    Time : 2020/07/02 16:45:40
    Author : mazhiyong
    Version : 1.0
"""

from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import Session
from app.database import Base
from pydantic import BaseModel
from typing import Optional


# Pydantic model
class User(BaseModel):
    id: Optional[int] = None
    username: str
    sex: Optional[str] = None
    login_time: Optional[int] = None

    class Config:
        orm_mode = True


# DB model
class DBUser(Base):
    __tablename__ = 'test_user'

    id = Column(INTEGER(64), primary_key=True, comment='编号')
    username = Column(String(100))
    password = Column(String(100))
    sex = Column(VARCHAR(10), server_default=text("''"), comment='性别')
    login_time = Column(INTEGER(11), server_default=text("'0'"), comment='登陆时间，主要为了登陆JWT校验使用')
    create_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    @classmethod
    def add(cls, db: Session, data):
        db.add(data)
        db.commit()
        # db.refresh(data)

    @classmethod
    def get_by_user_id(cls, db: Session, user_id):
        data = db.query(cls).filter_by(id=user_id).first()

        return data

    @classmethod
    def get_by_username(cls, db: Session, username):
        data = db.query(cls).filter_by(username=username).first()

        return data

    @classmethod
    def update(cls, db: Session, username, sex):
        db.query(cls).filter_by(username=username).update({cls.sex: sex})

        db.commit()

    @classmethod
    def update_login_time(cls, db: Session, user_id, login_time):
        db.query(cls).filter_by(id=user_id).update({cls.login_time: login_time})

        db.commit()
