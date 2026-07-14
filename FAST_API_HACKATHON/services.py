from sqlalchemy.orm import Session
from models import EmployeeModel
from fastapi import FastAPI , HTTPException 

def display_employees_handler(db:Session):
    result = db.query(EmployeeModel).all()
    return result


def department_search_handler(db:Session , department_keyword:str):
    result = db.query(EmployeeModel).filter(EmployeeModel.department.ilike(f"%{department_keyword}%")).all()
    return result

def search_by_id_handler(db:Session , employee_input):
    result = db.query(EmployeeModel).filter(EmployeeModel.id == employee_input).first()
    if result is None:
        raise HTTPException(status_code= 404 , detail=f"Không tìm thấy nhân viên có id{employee_input}")
    return result

def add_emp_handler(db:Session , emp_schema_input):
    new_emp = EmployeeModel(
        full_name = emp_schema_input.full_name,
        department = emp_schema_input.department,
        position = emp_schema_input.position,
        salary = emp_schema_input.salary
    )
    try:     
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        return new_emp
    except Exception:
        db.rollback()

def update_handler(db:Session ,emp_id:int , emp_upd_sche):
    check = db.query(EmployeeModel).filter(EmployeeModel.id == emp_id).first()
    if check is None:
        raise HTTPException(status_code=404 , detail=f"Không tìm thấy nhân viên có id {emp_id}")
    try:
        check.full_name = emp_upd_sche.full_name
        check.department = emp_upd_sche.department
        check.position = emp_upd_sche.position
        check.salary = emp_upd_sche.salary
        db.commit()
        db.refresh(check)
        return check
    except Exception:
        db.rollback()

def delete_handler(db:Session , id_input):
    check = db.query(EmployeeModel).filter(EmployeeModel.id == id_input).first()
    if check is None:
        raise HTTPException(status_code=404 , detail=f"Không tìm thấy nhân viên có id {id_input}")
    try:
        db.delete(check)
        db.commit()
        return check
    except Exception:
        db.rollback()
        