from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date
from help_fun.models import UserTypeEnum, TimezoneEnum, IdentityTypeEnum, GenderEnum, IndiaStateEnum, CountryEnum

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password_hash: str
    user_type: UserTypeEnum
    timezone: TimezoneEnum


class CreateUserProfile(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    user_level: int
    password_hash: str
    user_type: UserTypeEnum
    timezone: TimezoneEnum


class OnboardUserResponse(BaseModel):
    detail: str
    first_name: str
    is_phone_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserProfileUpdate(BaseModel):
    profile_img: str
    identity_type: IdentityTypeEnum
    identity_no: str
    identity_img: str
    dob: date
    gender: GenderEnum
    address: str
    city: str
    state: IndiaStateEnum
    country: CountryEnum
    pincode: int
    website: str
    