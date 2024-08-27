from BaseClasses import CollectionState
from typing import Dict, Callable
from enum import Enum


class RESOURCE_NAMES(Enum):
    IRON = 0
    MAGNESIUM = 1
    SILICON = 2
    TITANIUM = 3
    COBALT = 4
    ALUMINUM = 5
    ICE = 6
    IRIDIUM = 7
    URANIUM = 8
    OSMIUM = 9
    SULFUR = 10
    ZEOLITE = 11
    SUPER_ALLOY = 12

#will only account for the first 20(subject to change) of this resource, if more is required then will logically require ore extractors
RESOURCE_ACCESS: Dict[RESOURCE_NAMES, Callable[[CollectionState, int], bool]] = {
    RESOURCE_NAMES.IRON: lambda state, player: True,
    RESOURCE_NAMES.MAGNESIUM: lambda state, player: True,
    RESOURCE_NAMES.SILICON: lambda state, player: True,
    RESOURCE_NAMES.TITANIUM: lambda state, player: True,
    RESOURCE_NAMES.COBALT: lambda state, player: True,
    RESOURCE_NAMES.ALUMINUM: lambda state, player: get_max_travel_distance(state, player) > 3,#placeholder
    RESOURCE_NAMES.ICE: lambda state, player: True,#temp < whenever ice disappears
    RESOURCE_NAMES.IRIDIUM: lambda state, player: get_max_travel_distance(state, player) > 4,#placeholder
    RESOURCE_NAMES.URANIUM: lambda state, player: get_max_travel_distance(state, player) > 10,#placeholder, idk if the uranium cave is ever blocked
    RESOURCE_NAMES.OSMIUM: lambda state, player: state.can_acess_region("Osmium Cave", player),#idk yet if ill split the osmium caves into two regions or not
    RESOURCE_NAMES.SULFUR: lambda state, player: state.can_acess_region("Osmium Cave", player) or state.can_acess_region("Sulfur Fields", player),#idk if sulfur can be found anywhere else
    RESOURCE_NAMES.ZEOLITE: lambda state, player: state.can_acess_region("Zeolite Cave", player),#idk if zeolite can be found elsewhere, its been too long, are there even zeolite caves?
    RESOURCE_NAMES.SUPER_ALLOY: lambda state, player: state.can_acess_region("Super Alloy Caves", player) or \
                                                      (get_has_unlimited_access(RESOURCE_NAMES.IRON, state, player) and
                                                       get_has_limited_access(RESOURCE_NAMES.MAGNESIUM, state, player) and
                                                       get_has_limited_access(RESOURCE_NAMES.SILICON, state, player) and
                                                       get_has_limited_access(RESOURCE_NAMES.TITANIUM, state, player) and
                                                       get_has_limited_access(RESOURCE_NAMES.COBALT, state, player) and
                                                       get_has_limited_access(RESOURCE_NAMES.ALUMINUM, state, player))
}

#will require t1 ore extractor plus whatever else is in this lambda(so region access, resource access, etc) - will logically allow for infinite of this resource
T1_RESOURCE_ACCESS: Dict[RESOURCE_NAMES, Callable[[CollectionState, int], bool]] = {}

#will require t2 ore extractor plus whatever else is in this lambda(so region access, resource access, etc) - will logically allow for infinite of this resource
T2_RESOURCE_ACCESS: Dict[RESOURCE_NAMES, Callable[[CollectionState, int], bool]] = {}

#will require t3 ore extractor plus whatever else is in this lambda(so region access, resource access, etc) - will logically allow for infinite of this resource
T3_RESOURCE_ACCESS: Dict[RESOURCE_NAMES, Callable[[CollectionState, int], bool]] = {}


def get_has_limited_access(resource: RESOURCE_NAMES, state:CollectionState, player:int) -> bool:
    return RESOURCE_ACCESS[resource](state, player)


def get_has_unlimited_access(resource: RESOURCE_NAMES, state:CollectionState, player:int) -> bool:
    if resource in T1_RESOURCE_ACCESS:
        return T1_RESOURCE_ACCESS[resource](state, player) and state.has("OreExtractor1",player)
    elif resource in T2_RESOURCE_ACCESS:
        return T2_RESOURCE_ACCESS[resource](state, player) and state.has("OreExtractor2",player)
    elif resource in T3_RESOURCE_ACCESS:
        return T3_RESOURCE_ACCESS[resource](state, player) and state.has("OreExtractor3",player)
    else:
        return False


#will return a "travel tier", 0 if unupgraded, and then boosts like oxygen tanks, jetpacks, and rebreathers can increase
#this by varying amounts. for example, an oxygen tank might boost it by 1 bc its not a huge boost while a jetpack might boost it by 3 bc of the mobility increase
def get_max_travel_distance(state:CollectionState, player:int) -> int:
    return 0


#will return the current logical temp to determine region acessibility
def get_logical_temp(state:CollectionState, player:int) -> int:
    return 0