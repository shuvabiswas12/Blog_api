from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Like(BaseModel):
    blog_id: str
    user_id: str
    created_at: Optional[datetime] = Field(default=datetime.now())
