from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# group together /documents path operations
router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=DocumentResponse)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    document = Document(filename=payload.filename)

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

@router.get("/", response_model=list[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    """
    Return all uploaded documents.
    """

    documents = (
        db.query(Document)

        .order_by(Document.id.desc())

        .all()
    )

    return documents