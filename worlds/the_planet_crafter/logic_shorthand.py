from BaseClasses import CollectionState
from typing import Dict, Callable
from enum import Enum, EnumType

RESOURCE_NAMES: Enum = Enum(
    "IRON"
)

RESOURCE_ACCESS: Dict[EnumType, Callable[[CollectionState], bool]] = {
    RESOURCE_NAMES: lambda state: True,
    "MAGNESIUM": lambda state: True,
    "SILICON": lambda state: True,
    "TITANIUM": lambda state: True,
    "": lambda state: True
}
