from BaseClasses import MultiWorld, Region, Location
from .locations import locations, check_valid, categories
from .options import OSOptions
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

    char_regions: List[Region] = []

    if options.game_mode.value == 1:
        game.connect(victory,
                                 rule=lambda state: (state.has("LP", player,
                                                               count=world.required_lp_count)))
    else:
        game.connect(victory, rule=lambda state: (state.has_all(world.characters, player)))

    menu.connect(game, rule=lambda state: True)

    for character in world.characters:
        char_regions.append(Region(character, player, multiworld))
        game.connect(char_regions[-1], rule = lambda state: (state.has(character, player)))
        for cat in categories:
            c = character
            print(c, cat)
            if "(" in c:
                c = character[0:character.index("(")]
            if(check_valid(character, c, "B" if "Brawler" in character else "M" if "Midfield" in character else "G" if "Goalie" in character else None)):
                add_location(player, f"{character} - Get X {cat}", char_regions)
                print(f"Adding location {character} - Get X {cat}")

def add_location(player: int, location: str, region: Region):
    region.locations.append(Location(player, location, locations[location]))
    region.locations[-1].parent_region = region
