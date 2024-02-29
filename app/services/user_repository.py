from datetime import datetime
import time
from typing import Collection, Union
from bson import ObjectId

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.services.generic_repository import GenericRepository
from passlib.context import CryptContext
from passlib.hash import bcrypt
from app.db import users_collection

# Create a password context for hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Error types
InvalidTokenError: str = "Invalid token."
InvalidEmailOrPasswordError: str = "Invalid email or password."
UserNotFound: str = "User not found."


class UserRepository(GenericRepository):
    def __init__(self, collection: Collection) -> None:
        super().__init__(collection)
        self.SECRET_KEY: str = "3c5fe5b9e0b960e488af1ba66ec4"
        self.ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600

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

    def __varify_password(self, plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)

    def __create_access_token(self, data: dict) -> str:
        data["exp"] = self.ACCESS_TOKEN_EXPIRE_SECONDS + int(time.time())
        token = jwt.encode(data, key=self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def authenticate_user(self, email: str, password: str) -> dict:
        user = self.get_user_by_email(email=email)

        # Varify the password and return the user
        if not self.__varify_password(password, hashed_password=user.get("password")):
            raise ValueError(InvalidEmailOrPasswordError)

        return user

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload = jwt.decode(
                token=token, key=self.SECRET_KEY, algorithms=self.ALGORITHM)
            email = payload.get("sub")

            if email is None:
                raise ValueError(InvalidTokenError)

            user = self.get_user_by_email(email=email)
            user.pop("password")  # remove password from response

            return user

        except JWTError as e:
            raise ValueError(InvalidTokenError)

    def get_user_by_email(self, email: str) -> dict:
        user = users_collection.find_one({"email": email})

        if user is None:
            raise ValueError(InvalidEmailOrPasswordError)

        user["id"] = str(user.pop("_id"))
        return user

    def get_user_by_id(self, id: str) -> dict:
        user = users_collection.find_one({"_id": ObjectId(id)})

        if user is None:
            raise ValueError(UserNotFound)

        user["id"] = str(user.pop("_id"))
        return user

    def login(self, item: dict) -> Union[str, None]:
        user = self.authenticate_user(item.get("email"), item.get("password"))

        access_token = self.__create_access_token(
            data={"sub": user.get("email")})
        return access_token
