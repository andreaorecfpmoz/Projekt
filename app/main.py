from fastapi import FastAPI
from app.database import init_db
from app.routers import items
from app.redis_utils import init_redis

app = FastAPI()

# Učitaj rute
app.include_router(items.router, prefix="/items", tags=["Items"])

# Inicijalizacija baze i Redis-a
@app.on_event("startup")
async def startup_event():
    await init_db()
    await init_redis()

@app.get("/")
def root():
    return {"message": "Welcome to the Maintenance Log API"}
