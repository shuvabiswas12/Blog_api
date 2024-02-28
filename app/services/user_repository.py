from datetime import datetime
from typing import Collection, Union

from fastapi import HTTPException
from app.services.generic_repository import GenericRepository
from passlib.context import CryptContext
from passlib.hash import bcrypt
from app.db import users_collection

# Create a password context for hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository(GenericRepository):
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)

    def __hash_password(self, password: str) -> str:
        return password_context.hash(password)

    def create(self, item: any) -> Union[any, bool, None]:
        # Item to as dict conversion
        item_dict = item.model_dump()
        existing_user = users_collection.find_one(
            {"email": item_dict["email"]})
        if existing_user:
            return False

        # Hash the password before inserting it into the DB
        item_dict["password"] = self.__hash_password(item_dict["password"])

        # Add created_at datetime field to the item_dict
        item_dict["created_at"] = datetime.now()

        try:
            # Insert the user into the database and return the inserted user's ID
            inserted_id = users_collection.insert_one(item_dict).inserted_id
            return str(inserted_id)
        except Exception as e:
            print(e)
            return None
