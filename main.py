from fastapi import (
    FastAPI,
    Request,
    Depends,
    Path,
    HTTPException,
    status
)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Annotated
from database import engine, SessionLocal
from models import Base, Todos
from routers import auth, todos
import signal
import os
import logging

app = FastAPI(
    title="TODOS",
    description="You can access Todo API(s) from here",
    version="1.0.0",
)


@app.get("/", tags=["Home"])
async def root():
    return RedirectResponse(url="/docs", status_code=301)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
