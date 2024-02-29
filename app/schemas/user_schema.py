from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime


class UserSignUpRequestModel(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr = Field(max_length=25)
    password: str = Field(min_length=8)


class UserSignupResponseModel(BaseModel):
    id: str


class UserLoginRequestModel(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponseModel(BaseModel):
    token: str


class UserDetailsUpdateRequestModel(BaseModel):
    pass


class UserDetailsResponseModel(BaseModel):
    pass
