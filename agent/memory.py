import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, select, Integer
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL","sqlite+aiosqlite:///./agentkit.db")
if DATABASE_URL.startswith("postgresql://"): DATABASE_URL = DATABASE_URL.replace("postgresql://","postgresql+asyncpg://",1)
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
class Base(DeclarativeBase): pass
class Mensaje(Base):
    __tablename__ = "mensajes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telefono: Mapped[str] = mapped_column(String(50), index=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
async def inicializar_db():
    async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
async def guardar_mensaje(tel,role,content):
    async with async_session() as s:
        s.add(Mensaje(telefono=tel,role=role,content=content,timestamp=datetime.utcnow())); await s.commit()
async def obtener_historial(tel,limite=20):
    async with async_session() as s:
        r = await s.execute(select(Mensaje).where(Mensaje.telefono==tel).order_by(Mensaje.timestamp.desc()).limit(limite))
        return [{"role":m.role,"content":m.content} for m in reversed(r.scalars().all())]
async def limpiar_historial(tel):
    async with async_session() as s:
        r = await s.execute(select(Mensaje).where(Mensaje.telefono==tel))
        for m in r.scalars().all(): await s.delete(m)
        await s.commit()