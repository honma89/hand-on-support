from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.user_department import UserDepartment
from app.schemas.department import DepartmentCreate, DepartmentMemberAdd


def create_department(db: Session, data: DepartmentCreate):
    department = Department(
        name=data.name,
        description=data.description,
        head_user_id=data.head_user_id
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def add_department_member(
    db: Session,
    department_id,
    data: DepartmentMemberAdd
):
    member = UserDepartment(
        department_id=department_id,
        user_id=data.user_id,
        role_title=data.role_title
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member
