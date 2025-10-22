from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, OptionSet, Toggle, Range
from .data import characters


class Goal(Choice):
    """
    Win All: Win once on every striker

    McGuffin: Receive a set amount of LP
    """
    display_name = "Game Mode"
    option_win_all = 0
    option_mcguffin = 1
    default = 0

class LPRequired(Range):
    """
    The % of total LP that must be collected to reach goal when the mcguffin game mode is selected.
    """
    display_name = "LP Required"
    range_start = 1
    range_end = 100
    default = 80

class Whitelist(OptionSet):
    """
    All strikers that can be chosen from to be checks in the multiworld. If empty, counts as all. If less than the desired number of strikers, additional strikers will be chosen at random.
    """
    display_name = "Whitelist"
    default = {}
    valid_keys = [char for char in characters]

class Blacklist(OptionSet):
    """
    All strikers that can't be chosen from to be checks in the multiworld. Can cause generation to fail if there are more strikers requested than non-blacklisted strikers.
    """
    display_name = "Blacklist"
    default = {}
    valid_keys = [char for char in characters]

class Brawlers(OptionSet):
    """
    All strikers that you can reasonably play as brawler.
    """
    display_name = "Brawlers"
    default = {"Juliette",
    "Dubu",
    "Luna",
    "Asher",
    "X",
    "Zen",
    "Drek'ar",
    "Atlas",
    "Rasmus",
    "Kazan"}
    valid_keys = [char for char in characters]

class Midfielders(OptionSet):
    """
    All strikers that you can reasonably play as midfield.
    """
    display_name = "Midfielders"
    default = {
    "Estelle",
    "Luna",
    "Juno",
    "Kai",
    "Era",
    "Aimi",
    "Finii",
    "Octavia",
    "Vyce",
    "Rune",
    "Nao"}
    valid_keys = [char for char in characters]

class Goalies(OptionSet):
    """
    All strikers that you can reasonably play as goalie
    """
    display_name = "Goalies"
    default = {"Estelle",
    "Dubu",
    "Luna",
    "Juno",
    "Asher",
    "Kai",
    "Era",
    "Aimi",
    "Finii",
    "Vyce",
    "Mako",
    "Rune",
    "Drek'ar",
    "Atlas",
    "Nao",
    "Rasmus",
    "Kazan"}
    valid_keys = [char for char in characters]

class SplitRoles(Toggle):
    """
    Count strikers who can play multiple roles as multiple strikers
    Example: Juno becomes Midfield Juno and Goalie Juno
    """
    display_name = "Split Roles"
    default = False

@dataclass
class OSOptions(PerGameCommonOptions):
    game_mode: Goal
    lp_required: LPRequired
    whitelist: Whitelist
    blacklist: Blacklist
    brawlers: Brawlers
    midfielders: Midfielders
    goalies: Goalies
    split_roles: SplitRoles