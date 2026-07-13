import json
import requests
import helpers
from jsonquerylang import jsonquery

"""
Determines the targets of fetch_all from a JSON file,
typically data/fetch_targets.json

Used to grab something to iterate over while using fetch()
"""
def get_targets(path="data/fetch_targets.json"):
    targets = []
    
    try:
        with open(path, 'r', encoding="utf-8") as f:
            targets = json.load(f)["data"]
    except:
        print("error: unable to read", path)
    
    return targets

"""
Retrieves JSON data from NetrunnerDB.
"""
def fetch(route="api/v3/public/card_cycles", path="data/default_fetch.json", name="unspecified"):
    BASE_URL = "https://api.netrunnerdb.com/"
    url = BASE_URL + route
    pages = []
    page_number = 1
    
    # Make a safe request for the data
    try:
        # Need to hack in a do while loop here because Python 3 doesn't have them
        # This should iterate over all the pages, if there are any
        while True:
            # NOTE: The use of Netrunner terminology from the rules and
            # lore might be a bit too cutesy, but it's my program and I
            # can do whatever I want.
            # 
            # Ideally output should be seperated
            print("Approaching", name, "server...")
            
            get_request = requests.get(url)
            content = get_request.content
            raw_data = json.loads(content)
            
            if "data" in raw_data:
                pages.append(raw_data["data"])
            
            if "next" in raw_data["links"]:
                print("Encountered new page", raw_data["links"]["next"], "at position", page_number + 1)
                
                url = raw_data["links"]["next"]
                page_number += 1
                
                print("Continuing to movement...")
            else:
                print("Accessed", name + '.')
                
                data = helpers.flatten_list(pages)
                
                # Cache the data to a local file and exit
                with open(path, 'w', encoding="utf-8") as f:
                    json.dump(data, f)
                
                print("Added", name, "to", path)
                
                break
    except:
        print("error: python exception thrown when attempting to fetch", name)
        raw_data = {} # Has to be cleared to ensure verification fails
    
    return data


"""
Fetches everything that can be gained from NetrunnerDB, as specified by
get_targets()
"""
def fetch_all():
    success = False
    
    print("Jacking in...")
    
    try:
        BASE_URL = "https://api.netrunnerdb.com/"
        GET_REQUEST = requests.get(BASE_URL)
        
        if GET_REQUEST.status_code == 200:
            print("Connected to", BASE_URL)
            print("Initiating fetch...")
            
            COMMON_ROUTE = "api/v3/public/"
            DATA_FOLDER = "data/"
            TARGETS = get_targets()
            data = {}
            
            # Store local copies of the data in memory for verification
            for target in TARGETS:
                data[target] = fetch(route=COMMON_ROUTE + target, path=DATA_FOLDER + target + ".json", name=target)
        else:
            print("error: connection to NetrunnerDB API failed with code", GET_REQUEST.status_code)
    except:
        print("error: exception thrown during general purpose fetch")
    
    # TODO: Fix data verification on fetch_all()
    # The fetch will only be successful when all the data is found
    #if "data" in card_cycles and "data" in card_pools and "data" in card_set_types:
    #    success = True
    
    success = True
    
    # Give the user some feedback regardless of success
    print("Ending the run...")
    
    return success