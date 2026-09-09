import math
from typing import Dict, TYPE_CHECKING
from BaseClasses import Location
from .data import characters, in_rotation_trainings

if TYPE_CHECKING:
    from . import OmegaStrikersWorld


class OmegaStrikersLocation(Location):
    game: str = f"Omega Strikers"


os_locations_start_id = 1
max_id = os_locations_start_id
categories = [
    "Get X Goals",
    "Strike X Times",
    "Primary X Times",
    "Secondary X Times",
    "Special X Times",
    "Win X Games",
    "Win X Sets"
]

def get_default_location_map() -> Dict[str, int]:
    location_result = {}

    for i in range(len(characters)):
        for j in range(len(categories)):
            location_result.update(check_location(f"{characters[i]} - {categories[j]}"))

    for value in in_rotation_trainings.values():
        location_result.update(check_location(f"Awakening - {value}"))

    return location_result

def check_location_amount(world: "OmegaStrikersWorld") -> int:
    count = len(in_rotation_trainings.keys()) * world.options.awakening_checks.value
    if world.options.awakening_checks.value == 1:
        count -= 4 * (1-world.options.goalie_gear.value)
        count -= 5 * (1-world.options.forward_gear.value)
    for char in world.striker_pool:
        for cat in categories:
            count+=1
    return count

def check_location(location_name: "str"):
    global max_id
    global locations

    if location_name not in locations.keys():
        location_id = max_id
        max_id += 1
        locations.update({location_name: location_id})
        return {location_name: location_id}
    return {location_name: locations[location_name]}
    
locations : Dict[str, int] = {}