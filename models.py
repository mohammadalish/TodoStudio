from database import Base
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Boolean,
                        ForeignKey,
                        DateTime
                        )
from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String, index=True)
    is_active = Column(Boolean, default=False, index=True)
    role = Column(String, index=True)


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    priority = Column(Integer, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    complete = Column(Boolean, default=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))


# class Projects(Base):
#     __tablename__ = "projects"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String, index=True)
#     start_date = Column(DateTime, default=datetime.utcnow)
#     end_date = Column(DateTime, nullable=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
