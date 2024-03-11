from fastapi import Depends, HTTPException, Header
from app.schemas.user_schema import User
from app.services.blog_repository import BlogRepository
from app.services.comment_respository import CommentRepository
from app.services.like_repository import LikeRepository
from app.services.user_repository import UserRepository
from app.helpers.objectId_helper import check_objectId
from app.db import users_collection, likes_collection, blogs_collection, comments_collection


def get_blog_service():
    return BlogRepository(collection=blogs_collection)


def get_user_service():
    return UserRepository(collection=users_collection)


def get_like_service():
    return LikeRepository(collection=likes_collection)


def get_comment_service():
    return CommentRepository(collection=comments_collection)


async def get_user_from_access_token(user_service: UserRepository = Depends(get_user_service), access_token: str = Header()) -> User:
    try:
        _user = user_service.get_current_user(token=access_token)
        return User(**_user)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"{e}")


async def get_validated_blogId_from_query(blog_id: str = None, blog_service: BlogRepository = Depends(get_blog_service)):
    if blog_id is None:
        return None

    validate_objectId(blog_id)

    _blog = blog_service.get(id=blog_id)
    if _blog is None:
        raise HTTPException(status_code=404, detail="Blog not found!")
    return _blog.get("id")


async def get_validated_userId_from_query(user_id: str = None, user_service: UserRepository = Depends(get_user_service)):
    if user_id is None:
        return None

    _user = user_service.get(id=user_id)
    if _user is None:
        raise HTTPException(status_code=404, detail="User not found!")
    return _user.get("id")


async def validate_objectId(id: str) -> str:
    if id is None:
        raise HTTPException(status_code=400, detail="ID is required!")
    try:
        if check_objectId(str(id)):
            return id
    except ValueError as e:
        raise HTTPException(status_code=400, detail="ID is invalid!")
