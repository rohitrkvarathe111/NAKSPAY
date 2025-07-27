from fastapi import APIRouter, Depends, HTTPException, status, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, select
from database import get_db
from orgist.schemas import OrgCreate, OrgCreateResponse, CompanySetup
from orgist.crud import create_orgist_user
from orgist.models import Orgist, OrgTypeEnum, OrgCateEnum, OrgIDTypeEnum
from users.models import UserTypeEnum, User
from users.routes import oauth2_scheme
from help_fun.auth_helpers import get_current_user
import asyncio





router = APIRouter()





@router.get("/options")
def get_options():

    org_types = [{"code": item.name, "name": item.value} for item in OrgTypeEnum]
    org_categories = [{"code": item.name, "name": item.value} for item in OrgCateEnum]
    org_indentity = [{"code": item.name, "name": item.value} for item in OrgIDTypeEnum]
    user_type = [{"code": item.name, "name": item.value} for item in UserTypeEnum]

    return {
        "org_types": org_types,
        "org_categories": org_categories,
        "org_indentity": org_indentity,
        "user_type": user_type
    }





@router.post("/onboard-org", response_model=OrgCreateResponse, status_code=status.HTTP_201_CREATED)
async def add_orgist(org_user: CompanySetup, db: AsyncSession = Depends(get_db), token: str = Security(oauth2_scheme)):

    payload = get_current_user(token)
    if payload["user_type"] != UserTypeEnum.SUPER_ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not allowed to create an Orgist. Only Super Admins have permission to perform this action.")

    email = org_user.org.org_email

    org_query = select(Orgist).where(Orgist.org_email == email)
    user_query = select(User).where(User.email == email)

    org_result, user_result = await asyncio.gather(
        db.execute(org_query),
        db.execute(user_query)
    )

    if org_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists in Orgist")
    if user_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists in User")


    org_data =  await create_orgist_user(db, org_user)
    
    return {
        "detail": "Orgist created successfully",
        "is_verified": org_data.is_verified,
        "org_name": org_data.org_name,
    }


