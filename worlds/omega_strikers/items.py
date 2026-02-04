import math

from BaseClasses import Item, ItemClassification
from typing import Dict, TYPE_CHECKING, Tuple, List
from .locations import generate_locations
from .data import characters

if TYPE_CHECKING:
    from . import OmegaStrikersWorld


class OmegaStrikersItem(Item):
    game: str = f"Omega Strikers"


class SlotItemData:
    def __init__(self):
        self.classification_table: Dict[str, ItemClassification] = {}


class OSItem:
    id = 0

    def __init__(self, slot_item_data: SlotItemData, name, classification = ItemClassification.progression):
        self.name = name
        if self.name in item_table.keys():
            self.item_id = item_table[self.name]
        else:
            self.item_id = OSItem.id
            OSItem.id += 1
        item_table.update({self.name: self.item_id})

        slot_item_data.classification_table[name] = classification

    def create_item(self):
        return self.name


item_table: Dict[str, int] = {}


def get_default_item_map(world: "OmegaStrikersWorld|None"):
    generate_items(world)
    return item_table


def generate_items(world: "OmegaStrikersWorld|None") -> Tuple[List[OSItem], SlotItemData]:
    slot_item_data = SlotItemData()

    items = [OSItem(slot_item_data, char) for char in characters]
    OSItem(slot_item_data, "LP", ItemClassification.progression)
    OSItem(slot_item_data, "Nothing", ItemClassification.filler)

    return items, slot_item_data
