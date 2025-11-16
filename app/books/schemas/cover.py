from pydantic import BaseModel


class CoverBase(BaseModel):
    cover_file: int
    book_id: int

class CoverCreate(CoverBase):
    pass

class CoverRead(CoverBase):
    id: int