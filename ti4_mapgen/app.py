from typing import Optional
from deta import Deta
from fastapi import FastAPI, Form, Query

from ti4_mapgen.database import AsyncBase
from ti4_mapgen.schema import (
    Color,
    Faction,
    Map,
    MapInDB,
    TileBase,
    TileInDB,
    TileQuery,
    TileRead,
    Type,
    Letter,
    Release,
)

app = FastAPI()
engine = Deta()


@app.get("/")
async def index() -> dict[str, str]:
    return {
        "info": "This is the index page of the ti4-mapgen API."
        "You probably want to go to 'http://<hostname:port>/docs'.",
    }


@app.get("/maps/", response_model=list[Map])
async def read_maps() -> list[MapInDB]:
    async with AsyncBase(engine, "map") as base:
        results = await base.fetch()
    db_maps = [MapInDB(**result) for result in results.items]
    return db_maps


@app.get("/factions/", response_model=list[Faction])
async def read_factions():
    ...


@app.get("/tiles/", response_model=list[TileRead])
async def read_tiles(query: TileQuery):
    async with AsyncBase(engine, "tile") as base:
        results = await base.fetch(**query.dict())
    db_tiles = [TileInDB(**result) for result in results.items]
    return db_tiles


@app.get("/generate/")
async def generate(
    releases: list[str] = Form(),
    players: int = Form(),
    style: str = Form(),
    factions: list[str] = Form(),
):
    ...
