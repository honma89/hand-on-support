from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.department import Department
from app.models.user_department import UserDepartment

from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentMemberAdd,
    DepartmentMemberResponse
)

from app.services.department_service import (
    create_department,
    add_department_member
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.get("", response_model=list[DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).order_by(Department.name).all()


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: str, db: Session = Depends(get_db)):
    return db.query(Department).filter(
        Department.id == department_id
    ).first()


@router.get(
    "/{department_id}/members",
    response_model=list[DepartmentMemberResponse]
)
def list_department_members(
    department_id: str,
    db: Session = Depends(get_db)
):
    return db.query(UserDepartment).filter(
        UserDepartment.department_id == department_id
    ).all()


@router.post("", response_model=DepartmentResponse)
def create_department_endpoint(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return create_department(db, department)


@router.post(
    "/{department_id}/members",
    response_model=DepartmentMemberResponse
)
def add_member_endpoint(
    department_id: str,
    member: DepartmentMemberAdd,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    return add_department_member(db, department_id, member)
