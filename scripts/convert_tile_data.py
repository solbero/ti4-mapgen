from typing import Any, Optional

import dataclass_wizard
import requests

from ti4_mapgen import hex, schema


def load(url: str) -> Any:
    "Load JSON data from URL."
    response = requests.get(url)
    return response.json()


def parse(response: dict[str, dict]) -> dataclass_wizard.Container[schema.TileBase]:
    """Parse JSON tile data to tile dataclasses."""
    # List like dataclass container to hold the tiles.
    tiles = dataclass_wizard.Container[schema.TileBase]()

    for ordinal, data in response.items():
        # Separate tile numbers from tile letters, e.g. '81A'.
        try:
            number = int(ordinal)
            letter: Optional[schema.Letter] = None
        except ValueError:
            number = int(ordinal[:-1])
            letter: Optional[schema.Letter] = schema.Letter(ordinal[-1:])

        # Parse the home system tiles.
        if 1 <= number <= 17 or 52 <= number <= 58:
            tile = to_tile(schema.Type.HOME, number, letter, data)
        elif number == 18:
            tile = to_tile(schema.Type.CENTER, number, letter, data)
        # Parse the system tiles.
        elif 19 <= number <= 50 or 59 <= number <= 80:
            tile = to_tile(schema.Type.SYSTEM, number, letter, data)
        # Parse the hyperlane tiles.
        elif 83 <= number <= 91:
            tile = to_tile(schema.Type.HYPERLANE, number, letter, data)
        # Parse the tiles which are outside the board.
        elif number == 51 or number == 81 or number == 82:
            tile = to_tile(schema.Type.EXTERIOR, number, letter, data)
        else:
            raise ValueError(f"tile number must be between 1 and 91, number is {number}")

        tiles.append(tile)

    return tiles


def to_tile(tag: schema.Type, number: int, letter: Optional[schema.Letter], data: dict[str, Any]) -> schema.TileBase:
    """Parse tile data to internal dataclass schema."""
    tile = {}
    tile["tag"] = tag
    tile["front"] = to_front(number, letter, data)
    tile["back"] = to_back(number, data)

    return schema.TileBase(**tile)


def to_front(number: int, letter: Optional[schema.Letter], data: dict[str, Any]) -> schema.Front:
    """Parse tile front to internal dataclass schema."""
    front = {}
    front["number"] = number
    front["letter"] = letter
    front["release"] = schema.Release.BASE if number < 52 else schema.Release.POK
    if (name := data.get("race")) in (n.value for n in schema.Name):
        front["faction"] = schema.Name(name)
    front["system"] = to_system(number, data)
    front["hyperlanes"] = to_hyperlanes(data)

    # Assign faction to Muuat supernova tile.
    if number == 81:
        front["faction"] = schema.Name.MUAAT
    # Assign faction to Creuss home system.
    elif number == 51:
        front["faction"] = schema.Name.CREUSS

    return schema.Front(**front)


def to_back(number: int, data: dict[str, Any]) -> schema.Back | None:
    """Parse tile back to internal dataclass schema."""
    # If the tile is Mecatol Rex or a hyperlane tile return 'None' since the tile does not have a back.
    if number == 18 or 83 <= number <= 91:
        return None

    back = {}
    if (color := data.get("type")) in (c.value for c in schema.Color):
        back["color"] = schema.Color(color)

    return schema.Back(**back)


def to_system(number: int, data: dict[str, Any]) -> schema.System | None:
    """Parse system to internal dataclass schema."""
    # If the tile is a hyperlane tile return 'None' since the tile does not have a system.
    if 83 <= number <= 91:
        return None

    system = {}
    if (wormhole := data.get("anomaly")) in (a.value for a in schema.Anomaly):
        system["anomaly"] = schema.Anomaly(wormhole)
    if (wormhole := data.get("wormhole")) in (w.value for w in schema.Wormhole):
        system["wormhole"] = schema.Wormhole(wormhole)
    system["resources"] = sum(planet.get("resources", 0) for planet in data["planets"])
    system["influence"] = sum(planet.get("influence", 0) for planet in data["planets"])
    system["planets"] = len(data["planets"])
    system["traits"] = [schema.Trait(trait) for planet in data["planets"] if (trait := planet.get("trait"))]
    system["techs"] = [schema.Tech(tech) for planet in data["planets"] if (tech := planet.get("specialty"))]
    system["legendary"] = True if any(planet["legendary"] for planet in data["planets"]) else False

    # Set the Wormhole Nexus wormhole to 'gamma'.
    if number == 82:
        system["wormhole"] = schema.Wormhole.GAMMA
    # Set the Empyrian home system anomaly to 'nebula'.
    elif number == 56:
        system["anomaly"] = schema.Anomaly.NEBULA
    # Set the Muuat supernova tile to 'supernova'.
    elif number == 81:
        system["anomaly"] = schema.Anomaly.SUPERNOVA

    return schema.System(**system)


def to_hyperlanes(data: dict[str, Any]) -> list[list[hex.Cube]]:
    """Parse hyperlanes to internal dataclass schema."""
    data_hyperlanes = data.get("hyperlanes", list())
    index_to_vector = {index: vector for index, vector in enumerate(hex.ring(hex.Cube(0, 0, 0), 1))}
    hyperlanes = []
    for data_hyperlane in data_hyperlanes:
        hyperlane = [index_to_vector[index] for index in data_hyperlane]
        hyperlanes.append(hyperlane)

    return hyperlanes


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/KeeganW/ti4/master/src/data/tileData.json"
    response = load(url)
    tiles = parse(response["all"])
    tiles.sort(key=lambda tile: (tile.front.number, tile.front.letter))
    tiles.to_json_file("ti4_mapgen/data/tile_data.json", indent=2)
