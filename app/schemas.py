from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WorkOrderCreate(BaseModel):
    task_description: str
    status: str
    severity: str
    created_at: datetime

class WorkOrder(WorkOrderCreate):
    id: int

    class Config:
        from_attributes = True



class ItemCreate(BaseModel):
    name: str
    description: str | None = None  
    

class ItemOut(ItemCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
 

class UserBase(BaseModel):
    firstname: str
    lastname: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True



class ToolBase(BaseModel):
    name: str
    description: Optional[str] = None

class ToolCreate(ToolBase):
    pass

class ToolUpdate(ToolBase):
    pass

class Tool(ToolBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MachineBase(BaseModel):
    name: str
    description: Optional[str] = None

class MachineCreate(MachineBase):
    pass

class MachineUpdate(MachineBase):
    pass

class Machine(MachineBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True