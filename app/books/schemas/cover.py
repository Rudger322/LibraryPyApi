from pydantic import BaseModel


class CoverBase(BaseModel):
    book_id: int


class CoverCreate(CoverBase):
    cover_file: str  # Путь к файлу


class CoverRead(BaseModel):
    id: int
    cover_file: str
    book_id: int

    model_config = {"from_attributes": True}


class CoverURL(BaseModel):
    """URL для доступа к обложке"""
    id: int
    url: str