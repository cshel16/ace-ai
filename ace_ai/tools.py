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
            },
            {
                "name": "get_pitcher_statcast",
                "description": "Using a player's MLBAM ID, get the statcast data for every individual pitch thrown over a specific time frame. This tool returns a list of dictionaries, where each list item is a pitch. This tool can filter on start and end date, pitch type, and specific columns or metrics. This tool is primarly used for individual pitch statcast analysis. Statcast data didn't become available until the 2008 season.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "player_id": {
                            "type": "integer",
                            "description": "The MLBAM ID associated with the player"
                        },
                        "start": {
                            "type": "string",
                            "description": "The start date (inclusive) to collect data for. Format is YYYY-MM-dd. If omitted, defaults to yesterday."
                        },
                        "end": {
                            "type": "string",
                            "description": "The end date (inclusive) to collect data for. Format is YYYY-MM-dd. If omitted, the query will return a single day of data."
                        },
                        "sort_by": {
                            "type": "string",
                            "description": "The name of a single Statcast table column to sort by."
                        },
                        "ascending": {
                            "type": "boolean",
                            "description": "If sort_by is used, set this to True to sort by ascending. If omitted, it will default to descending sort."
                        },
                        "pitch_type": {
                            "type": "string",
                            "description": "The official Statcast pitch type code to filter the result by. If omitted, the result will include all pitch types."
                        },
                        "columns": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "The Statcast pitch-level dataset columns to keep in the result. This needs to be a list of strings where each string is exactly the column name to keep. If omitted, will keep all columns for analysis. This is helpful for filtering columns when you know we only care about a certain metric, like release_speed."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Limit the number of records to send back to Claude. This is applied last, so all filters will apply, and then it will grab the top X results."
                        }

                    },
                    "required": ["player_id"]
                }
            },
            {
                "name": "get_player_splits",
                "description": "Using a player's Baseball Reference ID (key_bbref), retrieve split stats for a player for either a whole season or their whole career. This cannot provide more granular data than yearly. Returns batting or pitching splits broken down by various categories (e.g., vs LHP/RHP, home/away). Use this for aggregate performance breakdowns rather than pitch-level data.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "player_id": {
                            "type": "string",
                            "description": "The Baseball Reference ID (key_bbref) associated with the player"
                        },
                        "year": {
                            "type": "integer",
                            "description": "The season year to get splits for. If omitted, returns career splits."
                        },
                        "player_info": {
                            "type": "boolean",
                            "description": "Whether to include general player info. Defaults to false."
                        },
                        "pitching_splits": {
                            "type": "boolean",
                            "description": "Set to true for pitching splits, false for batting splits. Defaults to false."
                        }
                    },
                    "required": ["player_id"]
                }
            }
        ]
        self.tool_handlers = {
            "get_player_id": self.get_player_id,
            "get_pitcher_statcast": self.get_pitcher_statcast,
            "get_player_splits": self.get_player_splits
        }

    # get player id
    # 
    # The model will fix any typos in the name and/or deduce the first/last if given a generic name
    @staticmethod
    def get_player_id(last_name: str, first_name: str):
        return pybaseball.playerid_lookup(last_name, first_name).to_dict(orient='records')
    

    # get pitcher statcast data for a given range
    @staticmethod
    def get_pitcher_statcast(player_id: int,
                             start: str = None,
                             end: str = None,
                             sort_by: str = None,
                             ascending: bool = False,
                             pitch_type: str = None,
                             columns: list[str] = None,
                             limit: int = None):
        pitches = pybaseball.statcast_pitcher(start_dt=start, end_dt=end, player_id=player_id)
        if sort_by:
            pitches = pitches.sort_values(by=sort_by, ascending=ascending)
        if pitch_type:
            pitches = pitches[pitches["pitch_type"] == pitch_type]
        if columns:
            pitches = pitches[columns]
        if limit:
            pitches = pitches.head(limit)
        return pitches.to_dict(orient='records')
    
    # get split stats
    @staticmethod
    def get_player_splits(player_id: int,
                          year: int = None,
                          player_info: bool = False,
                          pitching_splits: bool = False):
        response = pybaseball.get_splits(player_id, year=year, player_info=player_info, pitching_splits=pitching_splits)    
        if isinstance(response, tuple):                                                                                                                          
            return response[0].to_dict(orient='records')
        return response.to_dict(orient='records')