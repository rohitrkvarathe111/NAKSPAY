from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, select
from database import get_db
from users.models import UserTypeEnum, User
from users.schemas import CreateUserProfile, OnboardUserResponse, UserLogin, RefreshTokenRequest
from help_fun.auth_helpers import verify_password, create_access_token, create_refresh_token, verify_token, get_current_user, blacklist_token, is_token_blacklisted
from orgist.models import Orgist
from users.crud import create_user
import asyncio
from fastapi.security import OAuth2PasswordBearer





router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post(
    "/hii",
    summary="Greet the user",
    description="This API endpoint returns a simple greeting message to confirm the server is responding.",
    response_description="A JSON message containing a greeting."
)
def read_root():
    return {"message": "Hello this is user"}




@router.post("/onboard-user", response_model=OnboardUserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Security(oauth2_scheme)])
async def add_user(org_user: CreateUserProfile, db: AsyncSession = Depends(get_db), token: str = Security(oauth2_scheme)):

    payload = get_current_user(token)
    if payload["user_type"] != UserTypeEnum.SUPER_ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not allowed to create an User. Only Super Admins have permission to perform this action.")

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
    
    user_data = {
        "user_id": db_user.id,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "user_type": db_user.user_type,
        "user_level": db_user.user_level,
        "timezone": db_user.timezone,
    }
    if db_user.orgist_id and db_user.user_type in [UserTypeEnum.ORGIST_ADMIN, UserTypeEnum.ORGIST_USER]:
        result = await db.execute(
            select(Orgist).where(Orgist.id == db_user.orgist_id)
        )
        orgist = result.scalar_one_or_none()
        if orgist:
            user_data["orgist_id"] = orgist.id
            user_data["orgist_name"] = orgist.org_name
    
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token({"user_id": db_user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_info": user_data,
    }



@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest,  db: AsyncSession = Depends(get_db)):

    payload = verify_token(request.refresh_token, is_refresh=True)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    
    user_data = {
        "user_id": db_user.id,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "user_type": db_user.user_type,
        "user_level": db_user.user_level,
        "timezone": db_user.timezone,
    }
    if db_user.orgist_id and db_user.user_type in [UserTypeEnum.ORGIST_ADMIN, UserTypeEnum.ORGIST_USER]:
        result = await db.execute(
            select(Orgist).where(Orgist.id == db_user.orgist_id)
        )
        orgist = result.scalar_one_or_none()
        if orgist:
            user_data["orgist_id"] = orgist.id
            user_data["orgist_name"] = orgist.org_name
    
    new_access_token = create_access_token(user_data)

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }



@router.get("/me")
async def get_user_info(token: str = Security(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    return {
        "user_id": payload.get("user_id"),
        "first_name": payload.get("first_name"),
        "last_name": payload.get("last_name"),
        "user_type": payload.get("user_type"),
        "user_level": payload.get("user_level"),
        "timezone": payload.get("timezone")
    }


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    if is_token_blacklisted(token):
        raise HTTPException(status_code=400, detail="Token is already blacklisted")
    
    blacklist_token(token)
    return {"msg": "Successfully logged out"}