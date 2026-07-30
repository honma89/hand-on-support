from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.document import Document, DocumentCategory

from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("", response_model=list[DocumentResponse])
def list_documents(
    category: DocumentCategory | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Document)

    if category:
        query = query.filter(Document.category == category)

    return query.order_by(Document.created_at.desc()).all()


@router.post("", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    new_document = Document(
        **document.model_dump(),
        uploaded_by=current_admin.id
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document
