from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_user_service
from app.helpers.login_request_form import LoginRequestForm
from app.schemas.user_schema import *
from app.services.user_repository import UserRepository

user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.post("/auth/signup", status_code=status.HTTP_200_OK, response_model=UserSignupResponseModel)
def create_user(user: UserSignUpRequestModel, service: UserRepository = Depends(get_user_service)):
    created_user = service.create(user)
    if created_user is None:
        raise HTTPException(
            status_code=400, detail="Could not create user.")
    if created_user is False:
        raise HTTPException(
            status_code=400, detail="Email already exists!")
    return UserSignupResponseModel(id=created_user)


@user_router.post("/auth/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponseModel)
def login_user(form_data: LoginRequestForm = Depends(), service: UserRepository = Depends(get_user_service)):
    user = {
        "email": form_data.email,
        "password": form_data.password
    }
    try:
        access_token = service.login(user)
        if access_token is None:
            raise HTTPException(
                status_code=401, detail="Email or Password did not match. Login failed!")
        return UserLoginResponseModel(token=access_token)
    except ValueError as e:
        raise HTTPException(
            status_code=401, detail=f"{e}")
