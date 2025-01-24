from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.redis_utils import init_redis
from app.routers.items import router as items_router
from app.routers.work_orders import router as work_orders_router
from app.routers.user import router as user_router
from app.routers.tool import router as tool_router
from app.routers.machine import router as machine_router
from fastapi.staticfiles import StaticFiles



app = FastAPI()

# CORS konfiguracija
origins = [
     "http://localhost:5000",  # Vaš frontend lokalno
    "http://79.76.111.88:5000",  # Backend na serveru
    "http://localhost:5000",  # Lokalni backend
    "http://127.0.0.1:5000",  # Alternativni localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],    
)

# Statičke datoteke
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rute
app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(work_orders_router, prefix="/work_orders", tags=["Work Orders"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(tool_router, prefix="/tools", tags=["Tools"])
app.include_router(machine_router, prefix="/machines", tags=["Machines"])
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    await init_db()
    await init_redis()

@app.get("/")
def root():
    return {"message": "Welcome to the Maintenance Log API"}
