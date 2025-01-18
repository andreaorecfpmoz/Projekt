from pydantic import BaseModel
from datetime import datetime


class WorkOrderCreate(BaseModel):
    task_description: str
    status: str
    severity: str
    created_at: datetime

class WorkOrder(WorkOrderCreate):
    id: int

    class Config:
        orm_mode = True



class ItemCreate(BaseModel):
    name: str
    description: str | None = None  
    

class ItemOut(ItemCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
