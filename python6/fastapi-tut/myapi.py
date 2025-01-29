from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

students = {1: {"name": "John", "age": 17, "year": "Year 12"}}


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/")
def index():
    """End Point for HomePage"""
    return {"name": "First Data"}


@app.get("/get-student/{student_id}")
def get_student(
    student_id: int = Path(..., description="The ID of the student you want to view")
):
    """End Point to get students by their IDs"""
    if student_id in students:
        return students[student_id]

    return {"Error": "Invalid Student ID"}


@app.get("/get-by-name")
def get_by_name(
    name: Optional[str] = None,
):  # Adding a None alone will make that query parameter optional but its better to add Optional[]
    """End Point to get student by their name"""
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}

    students[student_id] = student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "This student doesn't exist"}

    if student.name != None:
        students[student_id].name = student.name

    if student.age != None:
        students[student_id].age = student.age

    if student.year != None:
        students[student_id].year = student.year

    return students[student_id]


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "This student doesn't exist"}

    del students[student_id]
    return {"Message": "Student Deleted Successfully"}
