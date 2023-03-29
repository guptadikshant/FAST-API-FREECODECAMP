from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass
