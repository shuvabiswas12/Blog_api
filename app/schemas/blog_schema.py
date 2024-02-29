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
            "image": "Here is the image's url."
        }


class BlogResponseSchema(BlogRequestSchema):
    id: str
    user_id: str
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    class ConfigDict:
        json_schema_extra = {
            "title": "Bangladesh is a illiterate country!",
            "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. ",
            "image": "An image url",
            "id": "65e01b62b95a77199a5f5348",
            "user_id": "65e01062a3289c1c977bfc5d",
            "created_at": "2024-02-29T11:51:30.760868",
            "updated_at": "2024-02-29T11:51:30.760868"
        }
