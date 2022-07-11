from typing import Any

import dataclass_wizard
import requests

from ti4_mapgen import hex, schema, util


def load(url: str) -> Any:
    "Load JSON data from URL."
    response = requests.get(url)
    return response.json()


def parse(response: dict[str, dict]) -> dataclass_wizard.Container[schema.Map]:
    """Parse JSON map data to map dataclasses."""
    maps = dataclass_wizard.Container[schema.Map]()

    for players, data in response.items():
        for style, data in data.items():
            map = {}
            map["players"] = schema.Players(int(players))
            map["style"] = style
            map["description"] = data["description"]
            map["source"] = data["source"]
            map["layout"] = to_layout(data)

            maps.append(schema.Map(**map))

    return maps


def to_layout(data) -> list[schema.TileBase]:
    data_homes = data["home_worlds"]
    data_systems = data["primary_tiles"] + data["secondary_tiles"] + data["tertiary_tiles"]
    data_hyperlanes = data["hyperlane_tiles"]

    index_to_position = {index: position for index, position in enumerate(hex.spiral(hex.Cube(0, 0, 0), 4))}

    file = "./ti4_mapgen/data/tile_data.json"
    tiles = util.dataclass_container_from_file(schema.TileBase, file)

    layout = []

    # Add Mecatol Rex (#18) as the center tile
    tile = next(tile for tile in tiles if tile.front.number == 18)
    tile.position = hex.Cube(0, 0, 0)
    layout.append(tile)

    for index in data_homes:
        position = index_to_position[index]
        back = schema.Back(color=schema.Color.GREEN)
        tile = schema.TileBase(position=position, type=schema.Type.HOME, back=back)
        layout.append(tile)

    for index in data_systems:
        position = index_to_position[index]
        back = schema.Back(color=schema.Color.BLUE)
        tile = schema.TileBase(position=position, type=schema.Type.SYSTEM, back=back)
        layout.append(tile)

    for index, ordinal, rotation in data_hyperlanes:
        number = int(ordinal[:-1])
        letter = schema.Letter(ordinal[-1:])
        angle = rotation * 60

        tile = next(tile for tile in tiles if tile.front.number == number and tile.front.letter == letter)
        tile.position = index_to_position[index]

        for hyperlane in tile.front.hyperlanes:
            for index, vector in enumerate(hyperlane):
                hyperlane[index] = hex.rotate(vector, tile.position, angle=angle)

        layout.append(tile)

    return layout


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/KeeganW/ti4/master/src/data/boardData.json"
    data = load(url)
    maps = parse(data["styles"])
    maps.to_json_file("ti4_mapgen/data/map_data.json", indent=2)
