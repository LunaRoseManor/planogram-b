import json
import helpers

def get_side_ids():
    PATH = "data/sides.json"
    sides = helpers.get_list_from_json_file(PATH)["data"]
    side_ids = []
    
    for side in sides:
        side_ids.append(side["id"])
    
    return side_ids