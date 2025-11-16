from sqlmodel import SQLModel

class AuthorShortDTO(SQLModel):
    key: str
    name: str