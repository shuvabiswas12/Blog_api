from fastapi import Depends
from app.services.blog_repository import BlogRepository
from app.db import blogs_collection
from app.schemas.blog_schema import BlogRequestSchema, BlogResponseSchema


def get_blog_service():
    return BlogRepository(collection=blogs_collection, requestModelType=BlogRequestSchema, responseModelType=BlogResponseSchema)
