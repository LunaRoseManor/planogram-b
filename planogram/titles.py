import json
import cards

def cache_titles():
    CARDS = cards.get_cards()
    
    try:
        TITLES_FILE = "data/card_titles.json"
        titles = {}
        
        for card in CARDS:
            titles[card["id"]] = card["attributes"]["title"]
        
        with open(TITLES_FILE, 'w', encoding="utf-8") as f:
            json.dump(titles, f)
        
    except:
        print("ERROR: Failed to cache card titles")

def get_titles():
    titles = {}
    
    try:
        TITLES_FILE = "data/card_titles.json"
        
        with open (TITLES_FILE, 'r', encoding="utf-8") as f:
            titles = json.load(f)
    except:
        print("ERROR: Titles file does not exist or failed to load")
    
    return titles