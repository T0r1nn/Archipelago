from BaseClasses import MultiWorld, Region, Location
from .locations import locations, check_valid, categories
from .options import OSOptions
from .data import in_rotation_trainings, training_categories
from typing import TYPE_CHECKING, List
from rule_builder.rules import *

if TYPE_CHECKING:
    from . import OmegaStrikersWorld


def create_regions(options: OSOptions, world: "OmegaStrikersWorld"):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    menu: Region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)
    game: Region = Region("Game", player, multiworld)
    multiworld.regions.append(game)
    victory: Region = Region("Victory", player, multiworld)
    multiworld.regions.append(victory)
    awakenings: Region = Region("Awakenings", player, multiworld)
    multiworld.regions.append(awakenings)

    char_regions: List[Region] = []

    game.connect(awakenings)

    if options.awakening_checks.value:
        for value in in_rotation_trainings.values():
            if (options.goalie_gear.value == 1 or value not in training_categories["Goalie"]) and (options.forward_gear.value == 1 or value not in training_categories["Forward"]):
                add_location(player, f"Awakening - {value}", awakenings)

    if options.game_mode.value == 1:
        world.set_rule(game.connect(victory), Has("LP", world.required_lp_count))
    else:
        world.set_rule(game.connect(victory), HasAllCounts({striker: 1 for striker in world.striker_pool}))

    menu.connect(game, rule=lambda state: True)

    for character in world.striker_pool:
        char_regions.append(Region(character, player, multiworld))
        multiworld.regions.append(char_regions[-1])
        world.set_rule(game.connect(char_regions[-1]), Has(character))
        for cat in categories:
            if(check_valid(character, cat, world)):
                add_location(player, f"{character} - {cat}", multiworld.get_region(character, world.player))
    


def add_location(player: int, location: str, region: Region):
    region.locations.append(Location(player, location, locations[location], region))
