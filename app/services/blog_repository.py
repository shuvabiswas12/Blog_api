from typing import List
from app.schemas.blog_schema import BlogRequestSchema, BlogResponseSchema
from .generic_repository import GenericRepository
from pymongo.collection import Collection


class BlogRepository(GenericRepository[BlogRequestSchema, BlogResponseSchema]):

    def __init__(self, collection: Collection, requestModelType: BlogRequestSchema, responseModelType: BlogResponseSchema) -> None:
        super().__init__(collection, requestModelType, responseModelType)
