from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name : str
    password : str
    role : str = "admin"
    email: EmailStr
    # department : str = "YZM"
    


class RegisterResponse(BaseModel):
    email: EmailStr
    name : str
    # department : str
    access_token: str
    refresh_token: str
    access_token: str
    refresh_token: str