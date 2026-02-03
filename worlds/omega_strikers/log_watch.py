from typing import TypedDict, List
import os
import re

from .data import training_id_to_name_map

"""
Checks:
- Win X games on each char
- Win X sets on each char
- Score X goals on each char
- Strike X times on each char
- Primary X times on each char
- Secondary X times on each char
- Special X times on each char
- Drafting each awakening for the first time
"""

"""
Notes:
- Abilities:
    - 1 - strike
    - 2 - secondary
    - 3 - primary
    - 4 - special
    - 5 - evade/flip
"""

class GameInfo(TypedDict):
    Character: str
    Team: str
    TeamScore: int
    Score: int
    Sets: int
    Strikes: int
    Primaries: int
    Secondaries: int
    Specials: int
    Awakenings: List[str]
    Won: bool

class LogWatcher:
    def __init__(self, username):
        self.filepath = os.path.expandvars("%localappdata%/OmegaStrikers/Saved/Logs/OmegaStrikers.log")
        self.username = username
        self.most_recent_timestamp = self.getMostRecentTimestamp()
    def checkHasPlayedGame(self) -> bool:
        with open(self.filepath, "r") as file:
            lines = file.readlines()
            file.close()
            lines.reverse()
            for line in lines:
                if "TeamThatWonMatch" in line and self.getTimestampFromLine(line) > self.most_recent_timestamp:
                    return True
            return False
    def getLastGameInfo(self) -> GameInfo:
        character = self.getLastCharPlayed()
        with open(self.filepath, "r") as file:
            last_char = ""
            last_score = ""
            victor = ""
            stats_dict: GameInfo = {"Character": character, "Team": "", "Score": 0, "TeamScore":0, "Sets": 0, "Strikes": 0, "Primaries": 0, "Secondaries": 0, "Specials": 0, "Awakenings": [], "Won": False}
            sets = {"TeamOne": 0, "TeamTwo": 0}
            lines = file.readlines()
            file.close()
            lines.reverse()
            for line in lines:
                if "NewTeam = EAssignedTeam::" in line:
                    stats_dict["Team"] = line.split("NewTeam = EAssignedTeam::")[1].strip()
                    break
            for line in lines:
                if "NewTeam = EAssignedTeam::" in line:
                    break
                if "TeamTwo's NumPointsThisSet changed from" in line and " to 0" not in line:
                    last_score = "TeamTwo"
                    if "TeamTwo" == stats_dict["Team"]:
                        stats_dict["TeamScore"] += 1
                    if last_char != "":
                        if last_char == character and last_score == stats_dict["Team"]:
                            stats_dict["Score"] += 1
                        last_score = ""
                        last_char = ""
                if "TeamTwo's NumPointsThisSet changed from 2 to 3" in line:
                    sets["TeamTwo"] += 1
                if "TeamOne's NumPointsThisSet changed from" in line and " to 0" not in line:
                    last_score = "TeamOne"
                    if "TeamOne" == stats_dict["Team"]:
                        stats_dict["TeamScore"] += 1
                    if last_char != "":
                        if last_char == character and last_score == stats_dict["Team"]:
                            stats_dict["Score"] += 1
                        last_score = ""
                        last_char = ""
                if "StrikeAbility" in line and "on the client!" in line:
                    stats_dict["Strikes"] += 1
                if "PrimaryAbility" in line and "on the client!" in line:
                    stats_dict["Primaries"] += 1
                if "SecondaryAbility" in line and "on the client!" in line:
                    stats_dict["Secondaries"] += 1
                if "SpecialAbility" in line and "on the client!" in line:
                    stats_dict["Specials"] += 1
                if "TeamOne's NumPointsThisSet changed from 2 to 3" in line:
                    sets["TeamOne"] += 1
                if "TeamThatWonMatch" in line:
                    if "TeamOne" in line:
                        victor = "TeamOne"
                    if "TeamTwo" in line:
                        victor = "TeamTwo"
                if "VOD_" in line and "_GoalScore" in line:
                    name = line.split("VOD_")[1].split("_GoalScore")[0]
                    if last_score != "":
                        if name == character and last_score == stats_dict["Team"]:
                            stats_dict["Score"] += 1
                        last_score = ""
                        last_char = ""
                    else:
                        last_char = name
                if f"Player '{self.username}' registering training" in line:
                    training = line.split(f"Player '{self.username}' registering training ")[1]
                    training = training[1:len(training)-2]
                    if training_id_to_name_map[training] not in stats_dict["Awakenings"]:
                        stats_dict["Awakenings"].append(training_id_to_name_map[training])
            stats_dict["Sets"] = sets[stats_dict["Team"]]
            stats_dict["Won"] = stats_dict["Team"] == victor
            return stats_dict
    def getLastCharPlayed(self) -> str:
        with open(self.filepath, "r") as file:
            lines = file.readlines()
            lines.reverse()
            file.close()
            for line in lines:
                if "VOD_" in line and "_CharacterIntro" in line:
                    return line.split("VOD_")[1].split("_CharacterIntro")[0]
            return ""
    def getTimestampFromLine(self, line: str) -> int:
        timestamp = line.split("]")[0][1:]
        [date, time] = timestamp.split("-")
        [year, month, day] = date.split(".")
        [hour, minute, seconds] = time.split(".")
        [seconds, ms] = seconds.split(":")
        return int(ms) + int(seconds)*100 + int(minute)*6000 + int(hour) * 3600000 + int(day) * 86400000 + int(month) * 31 + int(year) * 366
    def getMostRecentTimestamp(self) -> int:
        with open(self.filepath, "r") as file:
            recent_line = file.readlines()[-1]
            file.close()
            return self.getTimestampFromLine(recent_line)
        
    def getAwakeningsFromLog(self):
        with open(self.filepath, "r") as file:
            lines = file.readlines()
            file.close()
            for line in lines:
                if "TD_" in line and "GTD_" not in line:
                    for match in re.findall("TD_[A-Za-z0-9]*", line):
                        if match not in training_id_to_name_map.keys():
                            print(match)