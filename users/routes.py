from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from users import schemas, crud


router = APIRouter()

@router.post("/hii")
def read_root():
    return {"message": "Hello this is user"}