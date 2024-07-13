from typing import TYPE_CHECKING
from BaseClasses import MultiWorld, Region

if TYPE_CHECKING:
    from . import ThePlanetCrafterWorld


def generate_regions(world: "ThePlanetCrafterWorld"):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    menu: Region = Region("Menu", player, multiworld)

