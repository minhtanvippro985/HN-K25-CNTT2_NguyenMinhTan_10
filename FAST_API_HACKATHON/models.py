from database import Base
from sqlalchemy import Column , Integer , Float , String


class EmployeeModel(Base):
    __tablename__ = "employee_table"
    id = Column(Integer , autoincrement=True , primary_key= True , nullable=True)
    full_name = Column(String(255) , nullable= True )
    department = Column(String(255) , nullable= True)
    position = Column(String(255) , nullable= False)
    salary = Column(Float , nullable= False )