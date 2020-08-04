# -*- encoding: utf-8 -*-
"""
    Copyright(C) 2018-2019 TEST
    All rights reserved

    File : items.py
    Time : 2020/07/27 14:32:51
    Author : mazhiyong
    Version : 1.0
"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}