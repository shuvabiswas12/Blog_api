from app.services.blog_repository import BlogRepository
from app.db import blogs_collection


def get_blog_service():
    return BlogRepository(collection=blogs_collection)
