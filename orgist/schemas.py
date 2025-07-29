from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from users.schemas import UserCreate
from help_fun.models import OrgTypeEnum, OrgCateEnum, OrgIDTypeEnum
from datetime import date


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


class EditOrgist(BaseModel):
    org_add: str
    org_city: str
    org_state: str
    org_pin: int
    org_country: str
    org_web: str
    org_owner: str
    org_est_date: date
    org_GSTIN: str
    GSTIN_img: str
    org_LLPIN: str
    LLPIN_img: str
    org_CIN: str
    CIN_img: str
    org_PAN: str
    PAN_img: str
    org_logo: str


