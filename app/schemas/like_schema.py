from datetime import datetime
from pydantic import BaseModel


class Like(BaseModel):
    blog_id: str
    user_id: str
    created_at: datetime
