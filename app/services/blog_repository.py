from datetime import datetime
from typing import Any
from .generic_repository import GenericRepository
from pymongo.collection import Collection


class BlogRepository(GenericRepository):

    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)

    def create(self, item: any) -> Any | None:
        try:
            item["created_at"] = datetime.now()
            result = self.collection.insert_one(item)
            item["id"] = str(result.inserted_id)
            return item
        except Exception as e:
            print(e)
            return None
