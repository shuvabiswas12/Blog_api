from app.services.blog_repository import BlogRepository
from app.db import blogs_collection
from app.services.user_repository import UserRepository
from app.db import users_collection


def get_blog_service():
    return BlogRepository(collection=blogs_collection)


def get_user_service():
    return UserRepository(collection=users_collection)
