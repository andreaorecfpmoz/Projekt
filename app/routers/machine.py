from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Machine)
async def create_machine(machine: schemas.MachineCreate, db: AsyncSession = Depends(get_db)):
    db_machine = models.Machine(**machine.dict())
    db.add(db_machine)
    await db.commit()
    await db.refresh(db_machine)
    return db_machine


@router.get("/{machine_id}", response_model=schemas.Machine)
async def get_machine(machine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Machine).where(models.Machine.id == machine_id)
    )
    db_machine = result.scalars().first()
    if db_machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return db_machine


@router.get("/", response_model=list[schemas.Machine])
async def get_machines(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Machine))
    machines = result.scalars().all()
    return machines


@router.put("/{machine_id}", response_model=schemas.Machine)
async def update_machine(
    machine_id: int, machine: schemas.MachineUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Machine).where(models.Machine.id == machine_id)
    )
    db_machine = result.scalars().first()
    if db_machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")

    db_machine.name = machine.name
    db_machine.description = machine.description

    await db.commit()
    await db.refresh(db_machine)
    return db_machine


@router.delete("/{machine_id}", response_model=dict)
async def delete_machine(machine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Machine).where(models.Machine.id == machine_id)
    )
    db_machine = result.scalars().first()
    if db_machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")

    await db.delete(db_machine)
    await db.commit()
    return {"message": "Machine deleted"}
