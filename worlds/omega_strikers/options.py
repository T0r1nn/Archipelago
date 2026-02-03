from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, OptionSet, FreeText, Range
from .data import characters


class Goal(Choice):
    """
    Win All: Win once on every striker

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


class Wins(Range):
    """
    The total number of games you need to win on a character to get a check. This number is cumulative.
    """
    display_name = "Wins"
    range_start = 1
    range_end = 50
    default = 2

class Sets(Range):
    """
    The total number of sets you need to win on a character to get a check. This number is cumulative.
    """
    display_name = "Sets"
    range_start = 1
    range_end = 150
    default = 5

class Scores(Range):
    """
    The total number of goals you need to score on a character to get a check. This number is cumulative.
    """
    display_name = "Scores"
    range_start = 1
    range_end = 650
    default = 6

class Strikes(Range):
    """
    The total number of strikes you need to perform on a character to get a check. This number is cumulative.
    """
    display_name = "Strikes"
    range_start = 1
    range_end = 5000
    default = 200

class Primaries(Range):
    """
    The total number of primaries you need to perform on a character to get a check. This number is cumulative.
    """
    display_name = "Primaries"
    range_start = 1
    range_end = 1000
    default = 75

class Secondaries(Range):
    """
    The total number of secondaries you need to perform on a character to get a check. This number is cumulative.
    """
    display_name = "Secondaries"
    range_start = 1
    range_end = 800
    default = 50

class Specials(Range):
    """
    The total number of specials you need to perform on a character to get a check. This number is cumulative.
    """
    display_name = "Specials"
    range_start = 1
    range_end = 500
    default = 15

class Username(FreeText):
    """
    Your OS username, used for awakening checks
    """
    display_name = "Username"
    default = ""

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

@dataclass
class OSOptions(PerGameCommonOptions):
    game_mode: Goal
    lp_required: LPRequired
    strikers: Strikers
    wins: Wins
    sets: Sets
    scores: Scores
    strikes: Strikes
    primaries: Primaries
    secondaries: Secondaries
    specials: Specials
    username: Username
    whitelist: Whitelist
    blacklist: Blacklist