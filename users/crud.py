from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from users.models import User
from users.schemas import UserCreate


async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(**user.dict())
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return new_user
