from fastapi import FastAPI
from routers import u_router, t_router

app = FastAPI()


@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(t_router)
app.include_router(u_router)
