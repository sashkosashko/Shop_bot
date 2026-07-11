import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

SqlAlchemyBase = orm.declarative_base()

__factory = None

async def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite+aiosqlite:///{db_file.strip()}?check_same_thread=False'
    
    engine = create_async_engine(conn_str, echo=False)
    
    __factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    from . import __all_models

    async with engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)


def create_session() -> AsyncSession:
    global __factory
    if not __factory:
        raise Exception("База данных не инициализирована. Вызовите global_init снаружи.")
    return __factory()
