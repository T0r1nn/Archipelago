from Options import PerGameCommonOptions, Choice, dataclass


class Goal(Choice):
    """
    Select the terraformation stage needed to beat the game
    """
    display_name = "Terraformation Goal"
    option_blue_sky = 0
    option_moss = 1
    option_rain = 2
    option_liquid_water = 3
    option_terraformed = 4
    default = 4


@dataclass
class TPCOptions(PerGameCommonOptions):
    terraform_goal: Goal
