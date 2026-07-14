from pydantic import BaseModel


class EmployeeSchemaCreate(BaseModel):
    full_name:str
    department:str
    position:str
    salary:float

class EmployeeSchemaUpdate(BaseModel):
    full_name:str
    department:str
    position:str
    salary:float