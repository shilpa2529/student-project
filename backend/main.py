from fastapi import FastAPI, Depends, HTTPException,status
from pydantic import BaseModel, conlist
from typing import Annotated
from sqlmodel import select

from db import create_db_and_tables, SessionDep, Student_details,UserDetails ,Session
from security import router as auth_router, get_current_active_user, User ,hash_password ,verify_password ,create_access_token,authenticate_user
from calculations import totalMarks, averageMarks, gradeAssignment
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

class StudentInput(BaseModel):
    name: str
    marks: conlist(float, min_length=5, max_length=5)

class UserRegister(BaseModel):
    username: str
    password:str



@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "Student API"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserRegister,db: SessionDep,):
    existing = db.exec(select(UserDetails).where(UserDetails.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    new_user = UserDetails(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(form_data: UserRegister,db: SessionDep,):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/register")
def get_students(
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return db.exec(select(UserDetails)).all()

@app.post("/students")
def add_student(
    student: StudentInput,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
   

    total = totalMarks(student.marks)
    average = averageMarks(student.marks)
    grade = gradeAssignment(average)

    marks_str = ",".join(map(str, student.marks))

    new_student = Student_details(
        name=student.name,
        marks=student.marks,
        totalmarks=total,
        average=average,
        grade=grade
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": f"Added by {current_user.username}",
        "data": {
            "name": new_student.name,
            "marks": student.marks,
            "total": new_student.totalmarks,
            "average": new_student.average,
            "grade": new_student.grade
        }
    }

@app.put("/students/id/{id}")
def update_student(
    id: int,
    student: StudentInput,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    db_student = db.exec(
        select(Student_details).where(Student_details.id == id)
    ).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.name = student.name
    db_student.marks =student.marks
    db_student.totalmarks = totalMarks(student.marks)
    db_student.average = averageMarks(student.marks)
    db_student.grade = gradeAssignment(db_student.average)

    db.commit()
    db.refresh(db_student)

    return {"message": "Updated successfully"}

@app.get("/students")
def get_students(
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return db.exec(select(Student_details)).all()

@app.get("/students/id/{id}")
def get_student(
    id: int,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):

    student = db.exec(
        select(Student_details).where(Student_details.id == id)
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student

@app.delete("/students/id/{id}")
def delete_student(
    id: int,
    db: SessionDep,
    current_user: Annotated[User, Depends(get_current_active_user)]
):

    student = db.exec(
        select(Student_details).where(Student_details.id == id)
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": f"Deleted by {current_user.username}"}

