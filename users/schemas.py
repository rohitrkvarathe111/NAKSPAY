from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from users.models import UserTypeEnum, TimezoneEnum

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password_hash: str
    user_type: UserTypeEnum
    timezone: TimezoneEnum


class UserOut(UserCreate):
    id: int
    is_email_verified: bool
    is_phone_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
