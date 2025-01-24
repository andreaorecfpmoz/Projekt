from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=list[schemas.User])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, user: schemas.UserUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.firstname = user.firstname
    db_user.lastname = user.lastname

    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    db_user = result.scalars().first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted"}
