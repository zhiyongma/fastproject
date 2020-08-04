# -*- encoding: utf-8 -*-
"""
    Copyright(C) 2018-2019 TEST
    All rights reserved

    File : users.py
    Time : 2020/07/27 14:32:44
    Author : mazhiyong
    Version : 1.0
"""

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auths import Auth
from app.models.user import User, DBUser

router = APIRouter()


@router.post("/register", response_model=User)
async def register(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 密码加密
    password = Auth.get_password_hash(form_data.password)

    db_user = DBUser.get_by_username(db, form_data.username)
    if db_user:
        return db_user

    db_user = DBUser(username=form_data.username, password=password)
    DBUser.add(db, db_user)

    request.session['test'] = "test"

    return db_user


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return Auth.login_authenticate(form_data.username, form_data.password, db)


@router.post("/users/me/", response_model=User)
async def read_users_me(request: Request):
    user = request.state.user
    return user
