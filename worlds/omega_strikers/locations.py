import math
from typing import Dict, TYPE_CHECKING
from BaseClasses import Location
from .data import characters

if TYPE_CHECKING:
    from . import OmegaStrikersWorld


class OmegaStrikersLocation(Location):
    game: str = f"Omega Strikers"


os_locations_start_id = 1869590
max_id = os_locations_start_id
categories = [
    "Goals+Assists",
    "KOs",
    "Saves",
    "Redirects",
    "Orbs",
    "Wins"
]

def get_default_location_map():
    location_result = {}

    for i in range(len(characters)):
        for j in range(len(categories)):
            location_result.update(check_location(f"{characters[i]} - Get X {categories[j]}"))

    for i in range(len(characters)):
        for j in range(len(categories)):
            location_result.update(check_location(f"{characters[i]}(Brawler) - Get X {categories[j]}"))
            location_result.update(check_location(f"{characters[i]}(Midfield) - Get X {categories[j]}"))
            location_result.update(check_location(f"{characters[i]}(Goalie) - Get X {categories[j]}"))

    return location_result


def generate_locations(world: "OmegaStrikersWorld"):
    location_result = {}

    for char in characters:
        for cat in categories:
            if(world.options.split_roles.value):
                if check_valid(char, cat, world, "B"):
                    location_result.update(check_location(f"{char}(Brawler) - Get X {cat}"))
                if check_valid(char, cat, world, "M"):
                    location_result.update(check_location(f"{char}(Midfield) - Get X {cat}"))
                if check_valid(char, cat, world, "G"):
                    location_result.update(check_location(f"{char}(Goalie) - Get X {cat}"))
            else:
                if check_valid(char, cat, world):
                    location_result.update(check_location(f"{char} - Get X {cat}"))
    
    return location_result

def check_location(location_name: "str") -> Dict[str, int]:
    global max_id
    global locations

    if location_name in locations.keys():
        location_id = locations[location_name]
    else:
        location_id = max_id
        max_id += 1
    locations.update({location_name: location_id})
    return {location_name: location_id}

def check_valid(character: str, category: str, world: "OmegaStrikersWorld", role: str = "") -> bool:
    brawler = character in world.options.brawlers.value
    midfield = character in world.options.midfielders.value
    goalie = character in world.options.goalies.value

    if role == "B":
        brawler = 1 * brawler
        midfield = 0
        goalie = 0
    elif role == "M":
        brawler = 0
        midfield = 1 * midfield
        goalie = 0
    elif role == "G":
        brawler = 0
        midfield = 0
        goalie = 1 * goalie

    if brawler + midfield + goalie == 0:
        return False

    category_map = {
        "Goals+Assists":"BMG",
        "KOs":"BM",
        "Saves":"G",
        "Redirects":"BMG",
        "Orbs":"BMG",
        "Wins":"BMG"
    }

    if brawler and "B" in category_map[category]:
        return True
    if midfield and "M" in category_map[category]:
        return True
    if goalie and "G" in category_map[category]:
        return True
    return False
    
locations : Dict[str, int] = {}