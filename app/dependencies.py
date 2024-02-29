from fastapi import Depends, HTTPException, Header
from app.schemas.user_schema import User
from app.services.blog_repository import BlogRepository
from app.db import blogs_collection
from app.services.user_repository import UserRepository
from app.db import users_collection


def get_blog_service():
    return BlogRepository(collection=blogs_collection)


def get_user_service():
    return UserRepository(collection=users_collection)


async def get_user_from_access_token(user_service: UserRepository = Depends(get_user_service), access_token: str = Header()) -> User:
    try:
        _user = user_service.get_current_user(token=access_token)
        return User(**_user)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"{e}")
