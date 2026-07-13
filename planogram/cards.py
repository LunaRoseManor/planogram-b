import json
import os
import formats

def get_cards():
    CARDS_FILE = "data/cards.json"
    cards = []
    
    with open(CARDS_FILE, 'r', encoding="utf-8") as f:
        cards = json.load(f)
    
    return cards

def get_card(id):
    PATH = "data/cards.json"
    cards = []
    card = {}
    
    with open(PATH, 'r', encoding="utf-8") as f:
        cards = json.load(f)
    
    card = next(filter(lambda x: x["id"] == id, cards), None)
    
    return card
    
def get_card_title(id=""):
    PATH = "data/cards.json"
    cards = []
    card = {}
    
    with open(PATH, 'r', encoding="utf-8") as f:
        cards = json.load(f)
    
    card = next(filter(lambda x: x["id"] == id, cards), None)
    
    return card["attributes"]["title"]

def get_card_title(id="", card_pool=[]):
    card = next(filter(lambda x: x["id"] == id, card_pool), None)
    
    return card["attributes"]["title"]

def cache_legality():
    LEGALITY_FOLDER = "data/legality"
    CARDS = get_cards()
    FORMATS = formats.get_formats()
    
    if not os.path.exists(LEGALITY_FOLDER):
        os.makedirs(LEGALITY_FOLDER)
    
    for netrunner_format in FORMATS:
        PATH = LEGALITY_FOLDER + '/' + netrunner_format["id"] + ".json"
        active_card_pool_id = netrunner_format["attributes"]["active_card_pool_id"]
        active_restriction_id = netrunner_format["attributes"]["active_restriction_id"]
        
        with open(PATH, 'w', encoding="utf-8") as destination_file:
            legality = {}
            
            for card in CARDS:
                legality[card["id"]] = False # Assume cards to not be legal
                
                if active_card_pool_id in card["attributes"]["card_pool_ids"]:
                    if active_restriction_id not in card["attributes"]["restriction_ids"]:
                        legality[card["id"]] = True
             
            json.dump(legality, destination_file)
    