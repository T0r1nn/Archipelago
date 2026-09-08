import math
import string

from BaseClasses import MultiWorld, CollectionState, ItemClassification, LocationProgressType
from .options import OSOptions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import OmegaStrikersWorld

def set_rules(os_world: 'OmegaStrikersWorld') -> None:
    player = os_world.player
    multiworld = os_world.multiworld
    
    """
    TODO: add logic so that awakenings are only in logic when a character that can use them is unlocked
    """

    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
