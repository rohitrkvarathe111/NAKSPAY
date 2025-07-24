from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from users.schemas import UserCreate
from orgist.models import OrgTypeEnum, OrgCateEnum, OrgIDTypeEnum


class OrgCreate(BaseModel):
    org_name: str
    org_sort_name: str
    org_type: OrgTypeEnum
    org_cate: OrgCateEnum
    org_email: EmailStr
    org_mobile: str
    identity_type: OrgIDTypeEnum
    identity_code: str
    org_high_level: Optional[int] = None


class OrgCreateResponse(BaseModel):
    detail: str
    is_verified: bool
    org_name: str


class CompanySetup(BaseModel):
    org: OrgCreate
    user: UserCreate

