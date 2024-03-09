from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_comment_service, get_user_from_access_token, get_validated_blogId_from_query

from app.schemas.comment_schema import CommentRequstSchema, CommentResponseSchema
from app.schemas.user_schema import User
from app.services.comment_respository import CommentRepository

comments_router = APIRouter(prefix="/comments", tags=["comments"])


@comments_router.post("/{blog_id}", status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentRequstSchema, blog_id: str = Depends(get_validated_blogId_from_query), _user: User = Depends(get_user_from_access_token), comment_service: CommentRepository = Depends(get_comment_service)):
    comment.user_id = _user.id
    comment.blog_id = blog_id
    newly_created_comment = comment_service.create(comment)
    if newly_created_comment is None:
        return HTTPException(status_code=400, detail="Comment could not be created!")

    return CommentRequstSchema(**newly_created_comment)


@comments_router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=List[CommentResponseSchema])
def get_comments_by_blogId(blog_id: str = Depends(get_validated_blogId_from_query), comment_service: CommentRepository = Depends(get_comment_service)):
    return comment_service.get_all(blog_id=blog_id)


@comments_router.get("/", status_code=status.HTTP_200_OK, response_model=List[CommentResponseSchema])
def get_comments_by_userId(_user: User = Depends(get_user_from_access_token), comment_service: CommentRepository = Depends(get_comment_service)):
    return comment_service.get_all(user_id=_user.id)
