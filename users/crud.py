from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from help_fun.auth_helpers import generate_username
from users.models import User, UserProfile
from users.schemas import UserCreate


async def create_user(db: AsyncSession, user: UserCreate):
    org_uc = await generate_username(user.user_type, user.first_name)

    user_data = user.dict()
    user_data["user_uc"] = org_uc
    new_user = User(**user_data)

    try:

        db.add(new_user)
        await db.flush()

        created_by = {
            "created_by": 2,
            "updated_by": 2
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


