#!/usr/bin/env python

from __future__ import annotations

from sanic import Request, Sanic, HTTPResponse, text

from dataclass_wizard import Container
from models.board import Map

app = Sanic(__name__)


@app.before_server_start
def setup(app):
    app.ctx.maps = Map.from_json_file("./ti4_mapgen/static/data/map_data.json")


@app.post("/maps")
async def maps(request: Request) -> HTTPResponse:
    maps: list[Map] = app.ctx.maps
    return text(Map.list_to_json(maps), content_type="application/json")


@app.post("/maps/<players:int>")
async def maps_players(request: Request, players: int):
    maps: list[Map] = app.ctx.maps
    filtered_maps = [map for map in maps if map.players == players]
    return text(Map.list_to_json(filtered_maps), content_type="application/json")


@app.post("/maps/<players:int>/<style:str>")
async def layout_players_name(request: Request, players: int, style: str):
    maps: list[Map] = app.ctx.maps
    filtered_maps = [map for map in maps if map.players == players and map.style == style]
    return text(Map.list_to_json(filtered_maps), content_type="application/json")


@app.post("/races")
async def races(request: Request):
    pass


@app.post("/races/<release:str>")
async def races_release(request: Request, release):
    pass


@app.post("/tiles")
async def tiles(request: Request):
    pass


@app.post("/tiles/<number:int>")
async def tiles_number(request: Request, number):
    pass


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, workers=2, debug=True)
