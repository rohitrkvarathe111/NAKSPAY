from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from orgist.models import Orgist, OrgistProfile
from orgist.schemas import OrgCreate, CompanySetup
from users.models import User, UserProfile
from help_fun.auth_helpers import generate_username, hash_password
    





async def create_orgist_user(db: AsyncSession, org_user: CompanySetup):
    org = org_user.org
    user = org_user.user

    try:
        org_uc = await generate_username(user.user_type, org.org_name)

        # Prepare and insert Orgist
        org_data = org.dict()
        org_data["org_uc"] = org_uc
        db_org = Orgist(**org_data)
        db.add(db_org)
        await db.flush()  # flush to get db_org.id without commit

        org_pro = {
            "orgist_id": db_org.id,
            "org_uc": org_uc,
        }

        created_by = {
            "created_by": 22,
            "updated_by": 22
        }

        db_org_pro = OrgistProfile(**org_pro, **created_by)

        user_data = user.dict()
        user_data.update({
            "user_uc": org_uc,
            "password_hash": hash_password(user.password_hash),
            "email": org.org_email,
            "phone_number": org.org_mobile,
            "user_type": user.user_type.name,
            "user_level": org.org_high_level,
            "orgist_id": db_org.id
        })
        db_user = User(**user_data)
        db.add(db_user)
        await db.flush()
        
        db_user_pro = UserProfile(**{"user_id": db_user.id}, **created_by)

        db.add_all([db_org_pro, db_user_pro])
        await db.commit()
        return db_org 

    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Data integrity error: " + str(e.orig))

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error: " + str(e.__class__.__name__))

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))