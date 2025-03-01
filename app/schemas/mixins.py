from datetime import datetime
from pydantic import BaseModel


class TimeStampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime


class UserMixin(BaseModel):
    from app.schemas.user_schema import UserOut
    user: UserOut
