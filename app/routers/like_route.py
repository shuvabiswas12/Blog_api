from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_like_service, get_user_from_access_token, get_validated_blogId_from_query, get_validated_userId_from_query
from app.schemas.like_schema import Like
from app.schemas.user_schema import User
from app.services.like_repository import LikeRepository


like_router = APIRouter(prefix="/likes", tags=["like"])


@like_router.get("", status_code=status.HTTP_200_OK, response_model=List[Like])
async def get_likes(user_id: str = Depends(get_validated_userId_from_query), blog_id: str = Depends(get_validated_blogId_from_query), like_service: LikeRepository = Depends(get_like_service)):
    if user_id is None and blog_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Either 'blog_id' or 'user_id' should be provided by query parameter.")
    if user_id and blog_id:
        return like_service.get_all(user_id=user_id, blog_id=blog_id)

    if user_id:
        return like_service.get_all(user_id=user_id)

    if blog_id:
        return like_service.get_all(blog_id=blog_id)


@like_router.post("/{blog_id}", status_code=status.HTTP_200_OK)
async def do_like_or_unlike(blog_id: str = Depends(get_validated_blogId_from_query), like_service: LikeRepository = Depends(get_like_service), _user: User = Depends(get_user_from_access_token)):
    likes_count = like_service.get(user_id=_user.id, blog_id=blog_id)
    if likes_count is None:
        like_service.create(Like(blog_id=blog_id, user_id=_user.id))
        return True
    return like_service.delete(id=likes_count.get("id"))
