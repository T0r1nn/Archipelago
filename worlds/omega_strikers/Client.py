from CommonClient import CommonContext, ClientCommandProcessor, server_loop, gui_enabled, get_base_parser, ClientStatus
from MultiServer import mark_raw, NetworkItem
import Utils
import asyncio
from typing import TypedDict, Any
from .log_watch import LogWatcher
from .items import get_default_item_map
from .locations import get_default_location_map
import os

if __name__ == "__main__":
    Utils.init_logging("OSClient", exception_logger="Client")


class CharProgress(TypedDict):
    Wins: int
    Sets: int
    Goals: int
    Strikes: int
    Primaries: int
    Secondaries: int
    Specials: int


class OSCommandProcessor(ClientCommandProcessor):
    ctx: "OSContext"
    def _cmd_get_game(self):
        """Prints the most recent game"""
        data = LogWatcher(self.ctx.slot_data["Username"]).getLastGameInfo()
        result = f"Character: {data['Character']}\nTeam: {data['Team']}\nScore: {data['Score']}\nSets: {data['Sets']}\nStrikes: {data['Strikes']}\nPrimaries: {data['Primaries']}\nSecondaries: {data['Secondaries']}\nSpecials: {data['Specials']}\n"
        result += "Awakenings:\n"
        for awakening in data["Awakenings"]:
            result += " - "+awakening+"\n"
        self.output(result)
    def _cmd_set_username(self, username):
        """Changes the set username, useful if you switch accounts or change usernames"""
        self.ctx.slot_data["Username"] = username
        self.ctx.update_username = True
    def _cmd_get_username(self):
        """Prints the currently set username"""
        self.output(self.ctx.slot_data["Username"])
    def _cmd_characters(self):
        """Lists the currently collected characters"""
        received_items = self.ctx.items_received
        result = "Unlocked Characters: \n"
        for item in received_items:
            chr = self.ctx.item_id_map[item.item]
            if chr != "LP" and chr != "Nothing":
                result += f" - {self.ctx.item_id_map[item.item]}\n"
        self.output(result)
    def _cmd_progress(self):
        """Lists progress towards goal"""
        received_items = self.ctx.items_received
        lp_count = 0
        for item in received_items:
            chr = self.ctx.item_id_map[item.item]
            if chr == "LP":
                lp_count += 1
        self.output(f"{lp_count}/{self.ctx.slot_data['Required LP']}")
    def _cmd_send_awake_checks(self):
        """Sends awakening checks"""
        data = LogWatcher(self.ctx.slot_data["Username"]).getLastGameInfo()
        for awakening in data["Awakenings"]:
            self.ctx.awakenings_found.append(f"Awakening - {awakening}")
        self.output("Sent!")


    
class OSContext(CommonContext):
    command_processor = OSCommandProcessor
    game = "Omega Strikers"
    items_handling = 0b111
    location_id_map = get_default_location_map()
    item_id_map = {value: key for key, value in get_default_item_map(None).items()}
    slot_data = {}
    progress_data:dict[str, CharProgress] = {}
    awakenings_found:list[str] = []
    received_characters:list[str] = []
    update_username = False

    def __init__(self, server_address: str | None = None, password: str | None = None) -> None:
        super(OSContext, self).__init__(server_address, password)
        self.syncing = False
        self.send_index = 0
        self.awaiting_bridge = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(OSContext, self).connection_closed()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []
        
    async def shutdown(self):
        await super(OSContext, self).shutdown()
    
    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.set_notify(f"{self.slot}OmegaStrikers-username")
            self.set_notify(f"{self.slot}OmegaStrikers-progress")
            self.set_notify(f"{self.slot}OmegaStrikers-awakenings")
            #Handle Slot Data
            for slot_data_key in list(args['slot_data'].keys()):
                self.slot_data[slot_data_key] = args["slot_data"][slot_data_key]
        if cmd in {"Retrieved"}:
            if f"{self.slot}OmegaStrikers-username" in args["keys"]:
                if args["keys"][f"{self.slot}OmegaStrikers-username"] != None:
                    self.slot_data["Username"] = args["keys"][f"{self.slot}OmegaStrikers-username"]
            if f"{self.slot}OmegaStrikers-progress" in args["keys"]:
                if args["keys"][f"{self.slot}OmegaStrikers-progress"] != None:
                    self.progress_data = args["keys"][f"{self.slot}OmegaStrikers-progress"]
            if f"{self.slot}OmegaStrikers-awakenings" in args["keys"]:
                if args["keys"][f"{self.slot}OmegaStrikers-awakenings"] != None:
                    self.awakenings_found = args["keys"][f"{self.slot}OmegaStrikers-awakenings"]
        if cmd in {"SetReply"}:
            if f"{self.slot}OmegaStrikers-username" == args["key"]:
                self.slot_data["Username"] = args["value"]

async def game_watcher(ctx: OSContext):
    while not "Username" in ctx.slot_data and not ctx.exit_event.is_set():
        await asyncio.sleep(0.1)
    watcher = LogWatcher(ctx.slot_data["Username"])

    stat_to_check_name_map = {
        "Goals": "Get X Goals",
        "Strikes": "Strike X Times",
        "Primaries": "Primary X Times",
        "Secondaries": "Secondary X Times",
        "Specials": "Special X Times",
        "Wins": "Win X Games",
        "Sets": "Win X Sets"
    }
    while not ctx.exit_event.is_set():
        ctx.received_characters = []
        lp_received = 0
        for item in ctx.items_received:
            chr = ctx.item_id_map[item.item]
            if chr != "LP" and chr != "Nothing":
                ctx.received_characters.append(ctx.item_id_map[item.item])
            else:
                lp_received += 1
        if ctx.update_username:
            await ctx.send_msgs([{"cmd":"Set", "key":f"{ctx.slot}OmegaStrikers-username", "default":ctx.slot_data["Username"], "want_replay":True, "operations":[{"operation":"replace", "value":ctx.slot_data["Username"]}]}])
            ctx.update_username = False
        if ctx.slot_data["Username"] != watcher.username:
            old_timestamp = watcher.most_recent_timestamp
            watcher = LogWatcher(ctx.slot_data["Username"])
            watcher.most_recent_timestamp = old_timestamp
        if ctx.syncing == True:
            sync_msg:list[dict[str, Any]] = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        if ctx.slot_data["Goal Mode"] == 1:
            victory = lp_received >= ctx.slot_data["Required LP"]
        else:
            wins = 0
            for char in ctx.progress_data.values():
                if char["Wins"] >= 1:
                    wins += 1
            victory = wins >= ctx.slot_data["Striker Count"]

        print(ctx.awakenings_found)

        if watcher.checkHasPlayedGame():
            data = watcher.getLastGameInfo()
            char = data["Character"]
            if char in ctx.received_characters:
                for awakening in data["Awakenings"]:
                    if awakening not in ctx.awakenings_found:
                        ctx.awakenings_found.append(f"Awakening - {awakening}")
                if char not in ctx.progress_data.keys():
                    ctx.progress_data[char] = {"Wins":0, "Sets": 0, "Goals": 0, "Strikes": 0, "Primaries": 0, "Secondaries": 0, "Specials": 0}
                if data["Won"]:
                    ctx.progress_data[char]["Wins"] += 1
                if ctx.slot_data["Score Mode"] == 0:
                    ctx.progress_data[char]["Goals"] += data["Score"]
                else:
                    ctx.progress_data[char]["Goals"] += data["TeamScore"]
                ctx.progress_data[char]["Primaries"] += data["Primaries"]
                ctx.progress_data[char]["Secondaries"] += data["Secondaries"]
                ctx.progress_data[char]["Sets"] += data["Sets"]
                ctx.progress_data[char]["Specials"] += data["Specials"]
                ctx.progress_data[char]["Strikes"] += data["Strikes"]
                await ctx.send_msgs([{"cmd":"Set", "key":f"{ctx.slot}OmegaStrikers-progress", "default":{}, "want_replay":True, "operations":[{"operation":"replace", "value":ctx.progress_data}]}])        
                await ctx.send_msgs([{"cmd":"Set", "key":f"{ctx.slot}OmegaStrikers-awakenings", "default":[], "want_replay":True, "operations":[{"operation":"replace", "value":ctx.awakenings_found}]}])        
            watcher.most_recent_timestamp = watcher.getMostRecentTimestamp()

        for char in ctx.progress_data.keys():
            check_names = []
            for key in ctx.progress_data[char]:
                if ctx.progress_data[char][key] > ctx.slot_data[key]:
                    check_names.append(f"{char} - {stat_to_check_name_map[key]}")
            
            for check in check_names:
                sending.append(ctx.location_id_map[check])
            
            for awakening in ctx.awakenings_found:
                sending.append(ctx.location_id_map[f"{awakening}"])


        ctx.locations_checked = set(sending)
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)
        



def main():
    async def main(args):
        ctx = OSContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="OSProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Omega Strikers Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()