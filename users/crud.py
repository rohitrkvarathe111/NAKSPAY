from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from help_fun.auth_helpers import generate_username, hash_password
from users.models import User, UserProfile, Account, UserMapping
from users.schemas import UserCreate, UserProfileUpdate
from sqlalchemy import select, insert, or_
from help_fun.models import MappedStatus


async def create_user(db: AsyncSession, user: UserCreate):
    org_uc = await generate_username(user.user_type, user.first_name)

    user_data = user.dict()
    user_data["user_uc"] = org_uc
    user_data["is_email_verified"] = True
    user_data["password_hash"] = hash_password(user_data["password_hash"])
    new_user = User(**user_data)

    try:
        db.add(new_user)
        await db.flush()

        created_by = {
            "created_by": new_user.id,
            "updated_by": new_user.id
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
    

async def create_account(db: AsyncSession, account: dict):
    try:
        db_info = Account(**account)
        db.add(db_info)
        await db.commit()
        await db.refresh(db_info)
        return db_info
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Account creation failed: {str(e)}")


async def create_mapping_request(
        db: AsyncSession,
        sender_obj: User,
        receiver_obj: User):
    
    try:
        existing = await db.scalar(
            select(UserMapping).where(
                or_(
                    (UserMapping.user_id == sender_obj.id) & (UserMapping.mapped_user_id == receiver_obj.id) & (UserMapping.is_active == True),
                    (UserMapping.user_id == receiver_obj.id) & (UserMapping.mapped_user_id == sender_obj.id) & (UserMapping.is_active == True),
                )
            )
        )

        if existing:
            raise HTTPException(status_code=409, detail="Mapping request already exists")
        
        main_data = {
            "requested_user_id": sender_obj.id,
            "mapped_status": MappedStatus.PENDING.value,
            "created_by": sender_obj.id,
            "updated_by": sender_obj.id,
        }
        t1 = {
            **main_data,
            "orgist_id": sender_obj.orgist_id,
            "user_id": sender_obj.id,
            "mapped_user_id": receiver_obj.id,
            "mapped_orgist_id": receiver_obj.orgist_id,
        }
        t2 = {
            **main_data,
            "orgist_id": receiver_obj.orgist_id,
            "user_id": receiver_obj.id,
            "mapped_user_id": sender_obj.id,
            "mapped_orgist_id": sender_obj.orgist_id,
        }

        await db.execute(insert(UserMapping), [t1, t2])
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating mapping request: {str(e)}")
