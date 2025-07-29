from fastapi import APIRouter, Depends, HTTPException, status, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload, joinedload
from database import get_db
from orgist.schemas import OrgCreate, OrgCreateResponse, CompanySetup, EditOrgist
from orgist.crud import create_orgist_user, update_orgist_user
from orgist.models import Orgist, OrgistProfile, OrgTypeEnum, OrgCateEnum, OrgIDTypeEnum
from users.models import UserTypeEnum, User, UserProfile
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





@router.post("/onboard_orgist", response_model=OrgCreateResponse, status_code=status.HTTP_201_CREATED)
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



@router.get("/get_orgist", dependencies=[Security(oauth2_scheme)])
async def get_orgist_by_id(
    db: AsyncSession = Depends(get_db),
    token: str = Security(oauth2_scheme)
):
    payload = get_current_user(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    result_user = await db.execute(
        select(User)
        .options(joinedload(User.org))
        .where(User.id == user_id)
    )
    users = result_user.scalar_one_or_none()

    if not users or not users.orgist_id:
        raise HTTPException(status_code=404, detail="Orgist not found")
    
    org_profile_result = await db.execute(
        select(OrgistProfile).where(OrgistProfile.orgist_id == users.orgist_id)
    )
    org_profile = org_profile_result.scalar_one_or_none()

    if not org_profile:
        raise HTTPException(status_code=404, detail="Orgist not found")

    return {
        "orgist_id": users.orgist_id,
        "first_name": users.first_name,
        "last_name": users.last_name,
        "org_name": users.org.org_name,
        "org_add": org_profile.org_add,
        "org_city": org_profile.org_city,
        "org_state": org_profile.org_state,
        "org_pin": org_profile.org_pin,
        "org_country": org_profile.org_country,
        "org_web": org_profile.org_web,
        "org_owner": org_profile.org_owner,
        "org_est_date": org_profile.org_est_date,
        "org_GSTIN": org_profile.org_GSTIN,
        "GSTIN_img": org_profile.GSTIN_img,
        "org_LLPIN": org_profile.org_LLPIN,
        "LLPIN_img": org_profile.LLPIN_img,
        "org_CIN": org_profile.org_CIN,
        "CIN_img": org_profile.CIN_img,
        "org_PAN": org_profile.org_PAN,
        "PAN_img": org_profile.PAN_img,
        "org_logo": org_profile.org_logo,
    }
    

@router.put("/update_orgist", status_code=status.HTTP_200_OK)
async def update_orgist(org_data: EditOrgist, 
                    db: AsyncSession = Depends(get_db), 
                    token: str = Security(oauth2_scheme)):
    payload = get_current_user(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    result_user = await db.execute(
        select(User)
        .options(joinedload(User.org))
        .where(User.id == user_id)
    )
    users = result_user.scalar_one_or_none()

    if not users or not users.orgist_id:
        raise HTTPException(status_code=404, detail="Orgist not found")
    
    org_profile = await update_orgist_user(db, org_data, users.orgist_id)
    return {
        "detail": "Organization profile updated successfully"
    }
    




