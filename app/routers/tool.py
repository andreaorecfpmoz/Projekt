from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Tool)
async def create_tool(tool: schemas.ToolCreate, db: AsyncSession = Depends(get_db)):
    db_tool = models.Tool(**tool.dict())
    db.add(db_tool)
    await db.commit()
    await db.refresh(db_tool)
    return db_tool


@router.get("/{tool_id}", response_model=schemas.Tool)
async def get_tool(tool_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Tool).where(models.Tool.id == tool_id)
    )
    db_tool = result.scalars().first()
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool


@router.get("/", response_model=list[schemas.Tool])
async def get_tools(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Tool))
    tools = result.scalars().all()
    return tools


@router.put("/{tool_id}", response_model=schemas.Tool)
async def update_tool(
    tool_id: int, tool: schemas.ToolUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Tool).where(models.Tool.id == tool_id)
    )
    db_tool = result.scalars().first()
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    db_tool.name = tool.name
    db_tool.description = tool.description

    await db.commit()
    await db.refresh(db_tool)
    return db_tool


@router.delete("/{tool_id}", response_model=dict)
async def delete_tool(tool_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Tool).where(models.Tool.id == tool_id)
    )
    db_tool = result.scalars().first()
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")

    await db.delete(db_tool)
    await db.commit()
    return {"message": "Tool deleted"}
