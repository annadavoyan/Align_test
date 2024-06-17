from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import requests
import aiofiles
import service_1.crud as crud
import service_1.models as models
import service_1.schemas as schemas
from service_1.database import SessionLocal, engine
import logging
import os  # Import the os module

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employees/new", response_model=schemas.Employee)
async def create_employee(
    first_name: str = Form(...),
    last_name: str = Form(...),
    age: int = Form(...),
    position: str = Form(...),
    remote: bool = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Save the photo
        photo_path = f"uploads/{photo.filename}"
        os.makedirs(os.path.dirname(photo_path), exist_ok=True)
        async with aiofiles.open(photo_path, 'wb') as out_file:
            content = await photo.read()
            await out_file.write(content)
        
        # Log the photo save
        logger.info(f"Photo saved at {photo_path}")

        # Send photo to service 2 and get numeric employee ID
        with open(photo_path, "rb") as image_file:
            response = requests.post("http://localhost:9000/image", files={"file": image_file})
            logger.info(f"Service 2 response: {response.json()}")
            if response.status_code != 200:
                logger.error("Error processing image with Service 2")
                raise HTTPException(status_code=500, detail="Error processing image")
            numeric_employee_id = response.json()["employee_id"]

        logger.info(f"Numeric employee ID: {numeric_employee_id}")

        employee_data = schemas.EmployeeCreate(
            first_name=first_name,
            last_name=last_name,
            age=age,
            position=position,
            remote=remote
        )
        
        db_employee = crud.create_employee(db=db, employee=employee_data, employee_id=numeric_employee_id, photo_path=photo_path)
        return db_employee

    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/employees/list", response_model=list[schemas.Employee])
def read_employees(name: str = None, position: str = None, remote: bool = None, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, name=name, position=position, remote=remote)
    return employees

@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee
