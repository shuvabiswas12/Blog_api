from typing import List, Union
from pymongo.collection import Collection
from app.schemas.like_schema import Like
from app.services.generic_repository import GenericRepository


class LikeRepository(GenericRepository):
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
