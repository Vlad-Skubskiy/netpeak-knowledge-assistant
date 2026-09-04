from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from src.db.models import Base, ChatHistory

DATABASE_URL = "sqlite+aiosqlite:///./data/bot_database.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_message(user_id: int, role: str, content: str):
    async with async_session() as session:
        msg = ChatHistory(user_id=user_id, role=role, content=content)
        session.add(msg)
        await session.commit()


async def get_recent_history(user_id: int, limit: int = 6) -> list[dict]:
    async with async_session() as session:
        stmt = (
            select(ChatHistory)
            .where(ChatHistory.user_id == user_id)
            .order_by(ChatHistory.id.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        messages = result.scalars().all()
        
        messages.reverse()
        return [{"role": m.role, "content": m.content} for m in messages]