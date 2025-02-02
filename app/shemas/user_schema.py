from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    

class UserCreate(UserBase):
    password: str
    

class UserUpdate(UserBase):
    pass
    

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    