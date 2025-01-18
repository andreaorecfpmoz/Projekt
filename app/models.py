from sqlalchemy import Column, Integer, String, Enum as SqlEnum, DateTime
from datetime import datetime
from app.database import Base

class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)
    task_description = Column(String(255), index=True)
    status = Column(
        SqlEnum("Pending", "Completed", name="status"),
        default="Pending"
    )
    severity = Column(
        SqlEnum("Low", "Medium", "High", name="severity"),
        default="Low"
    )
    created_at = Column(DateTime, default=datetime.utcnow)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
