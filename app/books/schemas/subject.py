from pydantic import BaseModel


class SubjectBase(BaseModel):
    subject: str
    book_id: int

class SubjectCreate(SubjectBase):
    pass

class SubjectRead(SubjectBase):
    id: int