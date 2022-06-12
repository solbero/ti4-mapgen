from typing import Any, Optional, cast

import requests
from dataclass_wizard import Container

from ..models.hex import cardinal_from_vector, vector_from_index
from ..models.tile import System, Tile
from ..models.typing import Letter, Tag
from ..models.hex import CardinalDirection, Cube


def load(url: str) -> Any:
    "Load JSON data from URL."
    response = requests.get(url)
    return response.json()


def parse(data: dict[str, dict]) -> Container[Tile]:
    """Parse JSON tile data to tile dataclasses."""
    # List like dataclass container to hold the tiles
    tiles = Container[Tile]()

    for number, data in data.items():
        # Separate tile numbers from tile letters, e.g. '81A'
        try:
            letter: Optional[Letter] = None
            number = int(number)
        except ValueError:
            letter: Optional[Letter] = cast(Letter, number[-1:])
            number = int(number[:-1])

        # Parse the home system tiles
        if 1 <= number <= 17 or 52 <= number <= 58:
            tile = to_tile("home", number, letter, data)
            tiles.append(tile)
        elif number == 18:
            tile = to_tile("mecatol", number, letter, data)
            tiles.append(tile)
        # Parse the system tiles
        elif 19 <= number <= 50 or 59 <= number <= 80:
            tile = to_tile("system", number, letter, data)
            tiles.append(tile)
        # Parse the hyperlane tiles
        elif 83 <= number <= 91:
            tile = to_tile("hyperlane", number, letter, data)
            tiles.append(tile)
        # Parse the tiles which are outside the board
        elif number == 51 or number == 81 or number == 82:
            tile = to_tile("exterior", number, letter, data)
            tiles.append(tile)

    return tiles


def to_tile(tag: Tag, number: int, letter: Optional[Letter], data: dict[str, Any]) -> Tile:
    """Parse tile data to internal dataclass schema."""
    tile = {}
    tile["tag"] = tag
    tile["number"] = number
    tile["letter"] = letter
    tile["release"] = "base" if number < 52 else "pok"
    tile["faction"] = data.get("race")
    tile["back"] = data.get("type")
    tile["system"] = to_system(number, data)
    tile["hyperlanes"] = to_hyperlanes(data)

    # Set Mecatol Rex and hyperlane tile backs to 'None'
    if number == 18 or 83 <= number <= 91:
        tile["back"] = None
    # Assign faction to Muuat supernova tile
    elif number == 81:
        tile["faction"] = "The Embers of Muaat"
    # Assign faction to Creuss home system
    elif number == 51:
        tile["faction"] = "The Ghosts of Creuss"

    return Tile(**tile)


def to_system(number: int, data: dict[str, Any]) -> System | None:
    """Parse system to internal dataclass schema."""
    # If the tile is a hyperlane tile return 'None' since the tile does not have a system
    if 83 <= number <= 91:
        return None

    system = {}
    system["resources"] = sum(planet["resources"] for planet in data["planets"])
    system["influence"] = sum(planet["influence"] for planet in data["planets"])
    system["planets"] = len(data["planets"])
    system["traits"] = [trait for planet in data["planets"] if (trait := planet.get("trait"))]
    system["techs"] = [trait for planet in data["planets"] if (trait := planet.get("specialty"))]
    system["anomaly"] = data.get("anomaly")
    system["wormhole"] = data.get("wormhole")
    system["legendary"] = True if any(planet["legendary"] for planet in data["planets"]) else False

    # Set the Wormhole Nexus wormhole to 'gamma'
    if number == 82:
        system["wormhole"] = "gamma"
    # Set the Empyrian home system anomaly to 'nebula'
    elif number == 56:
        system["anomaly"] = "nebula"
    # Set the Muuat supernova tile to 'supernova'
    elif number == 81:
        system["anomaly"] = "supernova"

    return System(**system)


def to_hyperlanes(data) -> list[list[CardinalDirection | Cube]]:
    """Parse hyperlanes to internal dataclass schema."""
    data_hyperlanes = data.get("hyperlanes", list())

    hyperlanes = []
    for data_hyperlane in data_hyperlanes:
        hyperlane = [cardinal_from_vector(vector_from_index(index)) for index in data_hyperlane]
        hyperlanes.append(hyperlane)

    return hyperlanes


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/KeeganW/ti4/master/src/data/tileData.json"
    data = load(url)
    tiles = parse(data["all"])
    tiles.sort(key=lambda tile: (tile.number, tile.letter))
    tiles.to_json_file("ti4_mapgen/data/tile_data.json", indent=2)
