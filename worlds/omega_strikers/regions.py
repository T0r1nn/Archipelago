from BaseClasses import MultiWorld, Region, Location
from .locations import locations, check_valid, categories
from .options import OSOptions
from .data import in_rotation_trainings, training_categories
from typing import TYPE_CHECKING, List

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
        game.connect(victory, rule= lambda state: state.has("LP", world.player, world.required_lp_count))
    else:
        game.connect(victory, rule= lambda state: state.has_all(world.striker_pool, world.player))

    menu.connect(game, rule=lambda state: True)

    for character in world.striker_pool:
        char_regions.append(Region(character, player, multiworld))
        multiworld.regions.append(char_regions[-1])
        game.connect(char_regions[-1], rule=lambda state, char=character: state.has(char, world.player))
        for cat in categories:
            if(check_valid(character, cat, world)):
                add_location(player, f"{character} - {cat}", multiworld.get_region(character, world.player))
    


def add_location(player: int, location: str, region: Region):
    region.locations.append(Location(player, location, locations[location], region))
