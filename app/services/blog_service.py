from app.schemas.blog_schema import BlogRequestSchema, BlogResponseSchema
from .generic_service import GenericService
from app.db import blogs_collection

BlogService = GenericService(requestModelType=BlogRequestSchema,
                             responseModelType=BlogResponseSchema, collection=blogs_collection)
