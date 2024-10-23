from fastapi import APIRouter
from app.models import *
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

u_router = APIRouter(prefix='/user', tags=['user'])


@u_router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users


@u_router.get('/user_id')
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@u_router.post('/create')
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.execute(select(User).where(User.id == user.id)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="User  with this ID already exists")

    existing_username = db.execute(select(User).where(User.username == user.username)).scalar_one_or_none()
    if existing_username:
        raise HTTPException(status_code=400, detail="User  with this username already exists")

    new_user = User(**user.dict())
    db.execute(insert(User).values(new_user))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@u_router.put('/update/{user_id}')
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    up_user = update(User).where(User.id == user_id).values(**user.dict())
    result = db.execute(up_user)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User  was not found")
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User  update is successful!'}


@u_router.delete('/delete/{user_id}')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    del_user = delete(User).where(User.id == user_id)
    result = db.execute(del_user)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User  was not found")
    return {'status_code': status.HTTP_204_NO_CONTENT, 'transaction': 'User  deleted successfully'}
