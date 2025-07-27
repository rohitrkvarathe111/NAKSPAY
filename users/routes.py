from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, select
from database import get_db
from orgist.schemas import OrgCreate, OrgCreateResponse, CompanySetup
from orgist.crud import create_orgist_user
from orgist.models import Orgist, OrgTypeEnum, OrgCateEnum, OrgIDTypeEnum
from users.models import UserTypeEnum, User
from users.schemas import CreateUserProfile, OnboardUserResponse, UserLogin
from help_fun.auth_helpers import verify_password
from users.crud import create_user
import asyncio



router = APIRouter()

@router.post("/hii")
def read_root():
    return {"message": "Hello this is user"}




@router.post("/onboard-user", response_model=OnboardUserResponse, status_code=status.HTTP_201_CREATED)
async def add_user(org_user: CreateUserProfile, db: AsyncSession = Depends(get_db)):
    email = org_user.email

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        raise HTTPException(status_code=400, detail="Email already exists in User")

    db_user = await create_user(db, org_user)

    return {
        "detail": "User created successfully",
        "first_name": db_user.first_name,
        "is_email_verified": db_user.is_email_verified,
        "is_phone_verified": db_user.is_phone_verified,
        "created_at": db_user.created_at
    }


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def user_login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    email = user.email
    password = user.password

    result = await db.execute(select(User).where(User.email == email))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    if not verify_password(password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    return {"message": "Login successful", "user_id": db_user.id}




