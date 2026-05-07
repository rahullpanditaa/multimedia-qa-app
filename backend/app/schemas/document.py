from datetime import datetime
from pydantic import BaseModel

class DocumentCreate(BaseModel):
    filename: str

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    filepath: str
    created_at: datetime

    class Config:
        from_attributes = True