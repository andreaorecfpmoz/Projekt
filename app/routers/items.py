from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ItemOut)
async def create_item(
    item_data: schemas.ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    db_item = models.Item(**item_data.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.ItemOut])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item))
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=schemas.ItemOut)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.ItemOut)
async def update_item(
    item_id: int,
    item_data: schemas.ItemCreate,
    db: AsyncSession = Depends(get_db)
):
  
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id)
    )
    db_item = result.scalars().first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    
    db_item.name = item_data.name
    db_item.description = item_data.description

    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Item).where(models.Item.id == item_id)
    )
    db_item = result.scalars().first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(db_item)
    await db.commit()
    return {"message": f"Item {item_id} deleted"}
