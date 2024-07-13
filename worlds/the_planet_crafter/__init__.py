from typing import Mapping, Any, List

from BaseClasses import MultiWorld, Item
from worlds.AutoWorld import World, WebWorld
from .locations import generate_location_map
from .items import item_map, items, classification_table, ThePlanetCrafterItem
from .options import TPCOptions


class ThePlanetCrafterWeb(WebWorld):
    pass


class ThePlanetCrafterWorld(World):
    """
    Placeholder Description
    """
    game = "The Planet Crafter"
    options_dataclass = TPCOptions
    options: TPCOptions
    topology_present = False

    item_name_to_id = item_map
    location_name_to_id = generate_location_map()

    data_version = 7
    required_client_version = (0, 5, 0)
    web = ThePlanetCrafterWeb()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def generate_early(self) -> None:
        pass

    def create_items(self) -> None:
        itempool: List = []
        for item in items:
            itempool.append(item.name)

        itempool = list(map(lambda item_name : self.create_item(item_name), itempool))

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        pass

    def get_filler_item_name(self) -> str:
        pass

    def create_regions(self) -> None:
        pass

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {}

    def create_item(self, name: str) -> "Item":
        item_id = self.item_name_to_id[name]
        classification = classification_table[name]
        item = ThePlanetCrafterItem(name, classification, item_id, self.player)
        return item

    def create_filler(self) -> "Item":
        pass
