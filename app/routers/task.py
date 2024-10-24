from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete


t_router = APIRouter(prefix='/task', tags=['task'])


@t_router.get('/')
async def all_tasks(db: Session = Depends(get_db)):
    tasks = db.execute(select(Task)).scalars().all()
    return tasks


@t_router.get('/task_id')
async def task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@t_router.post('/create')
async def create_task(task: CreateTask, user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User  was not found")

    new_task = Task(**task.dict(), user_id=user_id)
    db.execute(insert(Task).values(new_task))
    db.commit()

    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@t_router.put('/update')
async def update_task(task_id: int, task: UpdateTask, db: Session = Depends(get_db)):
    existing_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if existing_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    updated_task = existing_task.copy(update=task.dict())
    db.execute(update(Task).where(Task.id == task_id).values(updated_task.dict()))
    db.commit()

    return updated_task


@t_router.delete('/delete')
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    result = db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"detail": "Task deleted successfully"}
