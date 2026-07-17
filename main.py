# Author: Orian Ben Old
from fastapi import FastAPI
from .app.controller.poll_controller import router as poll_router
from .app.repository.database import database

app = FastAPI(title="Poll Service")
app.include_router(poll_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
