import re
from typing import Any

import requests

from ti4_mapgen.models.hex import cardinal_from_vector, vector_from_index
from ti4_mapgen.models.system import System, Planet
from ti4_mapgen.models.tile import HomeSystemTile, HyperlaneTile, Stack, SystemTile


def load(url: str) -> Any:
    "Load JSON data from URL."
    response = requests.get(url)
    return response.json()


def dump(stack: Stack, file: str) -> None:
    """Dump stack data to JSON file"""
    stack.to_json_file(file, indent=2)


def parse(tiles: dict[str, dict]) -> Stack:
    """Route tile data to correct parse function."""
    stack = Stack()

    for num, tile in tiles.items():
        match num:
            case num if re.match(r"[0-9]+[A-Z]", num):
                hyperlane_tile = parse_to_hyperlane_tile(num, tile)
                stack.hyperlane_tiles.append(hyperlane_tile)
            case num if 1 <= int(num) <= 17:
                home_system_tile = parse_to_home_system_tile(num, tile)
                stack.home_system_tiles.append(home_system_tile)
            case num if int(num) == 18:
                special_tile = parse_to_system_tile(num, tile)
                stack.special_tiles.append(special_tile)
            case num if 19 <= int(num) <= 50:
                system_tile = parse_to_system_tile(num, tile)
                stack.system_tiles.append(system_tile)
            case num if int(num) == 51:
                special_tile = parse_to_system_tile(num, tile)
                stack.special_tiles.append(special_tile)
            case num if 52 <= int(num) <= 58:
                home_system_tile = parse_to_home_system_tile(num, tile)
                stack.home_system_tiles.append(home_system_tile)
            case num if 59 <= int(num) <= 80:
                system_tile = parse_to_system_tile(num, tile)
                stack.system_tiles.append(system_tile)
            case num if 81 <= int(num) <= 82:
                special_tile = parse_to_system_tile(num, tile)
                stack.special_tiles.append(special_tile)

    return stack


def parse_to_hyperlane_tile(num, tile: dict[str, Any]) -> HyperlaneTile:
    number = int(num[:-1])
    letter = num[-1:]
    hyperlanes = tile["hyperlanes"]
    for index, hyperlane in enumerate(hyperlanes):
        hyperlane = [cardinal_from_vector(vector_from_index(number)) for number in hyperlane]
        hyperlanes[index] = hyperlane
    return HyperlaneTile(number=number, letter=letter, hyperlanes=hyperlanes)


def parse_to_system_tile(num, tile: dict[str, Any]) -> SystemTile:
    number = int(num)
    back = tile["type"]
    release = "base" if number < 52 else "pok"
    wormhole = tile.get("wormhole")
    anomaly = tile.get("anomaly")

    match number:
        case number if number == 61:
            tile["planets"][0]["name"] = "Ang"
        case number if number == 81:
            anomaly = "supernova"
        case number if number == 82:
            wormhole = "gamma"

    planets = parse_to_planet(tile["planets"])

    system = System(
        anomaly=anomaly,
        wormhole=wormhole,
        planets=planets,
    )

    return SystemTile(number=number, back=back, release=release, system=system)


def parse_to_home_system_tile(num, tile: dict[str, Any]) -> HomeSystemTile:
    number = int(num)
    back = tile["type"]
    release = "base" if number < 52 else "pok"
    faction = tile["race"]
    wormhole = tile.get("wormhole")
    anomaly = tile.get("anomaly")

    match number:
        case number if number == 56:
            anomaly = "nebula"

    planets = parse_to_planet(tile["planets"])

    system = System(
        anomaly=anomaly,
        wormhole=wormhole,
        planets=planets,
    )

    return HomeSystemTile(number=number, back=back, release=release, faction=faction, system=system)


def parse_to_planet(planets: list[dict[str, Any]]) -> tuple[Planet]:
    planet_list = []
    for planet in planets:
        name = planet["name"]
        resources = planet["resources"]
        influence = planet["influence"]
        trait = planet.get("trait")
        tech = planet["specialty"]
        legendary = planet["legendary"]
        planet = Planet(
            name=name,
            resources=resources,
            influence=influence,
            trait=trait,
            tech=tech,
            legendary=legendary,
        )
        planet_list.append(planet)
    return tuple(planet_list)


if __name__ == "__main__":
    data = load("https://raw.githubusercontent.com/KeeganW/ti4/master/src/data/tileData.json")
    tiles: dict[str, dict] = data["all"]
    stack = parse(tiles)
    dump(stack, "ti4_mapgen/static/data/tile_data.json")
