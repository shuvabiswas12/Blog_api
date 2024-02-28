from typing import Annotated, Optional, Union
from pydantic import EmailStr
from fastapi import Form


class LoginRequestForm:
    def __init__(
        self,
        email: Annotated[
            EmailStr,
            Form(),
        ],
        password: Annotated[
            str,
            Form(),
        ],
        grant_type: Annotated[
            Union[str, None],
            Form(pattern="password"),
        ] = None,
    ):
        self.email = email
        self.password = password
        self.grant_type = grant_type
