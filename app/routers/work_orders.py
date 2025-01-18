from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas
from app.database import get_db

router = APIRouter()



@router.post("/", response_model=schemas.WorkOrder)
async def create_work_order(
    work_order: schemas.WorkOrderCreate,
    db: AsyncSession = Depends(get_db)
):
    db_work_order = models.WorkOrder(**work_order.dict())
    db.add(db_work_order)
    await db.commit()
    await db.refresh(db_work_order)
    return db_work_order


@router.get("/{work_order_id}", response_model=schemas.WorkOrder)
async def get_work_order(work_order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.WorkOrder).where(models.WorkOrder.id == work_order_id)
    )
    db_work_order = result.scalars().first()
    if db_work_order is None:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return db_work_order


@router.get("/", response_model=list[schemas.WorkOrder])
async def get_work_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.WorkOrder))
    work_orders = result.scalars().all()
    return work_orders


@router.put("/{work_order_id}", response_model=schemas.WorkOrder)
async def update_work_order(
    work_order_id: int,
    work_order: schemas.WorkOrderCreate,
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(
        select(models.WorkOrder).where(models.WorkOrder.id == work_order_id)
    )
    db_work_order = result.scalars().first()
    if db_work_order is None:
        raise HTTPException(status_code=404, detail="Work Order not found")

    db_work_order.task_description = work_order.task_description
    db_work_order.severity = work_order.severity
    db_work_order.status = work_order.status

    await db.commit()
    await db.refresh(db_work_order)
    return db_work_order


@router.delete("/{work_order_id}", response_model=dict)
async def delete_work_order(work_order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.WorkOrder).where(models.WorkOrder.id == work_order_id)
    )
    db_work_order = result.scalars().first()
    if db_work_order is None:
        raise HTTPException(status_code=404, detail="Work Order not found")

    await db.delete(db_work_order)
    await db.commit()
    return {"message": "Work Order deleted"}
