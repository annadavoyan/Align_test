from sqlalchemy.orm import Session
import employee_app.models as models
import employee_app.schemas as schemas

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def create_employee(db: Session, employee: schemas.EmployeeCreate, photo_path: str):
    db_employee = models.Employee(**employee.dict(), photo=photo_path)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
