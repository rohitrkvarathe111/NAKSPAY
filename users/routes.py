from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Depends, Security, Body
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload, joinedload
from database import get_db
from users.models import User, UserProfile
from users.schemas import CreateUserProfile, OnboardUserResponse, UserLogin, RefreshTokenRequest, UserProfileUpdate
from help_fun.auth_helpers import verify_password, create_access_token, create_refresh_token, verify_token, get_current_user, blacklist_token, is_token_blacklisted, hash_password, generate_password
from help_fun.models import UserTypeEnum
from help_fun.redis_helper import RedisClient
from help_fun.email_funtion import get_welcome_email_html, send_password_reset_email_html
from orgist.models import Orgist
from users.crud import create_user, update_user_profile
import asyncio
import random
from fastapi.security import OAuth2PasswordBearer





router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
redis_client = RedisClient()


@router.post(
    "/hii",
    summary="Greet the user",
    description="This API endpoint returns a simple greeting message to confirm the server is responding.",
    response_description="A JSON message containing a greeting."
)
def read_root():
    return {"detail": "Hello this is user"}


@router.post("/user_verify", status_code=status.HTTP_201_CREATED)
async def verify_user_via_otp(
        email_id: Optional[EmailStr] = None,
        mobile_no: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
    ):

    if not (email_id or mobile_no):
        raise HTTPException(status_code=400, detail="email_id or mobile_no is required")

    try:
        if email_id:
            result = await db.execute(select(User).where(User.email == email_id))
            user = result.scalar_one_or_none()
            if user:
                raise HTTPException(status_code=400, detail="Email already exists in User")
        otp = str(random.randint(100000, 999999))
        if email_id:
            if redis_client.set_otp(f"otp:{email_id}", otp, 300):
                if get_welcome_email_html(email_id, otp):
                    return {"detail": "OTP sent to email and stored successfully", "otp": otp}
                else:
                    raise HTTPException(status_code=500, detail="Failed to send OTP via email")
            else:
                raise HTTPException(status_code=500, detail="Failed to store OTP in Redis for email")
        if mobile_no:
            if redis_client.set_otp(f"otp:{mobile_no}", otp, 300):
                # if get_welcome_sms(mobile_no, otp):              # TODO: create after implementing SMS service
                return {"detail": "OTP sent to mobile and stored successfully", "otp": otp}
            else:
                raise HTTPException(status_code=500, detail="Failed to store OTP in Redis for mobile")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")



@router.post("/onboard-user", response_model=OnboardUserResponse, status_code=status.HTTP_201_CREATED)
async def add_user(org_user: CreateUserProfile,
            email_otp: str = Body(..., embed=True),
            db: AsyncSession = Depends(get_db)):

    email = org_user.email
    stored_otp = redis_client.get_otp(email)
    print(f"[DEBUG] stored_otp: {stored_otp} (type: {type(stored_otp)}), received: {email_otp} (type: {type(email_otp)})")
    if stored_otp != email_otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
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



@router.post("/login", status_code=status.HTTP_201_CREATED, summary="User Login")
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



@router.post("/refresh", status_code=status.HTTP_201_CREATED, summary="Generate a new access token using a refresh token")
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


@router.get("/ping", summary="Ping to check token validity")
async def ping(current_user: dict = Depends(get_current_user)):
    return {
        "status": "ok",
        "detail": "Token is valid",
        # "user": current_user
    }



@router.get("/me", summary="Just for fun")
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


@router.post("/logout", summary="Logout user")
async def logout(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")
    
    if is_token_blacklisted(token):
        raise HTTPException(status_code=400, detail="Token is already blacklisted")
    
    blacklist_token(token)
    return {"detail": "Successfully logged out"}




@router.post("/reset_password", summary="Reset Password Via OTP on Email", status_code=status.HTTP_200_OK)
async def change_password(
    email_id: str,
    db: AsyncSession = Depends(get_db),
):
    if not email_id:
        raise HTTPException(status_code=400, detail="Email is required")

    try:
        result = await db.execute(select(User).where(User.email == email_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_password = generate_password(email_id)
        user.password_hash = hash_password(new_password)

        db.add(user)
        await db.commit()
        if send_password_reset_email_html(email_id, new_password):
            return {"detail": "Password reset email sent successfully", "password": new_password}
        else:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Failed to send password reset email, Please connect with admin")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    

@router.get("/get_user", summary="Edit current user info")
async def get_user_profile(
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)
    ):
    if not current_user or not current_user.get("user_id"):
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    
    user_id = current_user["user_id"]
    
    try:
        result_user = await db.execute(
            select(UserProfile)
            .options(joinedload(UserProfile.user)) 
            .where(UserProfile.user_id == user_id)
        )
        users = result_user.scalar_one_or_none()

        if not users or not users.user:
            raise HTTPException(status_code=404, detail="User or profile not found")

        return {
            "user_id": users.id,
            "first_name": users.user.first_name,
            "last_name": users.user.last_name,
            "user_type": users.user.user_type,
            "identity_type": users.identity_type,
            "address": users.address,
            "identity_no": users.identity_no,
            "city": users.city,
            "identity_img": users.identity_img,
            "state": users.state,
            "country": users.country,
            "dob": users.dob,
            "pincode": users.pincode,
            "website": users.website,
            "gender": users.gender,
            "profile_img": users.profile_img,
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error. Please try again later.")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error.")

    
    
@router.put("/update_user", summary="Edit current user info")
async def update_user(
        user_update: UserProfileUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)
    ):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    user_id = current_user["user_id"]
    if not user_id:
        raise HTTPException(status_code=401, detail="User does not exist")
    
    user_profile = await update_user_profile(db, user_update, user_id)
    return {
        "detail": "User profile updated successfully"
        }
    





