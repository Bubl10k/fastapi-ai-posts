from datetime import datetime
from pydantic import BaseModel


class TimeStampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime
