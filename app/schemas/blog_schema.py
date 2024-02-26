from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BlogRequestSchema(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=1000)
    image: Optional[str] = Field(default=None)

    class ConfigDict:
        json_schema_extra = {
            "title": "This is a dummy title!",
            "description": "This is a dummy description!",
            "image": "Here is the image's url.",
        }


class BlogResponseSchema(BlogRequestSchema):
    id: str
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
