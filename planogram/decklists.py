import json
from jsonquerylang import jsonquery
import cards
import sides
import formats
import os
import helpers

def get_filtered_to_legal(decklists, format_id="standard"):
    PATH = "data/legality/" + format_id + ".json"
    legal_decklists = []
    legality = helpers.get_dict_from_json_file(PATH)
    
    for decklist in decklists:
        legal = True
        
        # The data needs to be validated before it can be moved.
        # If one card slot contains a rotated or banned card,
        # it can't be legal.
        for card in decklist["attributes"]["card_slots"]:
            if legality[card] != True:
                legal = False
        
        # Banned identities also can't be included!
        if legality[decklist["attributes"]["identity_card_id"]] == False:
            legal = False
        
        # Decklists filtered must follow the formatting rules
        if decklist["attributes"]["follows_basic_deckbuilding_rules"] == False:
            legal = False
        
        # Only add legal decklists to the format list
        if legal:
            legal_decklists.append(decklist)
    
    return legal_decklists

def cache_legal_decklists():
    # New formats might be added, so we need to reference the file when caching
    current_format_ids = formats.get_format_ids()
    # Netrunner is an asymmetrical game, so there needs to be room in the
    # data to distinguish the different sides
    decklists_raw = get_all_decklists()
    legal_decklists = {}
    legality = {}
    side_ids = sides.get_side_ids()
    
    # Create the global decklist caches in the root decklist folder for each format
    for format_id in current_format_ids:
        legality = helpers.get_dict_from_json_file("data/legality/" + format_id + ".json")
        legal_decklists = get_filtered_to_legal(decklists_raw, format_id)
        format_decklists_file = "data/decklists/" + format_id + ".json"
        
        helpers.dump_json_to_file(legal_decklists, format_decklists_file)
    
    # Then for each side in each format
    for side_id in side_ids:
        sided_decklist_folder = "data/decklists/" + side_id
        
        # Make the destination folder for the sided decklists if it doesn't already exist.
        if not os.path.exists(sided_decklist_folder):
            print("OK")
            os.makedirs(sided_decklist_folder)
        
        print(side_id)

def is_side(decklist, side_id="corp"):
    return decklist["attributes"]["side_id"] == side_id

def split_by_side(decklists):
    split_decklists = {
        "corp": [],
        "runner": []
    }
    
    for decklist in decklists:
        if is_side(decklist, "runner"):
            split_decklists["runner"].append(decklist)
        elif is_side(decklist, "corp"):
            split_decklists["corp"].append(decklist)
    
    print(split_decklists["corp"])
    
    return split_decklists

def get_decklists(format="standard"):
    DECKLISTS_FILE = "data/decklists/" + format + ".json"
    decklists = []

    try:
        with open(DECKLISTS_FILE, 'r', encoding="utf-8") as f:
            decklists = json.load(f)
    except:
        print("Error: invalid format selection")

    return decklists

def get_all_decklists():
    return helpers.get_list_from_json_file("data/decklists.json")