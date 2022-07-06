from __future__ import annotations

import dataclasses
import enum
import ordered_enum
from typing import Optional

import dataclass_wizard

from ti4_mapgen import hex


class Letter(ordered_enum.OrderedEnum):
    A = "A"
    B = "B"


class Color(enum.Enum):
    BLUE = "blue"
    GREEN = "green"
    RED = "red"


class Wormhole(enum.Enum):
    ALPHA = "alpha"
    BETA = "beta"
    DELTA = "delta"
    GAMMA = "gamma"


class Trait(enum.Enum):
    CULTURAL = "cultural"
    HAZARDOUS = "hazardous"
    INDUSTRIAL = "industrial"


class Release(enum.Enum):
    BASE = "base"
    POK = "pok"
    CODEX_3 = "codex-3"


class Tech(enum.Enum):
    BIOTIC = "biotic"
    CYBERNETIC = "cybernetic"
    PROPULSION = "propulsion"
    WARFARE = "warfare"


class Anomaly(enum.Enum):
    ASTEROID_FIELD = "asteroid-field"
    GRAVITY_RIFT = "gravity-rift"
    NEBULA = "nebula"
    SUPERNOVA = "supernova"


class Tag(enum.Enum):
    CENTER = "center"
    HOME = "home"
    HYPERLANE = "hyperlane"
    SYSTEM = "system"
    EXTERIOR = "exterior"


class Name(enum.Enum):
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


class Players(ordered_enum.OrderedEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


@dataclasses.dataclass(kw_only=True)
class Tile(dataclass_wizard.JSONWizard, dataclass_wizard.JSONFileWizard):
    """Class representing a tile."""

    class _(dataclass_wizard.JSONWizard.Meta):
        skip_defaults = True

    tag: Tag
    position: Optional[hex.Cube] = None
    front: Optional[Front] = None
    back: Optional[Back] = None
    rotation: Optional[int] = 0


@dataclasses.dataclass(frozen=True, kw_only=True)
class Front:
    """Class representing the front of a tile."""

    number: int
    letter: Optional[Letter] = None
    release: Release
    faction: Optional[Name] = None
    system: Optional[System] = None
    hyperlanes: list[list[hex.Cube]] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(frozen=True)
class Back:
    """Class representing the back of a tile."""

    color: Color


@dataclasses.dataclass(frozen=True)
class System:
    """Class representing a system in a tile."""

    resources: int
    influence: int
    planets: int
    traits: list[Trait] = dataclasses.field(default_factory=list)
    techs: list[Tech] = dataclasses.field(default_factory=list)
    anomaly: Optional[Anomaly] = None
    wormhole: Optional[Wormhole] = None
    legendary: bool = False


@dataclasses.dataclass(frozen=True)
class Map(dataclass_wizard.JSONWizard, dataclass_wizard.JSONFileWizard):
    """Class representing a map."""

    class _(dataclass_wizard.JSONWizard.Meta):
        skip_defaults = True

    players: Players
    style: str
    description: str
    source: str
    layout: list[Tile]


@dataclasses.dataclass(frozen=True)
class Faction(dataclass_wizard.JSONWizard, dataclass_wizard.JSONFileWizard):
    """Class representing a faction."""

    name: Name
    release: Release
