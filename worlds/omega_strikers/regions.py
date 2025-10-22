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

    print(world.required_lp_count)

    if options.game_mode.value == 1:
        game.connect(victory,
                                 rule=lambda state: (state.has("LP", player,
                                                               count=world.required_lp_count)))
    else:
        game.connect(victory, rule=lambda state: (state.has_all(world.characters, player)))

    menu.connect(game, rule=lambda state: True)

    print(world.characters)

    for character in world.characters:
        char_regions.append(Region(character, player, multiworld))
        multiworld.regions.append(char_regions[-1])
        game.connect(char_regions[-1], rule = lambda state: (state.has(character, player)))
        for cat in categories:
            c = character
            if "(" in c:
                c = character[0:character.index("(")]
            if(check_valid(c, cat, world, "B" if "Brawler" in character else "M" if "Midfield" in character else "G" if "Goalie" in character else "")):
                add_location(player, f"{character} - Get X {cat}", multiworld.get_region(character, world.player))

def add_location(player: int, location: str, region: Region):
    region.locations.append(Location(player, location, locations[location], region))
    region.locations[-1].access_rule = lambda state: state.has(region.name, player)