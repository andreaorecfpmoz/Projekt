from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.redis_utils import init_redis
from app.routers.items import router as items_router
from app.routers.work_orders import router as work_orders_router

app = FastAPI()

origins = [
    "http://localhost:5000",       
    "http://79.76.111.88:5000",    
    "http://127.0.0.1:5000"       
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],    
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(work_orders_router, prefix="/work_orders", tags=["Work Orders"])


@app.on_event("startup")
async def startup_event():
    await init_db()
    await init_redis()


@app.get("/")
def root():
    return {"message": "Welcome to the Maintenance Log API"}
