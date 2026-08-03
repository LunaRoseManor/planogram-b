import json
import helpers

def get_factions():
    PATH = "data/factions.json"
    RAW_DATA = helpers.get_dict_from_json_file(PATH)["data"]
    factions = []
    
    for faction in RAW_DATA:
        if not faction["id"] in factions:
            factions.append(faction["id"])

    return factions