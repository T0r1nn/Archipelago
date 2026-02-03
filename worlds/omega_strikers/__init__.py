from .items import generate_items, get_default_item_map, item_table, OmegaStrikersItem, SlotItemData
from .locations import OmegaStrikersLocation, generate_locations, get_default_location_map, check_location_amount
from .rules import set_rules
from BaseClasses import Item, ItemClassification, Tutorial, MultiWorld, Region
from .options import OSOptions
from worlds.AutoWorld import World, WebWorld
from typing import Any
from .regions import create_regions
from worlds.LauncherComponents import launch_subprocess, components, Component, Type
from .data import characters

def run_client(*args: Any):
    from .Client import main
    launch_subprocess(main, "Omega Strikers Client")

components.append(Component("Omega Strikers Client",
                            func=run_client,
                            game_name="Omega Strikers",
                            component_type=Type.CLIENT
                ))

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
    options: OSOptions # type: ignore
    topology_present = False

    item_name_to_id = get_default_item_map(None)
    location_name_to_id = get_default_location_map()

    item_name_groups = {}

    location_name_groups = {}

    data_version = 7
    required_client_version = (0, 6, 2)
    web = OmegaStrikersWeb()
    initial_striker: str = ""
    generated_items = []
    slot_item_data : SlotItemData
    spoiler_text = ""
    required_lp_count: int = 5

    def __init__(self, multiworld, player: int):
        super().__init__(multiworld, player)
        self.striker_pool: list[str] = []

    def generate_early(self) -> None:
        if len(self.options.whitelist.value) > self.options.strikers.value:
            self.striker_pool = self.random.sample([item for item in self.options.whitelist.value], k=self.options.strikers.value)
        else:
            for striker in self.options.whitelist.value:
                self.striker_pool.append(striker)
            remaining_slots = self.options.strikers.value - len(self.striker_pool)
            pickable_strikers = []
            for striker in characters:
                if striker not in self.striker_pool and striker not in self.options.blacklist.value:
                    pickable_strikers.append(striker)
            self.striker_pool += self.random.sample(pickable_strikers, k=remaining_slots)
        
        self.required_lp_count = int((check_location_amount(self) - len(self.striker_pool)) * self.options.lp_required.value/100.0)

        self.initial_striker = self.random.choice(self.striker_pool)
        self.generated_items, self.slot_item_data = generate_items(self)

    def create_items(self) -> None:
        # Generate item pool
        itempool: list = []

        for name in self.striker_pool:
            if name != self.initial_striker:
                itempool.append(name)

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Fill remaining items with randomly generated junk
        if self.options.game_mode.value == 1:
            while len(itempool) < total_locations:
                itempool.append(self.get_filler_item_name())

        # Convert itempool into real items
        itempool = list(map(lambda item_name: self.create_item(item_name), itempool))
        self.multiworld.itempool += itempool

        self.multiworld.push_precollected(self.multiworld.create_item(self.initial_striker, self.player))

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
            "Wins":self.options.wins.value,
            "Required LP":self.required_lp_count,
            "Sets":self.options.sets.value,
            "Goals":self.options.scores.value,
            "Strikes":self.options.strikes.value,
            "Primaries":self.options.primaries.value,
            "Secondaries":self.options.secondaries.value,
            "Specials":self.options.specials.value,
            "Username":self.options.username.value,
            "Striker Count":self.options.strikers.value,
            "Goal Mode":self.options.game_mode.value,
            "AwakeningsEnabled":self.options.awakening_checks.value
        }

        return slot_data

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        classification = self.slot_item_data.classification_table.get(name)
        if(classification != None):
            item = OmegaStrikersItem(name, classification, item_id, self.player)
            return item
        else:
            return OmegaStrikersItem(name, ItemClassification.filler, item_id, self.player)


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
