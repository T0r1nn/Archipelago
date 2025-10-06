import string

from .items import generate_items, get_default_item_map, item_table, OmegaStrikersItem
from .locations import OmegaStrikersLocation, generate_locations, get_default_location_map
from .rules import set_rules
from BaseClasses import Item, ItemClassification, Tutorial, MultiWorld, Region
from .options import OSOptions
from worlds.AutoWorld import World, WebWorld
from typing import List, TextIO
from .regions import create_regions
from Options import OptionGroup
from . import options

class OmegaStrikersWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Omega Strikers integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["T0r1nn"]
    )]

class OmegaStrikersWorld(World):
    """
    Placeholder description
    """
    game = f"Omega Strikers"
    options_dataclass = OSOptions
    options: OSOptions
    topology_present = False

    item_name_to_id = get_default_item_map()
    location_name_to_id = get_default_location_map()

    item_name_groups = {}

    location_name_groups = {}

    data_version = 7
    required_client_version = (0, 6, 2)
    web = OmegaStrikersWeb()
    initial_striker: string = "Juliette"
    scrap_map = {}
    required_credit_count: int = 0
    imported_data = {}
    moons = []
    generated_items = []
    slot_item_data = None
    characters = []
    spoiler_text = ""
    required_lp_count = 5

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.generated_items, self.slot_item_data = generate_items()

    def generate_early(self) -> None:
        generate_locations(self)

    def create_items(self) -> None:
        # Generate item pool
        itempool: List = []

        for item in self.generated_items:
            name = item.create_item()
            if not (self.options.split_roles.value ^ ("(" in name)) and not name == self.initial_striker:
                if "Brawler" in name and name in self.options.brawlers.value or \
                   "Midfield" in name and name in self.options.midfielders.value or \
                   "Goalie" in name and name in self.options.goalies.value or \
                    not "(" in name:
                    self.characters.append(name)
                    itempool.append(name)

        total_locations = len(generate_locations(self))

        # Fill remaining items with randomly generated junk
        while len(itempool) < total_locations:
            itempool.append(self.get_filler_item_name())

        # Convert itempool into real items
        itempool = list(map(lambda item_name: self.create_item(item_name), itempool))
        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        set_rules(self)

    def get_filler_item_name(self) -> str:
        filler = self.multiworld.random.choices(["LP"], [100],
                                                k=1)[0]
        return filler

    def create_regions(self) -> None:
        create_regions(self.options, self)
        create_events(self.multiworld, self.player)

    def fill_slot_data(self):
        slot_data = {
            
        }

        for option in dir(self.options):
            if hasattr(getattr(self.options, option), "slot"):
                if getattr(self.options, option).slot:
                    slot_data[getattr(self.options, option).slot_name] = getattr(self.options, option).value

        return slot_data

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        classification = self.slot_item_data.classification_table.get(name)
        item = OmegaStrikersItem(name, classification, item_id, self.player)
        return item


def create_events(world: MultiWorld, player: int) -> None:
    world_region = world.get_region("Game", player)
    victory_region = world.get_region("Victory", player)
    victory_event = OmegaStrikersLocation(player, "Victory", None, victory_region)
    victory_event.place_locked_item(OmegaStrikersItem("Victory", ItemClassification.progression, None, player))
    world_region.locations.append(victory_event)


def create_region(world: MultiWorld, player: int, name: str, loc=None) -> Region:
    if loc is None:
        loc = {}
    ret = Region(name, player, world)
    for location_name, location_id in loc.items():
        ret.locations.append(OmegaStrikersLocation(player, location_name, location_id, ret))
    return ret
