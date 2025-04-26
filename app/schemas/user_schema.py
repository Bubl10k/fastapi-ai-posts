from pydantic import BaseModel, EmailStr

from app.schemas.mixins import TimeStampMixin


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserOut(UserBase, TimeStampMixin):
    id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLogout(BaseModel):
    email: EmailStr


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserMe(BaseModel):
    id: int
    email: EmailStr
