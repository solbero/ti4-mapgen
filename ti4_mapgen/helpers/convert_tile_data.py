from typing import Any, Optional

import requests
from dataclass_wizard import Container, fromlist

from ti4_mapgen.models.hex import cardinal_from_vector, vector_from_index
from ti4_mapgen.models.tile import Tile, Planet


def load(url: str) -> Any:
    "Load JSON data from URL."
    response = requests.get(url)
    return response.json()


def parse(tiles: dict[str, dict]) -> Container[Tile]:
    """Parse JSON tile data to tile dataclasses."""
    stack = Container[Tile]()

    for number, tile in tiles.items():
        # Separate tile numbers from tile letters
        try:
            letter = None
            number = int(number)
        except ValueError:
            letter = number[-1:]
            number = int(number[:-1])

        # Parse the home system tiles
        if 1 <= number <= 17 or 52 <= number <= 58:
            tile = to_tile("home-system-tile", number, letter, tile)
            stack.append(tile)
        # Parse the system tiles
        elif 18 <= number <= 50 or 59 <= number <= 80:
            tile = to_tile("system-tile", number, letter, tile)
            stack.append(tile)
        # Parse the hyperlane tiles
        elif 83 <= number <= 91:
            tile = to_tile("hyperlane-tile", number, letter, tile)
            stack.append(tile)
        # Parse the Ghost and Muat faction tiles
        elif number == 51 or number == 81 or number == 82:
            tile = to_tile("exterior-tile", number, letter, tile)
            stack.append(tile)

    return stack


def to_tile(type: str, number: int, letter: Optional[str], data: dict[str, Any]) -> Tile:

    number = number
    letter = letter
    release = "base" if number < 52 else "pok"
    faction = data.get("race")

    if number == 18 or 83 <= number <= 91:
        back = None
    else:
        back = data.get("type")

    if number == 82:
        wormhole = "gamma"
    else:
        wormhole = data.get("wormhole")

    if number == 56:
        anomaly = "nebula"
    elif number == 81:
        anomaly = "supernova"
    else:
        anomaly = data.get("anomaly")

    if planets := data.get("planets", list()):
        if number == 61:
            planets[0]["name"] = "Ang"
        planets = to_planet(planets)

    if hyperlanes := data.get("hyperlanes", list()):
        for index, hyperlane in enumerate(hyperlanes):
            hyperlane = [cardinal_from_vector(vector_from_index(number)) for number in hyperlane]
            hyperlanes[index] = hyperlane

    return Tile(
        number=number,
        letter=letter,
        back=back,
        faction=faction,
        release=release,
        anomaly=anomaly,
        wormhole=wormhole,
        planets=planets,
        hyperlanes=hyperlanes,
        type=type,
    )


def to_planet(planets: list[dict[str, Any]]) -> list[Planet]:
    list = []
    for planet in planets:
        name = planet["name"]
        resources = planet["resources"]
        influence = planet["influence"]
        trait = planet.get("trait")
        tech = planet.get("specialty")
        legendary = planet["legendary"]
        list.append(
            Planet(name=name, resources=resources, influence=influence, trait=trait, tech=tech, legendary=legendary)
        )
    return list


if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/KeeganW/ti4/master/src/data/tileData.json"
    data = load(url)
    tiles: dict[str, dict] = data["all"]
    stack = parse(tiles)
    stack.to_json_file("ti4_mapgen/static/data/tile_data.json", indent=2)
