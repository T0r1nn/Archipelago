from BaseClasses import MultiWorld, Region, Location
from .locations import locations, categories
from .options import OSOptions
from .data import in_rotation_trainings, training_categories
from typing import TYPE_CHECKING, List
from rule_builder.rules import Has, HasAll

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
        game.connect(victory, rule=Has("LP", count=world.required_lp_count))
    else:
        game.connect(victory, rule=HasAll(*world.striker_pool))

    menu.connect(game)

    for character in world.striker_pool:
        char_regions.append(Region(character, player, multiworld))
        multiworld.regions.append(char_regions[-1])
        game.connect(char_regions[-1], rule=Has(character))
        for cat in categories:
            add_location(player, f"{character} - {cat}", multiworld.get_region(character, world.player))
    


def add_location(player: int, location: str, region: Region):
    region.locations.append(Location(player, location, locations[location], region))
