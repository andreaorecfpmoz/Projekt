from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+aiomysql://user:password@db/yourdatabase"

# Asinhroni engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Asinhroni sessionmaker
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Inicijalizacija baze
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Funkcija za dobivanje sesije baze podataka
async def get_db():
    async with SessionLocal() as session:
        yield session
