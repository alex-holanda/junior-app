from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.service.client_service import scheduler

from .database import database
from .router import client_router, user_router

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://seu-dominio.com",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    await database.connect()
    yield
    scheduler.shutdown()
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(client_router)
