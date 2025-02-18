from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends
SQLITE_DATABASE_URL = "sqlite:///./todosapp.db"
engine = create_engine(url=SQLITE_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

Base = declarative_base()
