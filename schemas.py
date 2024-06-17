from pydantic import BaseModel

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    position: str
    remote: bool

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    photo: str

    class Config:
        orm_mode = True
