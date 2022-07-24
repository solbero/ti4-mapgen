from typing import Optional

from deta import Deta
from fastapi import APIRouter, Form, Query

from . import config
from . import database as db
from . import schemas

SETTINGS = config.get_settings()
PROJECT_KEY = SETTINGS.deta_project_key

engine = Deta(PROJECT_KEY)
router = APIRouter()


@router.get("/maps/", response_model=list[schemas.Map])
async def read_maps() -> list[schemas.MapInDB]:
    async with db.AsyncBase(engine, "map") as base:
        results = await base.fetch()
    db_maps = [schemas.MapInDB(**result) for result in results.items]
    return db_maps


@router.get("/factions/")
async def read_factions():
    ...


@router.get("/tiles/", response_model=list[schemas.TileRead])
async def read_tiles(query: Optional[schemas.TileQuery] = None, test: Optional[int] = None):
    async with db.AsyncBase(engine, "tile") as base:
        results = await base.fetch()
    db_tiles = [schemas.TileInDB(**result) for result in results.items]
    return db_tiles


@router.get("/generate/")
async def generate():
    ...
