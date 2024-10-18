from fastapi import APIRouter

u_router = APIRouter(prefix='/user', tags=['user'])


@u_router.get('/')
async def all_users():
    pass


@u_router.get('/user_id')
async def user_by_id():
    pass


@u_router.post('/create')
async def create_user():
    pass


@u_router.put('/update')
async def update_user():
    pass


@u_router.delete('/delete')
async def delete_user():
    pass
