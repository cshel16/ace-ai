import pybaseball
import pandas

class Tools:
    # get career stats for a given player
    def get_player_stats(last_name: str, first_name: str):
        return pybaseball.playerid_lookup(last_name, first_name).to_dict(orient='records')