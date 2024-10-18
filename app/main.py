from fastapi import FastAPI
from routers import task, user

app = FastAPI()


@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.t_router)
app.include_router(user.u_router)
