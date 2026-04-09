from typing import Annotated,List
from fastapi import Depends, FastAPI
from sqlalchemy import Column, JSON
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

class UserDetails(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str  # hashed password

class Student_details(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    marks: List[float] = Field(sa_column=Column(JSON))
    totalmarks: int | None = None
    average: float | None = None
    grade: str | None = None


sqlite_file_name = "database.db"  # single database
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]