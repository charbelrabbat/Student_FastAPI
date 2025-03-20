from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pymongo import MongoClient
from bson import ObjectId

print('hello')

# MongoDB client setup
client = MongoClient("mongodb://localhost:27017")
db = client.students_db  # Database name
students_collection = db.students  # Collection name

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for validation
class Student(BaseModel):
    id: int
    name: str
    grade: float

# Pydantic model for response (excluding MongoDB's ObjectId)
class StudentInDB(Student):
    _id: str

# Utility function to convert MongoDB document to Pydantic model
def student_helper(student) -> dict:
    return {
        "id": student["id"],
        "name": student["name"],
        "grade": student["grade"],
        "_id": str(student["_id"]),
    }

# Create a student (POST)
@app.post("/students/", response_model=StudentInDB)
async def create_student(student: Student):
    student_dict = student.dict()
    result = students_collection.insert_one(student_dict)
    student_dict["_id"] = str(result.inserted_id)
    return student_dict

# Read all students (GET)
@app.get("/students/", response_model=List[StudentInDB])
async def get_students():
    students = []
    for student in students_collection.find():
        students.append(student_helper(student))
    return students

# Read a student by ID (GET)
@app.get("/students/{student_id}", response_model=StudentInDB)
async def get_student(student_id: int):
    student = students_collection.find_one({"id": student_id})
    if student is not None:
        return student_helper(student)
    raise HTTPException(status_code=404, detail="Student not found")

# Update a student by ID (PUT)
@app.put("/students/{student_id}", response_model=StudentInDB)
async def update_student(student_id: int, updated_student: Student):
    student = students_collection.find_one({"id": student_id})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = updated_student.dict()
    students_collection.update_one({"id": student_id}, {"$set": update_data})
    updated_student = students_collection.find_one({"id": student_id})
    return student_helper(updated_student)

# Delete a student by ID (DELETE)
@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    result = students_collection.delete_one({"id": student_id})
    if result.deleted_count == 1:
        return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")
