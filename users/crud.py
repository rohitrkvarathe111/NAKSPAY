from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from help_fun.auth_helpers import generate_username, hash_password
from users.models import User, UserProfile
from users.schemas import UserCreate, UserProfileUpdate
from sqlalchemy import select


async def create_user(db: AsyncSession, user: UserCreate, user_id: int):
    org_uc = await generate_username(user.user_type, user.first_name)

    user_data = user.dict()
    user_data["user_uc"] = org_uc
    user_data["password_hash"] = hash_password(user_data["password_hash"])
    new_user = User(**user_data)

    try:

        db.add(new_user)
        await db.flush()

        created_by = {
            "created_by": user_id,
            "updated_by": user_id
        }

        db_user_pro = UserProfile(user_id=new_user.id, **created_by)
        db.add(db_user_pro)

        await db.commit()
        await db.refresh(new_user)
        return new_user

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"IntegrityError: {str(e.orig)}")
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail= f"UnexpectedError: {str(e)}")




async def update_user_profile(db: AsyncSession, user_update: UserProfileUpdate, user_id: int):

    try:
        result = await db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        user_profile = result.scalar_one_or_none()

        if not user_profile:
            raise HTTPException(status_code=404, detail="User Profile not found")
        
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(user_profile, field, value)

        await db.commit()
        await db.refresh(user_profile)
        return user_profile
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))