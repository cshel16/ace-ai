import pybaseball
import logging

logger = logging.getLogger(__name__)

class Tools:
    def __init__(self):
        self.tools = [
            {
                "name": "get_player_id",
                "description": "For a player's first and last name, retrieve the various IDs associated with that baseball player. This tool returns a list of dictionaries, with each record being a potential match for that player's first and last name that you input. Use it as the first step in answering a player specific question. You don't need this when the query doesn't involve a specific player.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "last_name": {
                            "type": "string",
                            "description": "The last name of the player you need to find."
                        },
                        "first_name": {
                            "type": "string",
                            "description": "The first name of the player you need to find."
                        }
                    },
                    "required": ["last_name", "first_name"]
                }
            }
        ]

    # get player id
    # 
    # The model will fix any typos in the name and/or deduce the first/last if given a generic name
    @staticmethod
    def get_player_id(last_name: str, first_name: str):
        return pybaseball.playerid_lookup(last_name, first_name).to_dict(orient='records')
    

    # get pitcher statcast data for a given range
    @staticmethod
    def get_pitcher_statcast(player_id: int,
                             start: str | None = None,
                             end: str | None = None,
                             pitch_type: str | None = None,
                             columns: list[str] | None = None):
        pitches = pybaseball.statcast_pitcher(start_dt=start, end_dt=end, player_id=player_id)
        if pitch_type:
            pitches = pitches[pitches["pitch_type"] == pitch_type]
        if columns:
            pitches = pitches[columns]
        return pitches.to_dict(orient='records')
    
    # get split stats
    @staticmethod
    def get_player_splits(player_id: int,
                          year: int | None = None,
                          player_info: bool = False,
                          pitching_splits: bool = False):
        return pybaseball.get_splits(player_id, year=year, player_info=player_info, pitching_splits=pitching_splits)