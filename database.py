
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/nakspay" 
# DATABASE_URL = (
#     "postgresql+asyncpg://nakspay:IkEvKrMmYjx9JoxOTKKciLUoJTKRtuGV"
#     "@dpg-d21lfd63jp1c7380pes0-a.oregon-postgres.render.com:5432/nakspay"
# )


engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session