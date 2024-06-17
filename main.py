from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import aiofiles

import employee_app.crud as crud
import employee_app.models as models
import employee_app.schemas as schemas
from employee_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees/", response_model=schemas.Employee)
async def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), photo: UploadFile = File(...)):
    photo_path = f"uploads/{photo.filename}"
    async with aiofiles.open(photo_path, 'wb') as out_file:
        content = await photo.read()
        await out_file.write(content)
    return crud.create_employee(db=db, employee=employee, photo_path=photo_path)

@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@app.get("/employees/photo/{employee_id}")
def get_employee_photo(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None or db_employee.photo is None:
        raise HTTPException(status_code=404, detail="Employee photo not found")
    return FileResponse(db_employee.photo)
