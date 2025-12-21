from pydantic import BaseModel


class CoverBase(BaseModel):
    cover_file: int
    book_id: int


from pydantic import BaseModel, HttpUrl


class CoverCreate(BaseModel):
    cover_url: str
    book_id: int


class CoverRead(BaseModel):
    id: int
    cover_url: str
    book_id: int

    model_config = {"from_attributes": True}