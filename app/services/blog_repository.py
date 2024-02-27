from .generic_repository import GenericRepository
from pymongo.collection import Collection


class BlogRepository(GenericRepository):

    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
