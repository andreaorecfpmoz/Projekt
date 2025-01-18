from fastapi import FastAPI

app = FastAPI()

from app.routers import items

app.include_router(items.router, prefix="/items", tags=["Items"])
