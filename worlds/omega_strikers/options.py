from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, OptionSet, Toggle, Range
from .data import characters


class Goal(Choice):
    """
    Win All: Win once on every striker(Not yet implemented)

    McGuffin: Receive a set amount of LP
    """
    display_name = "Game Mode"
    option_win_all = 0
    option_mcguffin = 1
    default = 1

class LPRequired(Range):
    """
    The % of total LP that must be collected to reach goal when the mcguffin game mode is selected.
    """
    display_name = "LP Required"
    range_start = 1
    range_end = 100
    default = 80

class Strikers(Range):
    """
    The total number of strikers that will be part of the multiworld.
    If the whitelist is bigger than this number, will select randomly from there
    Otherwise, will start with the whitelist, then randomly select some non-blacklisted strikers to fill the remaining roster
    If there are no more non-blacklisted strikers and there are still more slots to be filled, the remaining slots will be populated from the blacklist
    """
    display_name = "Strikers"
    range_start = 1
    range_end = 21
    default = 12

class XGoalsAssists(Range):
    """
    The total number of goals and assists combined you need on a character to get the Get X Goals+Assists check
    """
    display_name = "X Goals+Assists"
    range_start = 1
    range_end = 13
    default = 5

class XKOs(Range):
    """
    The total number of KOs you need on a character to get the Get X KOs check
    """
    display_name = "X KOs"
    range_start = 1
    range_end = 20
    default = 3

class XSaves(Range):
    """
    The total number of saves you need on a character to get the Get X Saves check
    """
    display_name = "X Saves"
    range_start = 1
    range_end = 200
    default = 75

class XRedirects(Range):
    """
    The total number of redirects you need on a character to get the Get X Redirects check
    """
    display_name = "X Redirects"
    range_start = 1
    range_end = 300
    default = 120

class XOrbs(Range):
    """
    The total number of orbs you need on a character to get the Get X Orbs check
    """
    display_name = "X Orbs"
    range_start = 1
    range_end = 45
    default = 25

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

class GoalsAssistsBlacklist(OptionSet):
    """
    All strikers you don't feel comfortable getting the Get X Goals+Assists check for
    """
    display_name = "Goals+Assists Blacklist"
    default = {}
    valid_keys = [char for char in characters]

class SavesBlacklist(OptionSet):
    """
    All strikers you don't feel comfortable getting the Get X Saves check for
    """
    display_name = "Saves Blacklist"
    default = {"Juliette",
    "X",
    "Zen",
    "Octavia"}
    valid_keys = [char for char in characters]



class KOsBlacklist(OptionSet):
    """
    All strikers you don't feel comfortable getting the Get X KOs check for
    """
    display_name = "KOs Blacklist"
    default = {
    "Juno",
    "Kai",
    "Era",
    "Octavia"}
    valid_keys = [char for char in characters]

class RedirectsBlacklist(OptionSet):
    """
    All strikers you don't feel comfortable getting the Get X Redirects check for
    """
    display_name = "Redirects Blacklist"
    default = {}
    valid_keys = [char for char in characters]



class OrbsBlacklist(OptionSet):
    """
    All strikers you don't feel comfortable getting the Get X Orbs check for
    """
    display_name = "Orbs Blacklist"
    default = {}
    valid_keys = [char for char in characters]

@dataclass
class OSOptions(PerGameCommonOptions):
    game_mode: Goal
    lp_required: LPRequired
    strikers: Strikers
    x_goals_assists: XGoalsAssists
    x_redirects: XRedirects
    x_saves: XSaves
    x_kos: XKOs
    x_orbs: XOrbs
    whitelist: Whitelist
    blacklist: Blacklist
    goals_assists_blacklist: GoalsAssistsBlacklist
    saves_blacklist: SavesBlacklist
    kos_blacklist: KOsBlacklist
    redirects_blacklist: RedirectsBlacklist
    orbs_blacklist: OrbsBlacklist