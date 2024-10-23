from fastapi import APIRouter


t_router = APIRouter(prefix='/task', tags=['task'])


@t_router.get('/')
async def all_tasks():
    pass


@t_router.get('/task_id')
async def task_by_id():
    pass


@t_router.post('/create')
async def create_task():
    pass


@t_router.put('/update')
async def update_task():
    pass


@t_router.delete('/delete')
async def delete_task():
    pass
