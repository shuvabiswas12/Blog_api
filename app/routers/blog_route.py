from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Header
from app.schemas.blog_schema import BlogRequestSchema, BlogResponseSchema
from app.dependencies import get_blog_service, get_user_from_access_token, get_user_service
from app.schemas.user_schema import User
from app.services.blog_repository import BlogRepository
from app.services.user_repository import UserRepository

blog_router = APIRouter(prefix="/blogs", tags=["blog"])


@blog_router.get("", status_code=status.HTTP_200_OK, response_model=List[BlogResponseSchema])
async def get_blogs(service: BlogRepository = Depends(get_blog_service)):
    return service.get_all()


@blog_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=BlogResponseSchema)
async def get_blog(id: str, service: BlogRepository = Depends(get_blog_service)):
    result = service.get(id=id)
    if result is None:
        raise HTTPException(status_code=404, detail="Not Found!")
    return result


@blog_router.post("", status_code=status.HTTP_201_CREATED, response_model=BlogResponseSchema)
async def create_blog(blog: BlogRequestSchema, service: BlogRepository = Depends(get_blog_service), _user: User = Depends(get_user_from_access_token)):
    blog_dict = blog.model_dump()

    blog_dict["user_id"] = str(_user.id)

    result = service.create(item=blog_dict)

    if result is None:
        raise HTTPException(
            status_code=500, detail="Blog could not be created!")
    return result


@blog_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: str, service: BlogRepository = Depends(get_blog_service), _user: User = Depends(get_user_from_access_token)):
    blog_to_delete = service.get(id=id)

    if blog_to_delete is None:
        raise HTTPException(
            status_code=404, detail="Blog could not be found! Maybe blog has been deleted already.")

    if blog_to_delete.get('user_id') != _user.id:
        raise HTTPException(
            status_code=400, detail="Access denied.")

    result = service.delete(id=id)

    if result:
        return "Done"
    raise HTTPException(
        status_code=404, detail="Blog could not be found! Maybe blog has been deleted already.")


@blog_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=BlogResponseSchema)
async def update_blog(id: str, item: BlogRequestSchema, service: BlogRepository = Depends(get_blog_service)):
    result = service.update(id=id, item=item)
    if result is None:
        raise HTTPException(
            status_code=500, detail="Blog could not be updated!")
    return result
