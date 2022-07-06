#!/usr/bin/env python

from __future__ import annotations

from typing import cast

import sanic
from sanic.exceptions import SanicException

from ti4_mapgen import board, schema

app = sanic.Sanic(__name__)


@app.get("/maps")
async def maps(request: sanic.Request) -> sanic.HTTPResponse:
    maps = cast(list[schema.Map], schema.Map.from_json_file("ti4_mapgen/data/map_data.json"))
    args = dict(request.args)

    match args:
        case {"players": players, "style": styles}:
            results = [map for map in maps if str(map.players.value) in players and map.style in styles]
        case {"players": players}:
            results = [map for map in maps if str(map.players.value) in players]
        case {"style": styles}:
            results = [map for map in maps if map.style in styles]
        case _ if args:
            raise SanicException(
                message=f"Request contained invalid paramater(s): {', '.join(f'{k!r}' for k in args.keys())}",
                status_code=404,
            )
        case _:
            results = [map for map in maps]

    exclude = ["layout"]
    response = [result.to_dict(exclude=exclude) for result in results]
    return sanic.json(response)


@app.get("/factions")
async def factions(request: sanic.Request):
    factions = cast(list[schema.Faction], schema.Faction.from_json_file("ti4_mapgen/data/faction_data.json"))
    args = dict(request.args)

    match args:
        case {"release": releases}:
            results = [faction for faction in factions if faction.release.value in releases]
        case _ if args:
            raise SanicException(
                message=f"Request contained invalid paramater(s): {', '.join(f'{k!r}' for k in args.keys())}",
                status_code=404,
            )
        case _:
            results = [faction for faction in factions]

    response = [result.to_dict() for result in results]
    return sanic.json(response)


@app.get("/tiles")
async def tiles(request: sanic.Request) -> sanic.HTTPResponse:
    tiles = cast(list[schema.Tile], schema.Tile.from_json_file("ti4_mapgen/data/tile_data.json"))
    args = dict(request.args)

    match args:
        case _ if args:
            raise SanicException(
                message=f"Request contained invalid paramater(s): {', '.join(f'{k!r}' for k in args.keys())}",
                status_code=404,
            )
        case _:
            results = [tile for tile in tiles]

    exclude = ["tag", "position"]
    response = [result.to_dict(exclude=exclude) for result in results]
    return sanic.json(response)


@app.get("/generate")
async def generate(request: sanic.Request) -> sanic.HTTPResponse:
    maps = cast(list[schema.Map], schema.Map.from_json_file("ti4_mapgen/data/map_data.json"))
    tiles = cast(list[schema.Tile], schema.Tile.from_json_file("ti4_mapgen/data/tile_data.json"))
    args = dict(request.args)

    match args:
        case {"release": releases, "players": players, "style": styles, "factions": names}:
            layout = next((map.layout for map in maps if str(map.players.value) in players and map.style in styles))
            stack = [tile for tile in tiles if tile.front.release.value in releases and tile.tag.value == "system"]
            home_systems_tiles = [
                tile
                for tile in tiles
                if tile.front.faction and tile.front.faction.value in names and tile.tag.value == "home"
            ]
        case {"release": releases, "players": players, "style": styles}:
            layout = next((map.layout for map in maps if str(map.players.value) in players and map.style in styles))
            stack = [tile for tile in tiles if tile.front.release.value in releases and tile.tag.value == "system"]
            home_systems_tiles = []
        case _:
            param = ["release", "players", "style"]
            raise SanicException(
                message=f"Request missing paramater(s): {', '.join(f'{k!r}' for k in param if k not in args.keys())}",
                status_code=404,
            )

    response = board.Board(layout=layout, stack=stack, home_system_tiles=home_systems_tiles)
    exclude = ["stack"]
    return sanic.json(response.to_dict(exclude=exclude))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, workers=2, debug=True)
