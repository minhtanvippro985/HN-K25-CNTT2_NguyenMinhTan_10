from sqlalchemy.orm import Session 
from typing import Any

from database import get_db, engine , Base
from fastapi import FastAPI , Depends ,status ,HTTPException  ,Request
from schemas import EmployeeSchemaCreate , EmployeeSchemaUpdate
from services import display_employees_handler , department_search_handler , search_by_id_handler ,add_emp_handler ,update_handler,delete_handler



Base.metadata.create_all(bind = engine)


app = FastAPI()


@app.get("/")
def check_server():
    return{
        "message" : "API ĐANG CHẠY"
    }

@app.get("/employees")
def show_employees(db:Session = Depends(get_db)):
    check = display_employees_handler(db=db)
    return{
        "message" : "Danh sách nhân viên",
        "data" : check
    }

@app.get("/employees/search/{department_key}")
def search_dep(department_key:str , db:Session = Depends(get_db)):
    check = department_search_handler(department_keyword=department_key , db=db)
    return{
        "message" : f"Danh sách nhân viên từ phong ban với từ khóa {department_key}",
        "data" : check 
    }


@app.get("/employees/{employee_id}")
def search_emp_id(employee_id:int , db:Session = Depends(get_db)):
    check = search_by_id_handler(employee_input=employee_id , db=db)
    return {
        "message": f"Đã tìm thấy nhân viên {employee_id}",
        "data" : check
    }

@app.post("/employee" , status_code=status.HTTP_201_CREATED)
def add_new_emp(empInput:EmployeeSchemaCreate , db:Session = Depends(get_db) ):
    check = add_emp_handler(emp_schema_input=empInput , db=db)
    return{
        "message" : "Đã thêm nhân viên thành công!",
        "data" : check
    }


@app.put("/employee/{emp_id}", status_code=status.HTTP_200_OK)
def update_emp_id(emp_id:int , emp_update_schema:EmployeeSchemaUpdate , db:Session = Depends(get_db)):
    check = update_handler(emp_id=emp_id , emp_upd_sche=emp_update_schema , db=db)
    return{
        "message" : f"Đã cập nhật thành công nhân viên có id {emp_id}",
        "data" : check
    }

@app.delete("/employee/{employee_id}" , status_code=status.HTTP_200_OK)
def delete_employee(employee_id:int , db:Session = Depends(get_db)):
    check = delete_handler(id_input = employee_id , db=db)
    return{
        "message" : f"Đã xóa thành công nhân viên có id {employee_id}",
        "data" : check
    }


def build_response(statusCode:int ,error:Any  , message:str , data):
    return {
        "statusCode" : statusCode,
        "error" : str(error),
        "message" : str(message),
        "data" : data
    } 
    


# @app.exception_handler(HTTPException)
# def throw_exc(req : Request , exc : HTTPException):
#     response = build_response(statusCode= exc.status_code , error= exc.detail , data= None , message= exc.detail)
#     return response