from deta import Deta
from asyncstdlib import contextmanager


@contextmanager
async def AsyncBase(engine: Deta, db_name: str):
    async_base = engine.AsyncBase(db_name)
    try:
        yield async_base
    finally:
        await async_base.close()
