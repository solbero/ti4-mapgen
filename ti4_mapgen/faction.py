from dataclasses import dataclass

from bidict import bidict

from dataclass_wizard import JSONWizard, JSONFileWizard
from ti4_mapgen.typing import Release
from ti4_mapgen.typing import Faction as Name

TILE_NUMBER_TO_FACTION_NAME: bidict[int, Name] = bidict(
    {
        1: "The Federation of Sol",
        2: "The Mentak Coalition",
        3: "The Yin Brotherhood",
        4: "The Embers of Muaat",
        5: "The Arborec",
        6: "The Lizix Mindnet",
        7: "The Winnu",
        8: "The Nekro Virus",
        9: "The Naalu Collective",
        10: "The Barony of Letnev",
        11: "The Clan of Saar",
        12: "The Universities of Jol-Nar",
        13: "Sardakk N'orr",
        14: "The Xxcha Kingdom",
        15: "The Yssaril Tribes",
        16: "The Emirates of Hacan",
        17: "The Ghosts of Creuss",
        52: "The Mahact Gene-sorcerers",
        53: "The Nomad",
        54: "The Vuil'raith Cabal",
        55: "The Titans of Ul",
        56: "The Empyrean",
        57: "The Naaz-Rokha Alliance",
        58: "The Argent Flight",
    }
)


@dataclass()
class Faction(JSONWizard, JSONFileWizard):

    name: Name
    release: Release
