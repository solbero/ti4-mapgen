from typing import Any

import dataclass_wizard
import requests

from ti4_mapgen import schema


def load(url: str) -> Any:
    "Load JSON data from URL."
    response = requests.get(url)
    return response.json()


def parse(response: dict[str, dict]) -> dataclass_wizard.Container[schema.Faction]:
    factions = dataclass_wizard.Container[schema.Faction]()

    for name in response["races"]:
        faction = {}
        faction["release"] = schema.Release.BASE
        faction["name"] = schema.Name(name)
        factions.append(schema.Faction(**faction))

    for name in response["pokRaces"]:
        faction = {}
        faction["release"] = schema.Release.POK
        faction["name"] = schema.Name(name)
        factions.append(schema.Faction(**faction))

    faction = {}
    faction["release"] = schema.Release.CODEX_3
    faction["name"] = "The Council Keleres"
    factions.append(schema.Faction(**faction))

    return factions


if __name__ == "__main__":
    url = "https://github.com/KeeganW/ti4/raw/master/src/data/raceData.json"
    data = load(url)
    factions = parse(data)
    factions.to_json_file("ti4_mapgen/data/faction_data.json", indent=2)
