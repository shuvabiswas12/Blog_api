from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class CommentRequstSchema(BaseModel):
    comment: str = Field(max_length=1000)
    user_id: Optional[str] = Field(default=None)
    blog_id: Optional[str] = Field(default=None)


class User(BaseModel):
    id: str
    name: str
    email: EmailStr


class CommentResponseSchema(BaseModel):
    id: str
    comment: str
    user_id: str
    user: User | None = None
    created_at: datetime
    updated_at: datetime | None = None
