from typing import TYPE_CHECKING
from BaseClasses import MultiWorld, Region, Location, CollectionState
from .locations import names

if TYPE_CHECKING:
    from . import ThePlanetCrafterWorld


def generate_regions(world: "ThePlanetCrafterWorld"):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    menu: Region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)
    victory: Region = Region("Victory", player, multiworld)
    multiworld.regions.append(victory)

    for name in names:
        add_location(player, name, menu, world)

    menu.connect(victory, rule=lambda state:True)

    multiworld.completion_condition[player] = lambda state: victory_condition(state, player)


def victory_condition(state: CollectionState, player: int):
    return state.can_reach_region("Victory", player)


def add_location(player: int, location: str, region: Region, world: "ThePlanetCrafterWorld"):
    region.locations.append(Location(player, location, world.location_name_to_id[location]))
    region.locations[-1].parent_region = region