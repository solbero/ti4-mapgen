from __future__ import annotations

from enum import Enum, IntEnum
from typing import Optional

from ordered_enum import OrderedEnum, ValueOrderedEnum
from pydantic import BaseModel, Field

from hex import Cube


class Letter(str, Enum):
    A = "A"
    B = "B"


class Color(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    RED = "red"


class Wormhole(str, Enum):
    ALPHA = "alpha"
    BETA = "beta"
    DELTA = "delta"
    GAMMA = "gamma"


class Trait(str, Enum):
    CULTURAL = "cultural"
    HAZARDOUS = "hazardous"
    INDUSTRIAL = "industrial"


class Release(str, Enum):
    BASE = "base"
    POK = "pok"
    CODEX_3 = "codex-3"


class Tech(str, Enum):
    BIOTIC = "biotic"
    CYBERNETIC = "cybernetic"
    PROPULSION = "propulsion"
    WARFARE = "warfare"


class Anomaly(str, Enum):
    ASTEROID_FIELD = "asteroid-field"
    GRAVITY_RIFT = "gravity-rift"
    NEBULA = "nebula"
    SUPERNOVA = "supernova"


class Type(str, Enum):
    CENTER = "center"
    HOME = "home"
    HYPERLANE = "hyperlane"
    SYSTEM = "system"
    EXTERIOR = "exterior"


class Name(str, Enum):
    ARBOREC = "The Arborec"
    ARGENT = "The Argent Flight"
    CREUSS = "The Ghosts of Creuss"
    EMPYREAN = "The Empyrean"
    HACAN = "The Emirates of Hacan"
    JOL_NAR = "The Universities of Jol-Nar"
    KELERES = "The Council Keleres"
    LETNEV = "The Barony of Letnev"
    LIZIX = "The Lizix Mindnet"
    MAHACT = "The Mahact Gene-sorcerers"
    MENTAK = "The Mentak Coalition"
    MUAAT = "The Embers of Muaat"
    NAALU = "The Naalu Collective"
    NAAZ_ROKHA = "The Naaz-Rokha Alliance"
    NEKRO = "The Nekro Virus"
    NOMAD = "The Nomad"
    SAAR = "The Clan of Saar"
    SARDAKK = "Sardakk N'orr"
    SOL = "The Federation of Sol"
    TITANS = "The Titans of Ul"
    VUILRAITH = "The Vuil'raith Cabal"
    WINNU = "The Winnu"
    XXCHA = "The Xxcha Kingdom"
    YIN = "The Yin Brotherhood"
    YSSARIL = "The Yssaril Tribes"


class Players(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


class System(BaseModel):
    """Class representing a system in a tile."""

    resources: int
    influence: int
    planets: int
    traits: list[Trait] = Field(default_factory=list)
    techs: list[Tech] = Field(default_factory=list)
    anomaly: Optional[Anomaly] = None
    wormhole: Optional[Wormhole] = None
    legendary: bool = False


class Tile(BaseModel):
    """Document representing a tile."""

    type: Type
    number: int
    letter: Optional[Letter] = None
    release: Release
    faction: Optional[Name] = None
    back: Optional[Color] = None
    system: Optional[System] = None
    hyperlanes: list[list[Cube]] = Field(default_factory=list)


class TileInDB(Tile):
    key: str


class TileRead(Tile):
    ...


class TileQuery(BaseModel):
    type: Optional[Type] = None
    number: Optional[int] = Field(default=None, ge=1, le=91)
    letter: Optional[Letter] = None
    release: Optional[Release] = None
    back: Optional[Color] = None


class Map(BaseModel):
    """Class representing a map."""

    players: Players
    style: str
    description: str
    source: str
    layout: list


class MapInDB(Map):
    key: str


class Faction(BaseModel):
    """Class representing a faction."""

    name: Name
    release: Release
