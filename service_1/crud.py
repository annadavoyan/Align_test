from sqlalchemy.orm import Session
from service_1 import models, schemas

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employees(db: Session, name: str = None, position: str = None, remote: bool = None):
    query = db.query(models.Employee)
    if name:
        query = query.filter((models.Employee.first_name.contains(name)) | (models.Employee.last_name.contains(name)))
    if position:
        query = query.filter(models.Employee.position == position)
    if remote is not None:
        query = query.filter(models.Employee.remote == remote)
    return query.all()

def create_employee(db: Session, employee: schemas.EmployeeCreate, employee_id: int, photo_path: str):
    db_employee = models.Employee(**employee.dict(), id=employee_id, photo=photo_path)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
