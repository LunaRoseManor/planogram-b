import json
from jsonquerylang import jsonquery
import argparse
from commands import retrieve, list
import cards
import titles
import decklists
import os
from datetime import datetime

"""
Retrieves global config data from the specified file
"""
def get_config():
    PATH = "data/config.json"
    config = {}
    
    with open(PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # Include the path to the config file for error handling
    config["path"] = PATH
    
    return config

def generate_config_file():
    PATH = "data/config.json"
    DATA = {
        "app_id": "planogram",
        "prog": "Planogram",
        "description": "Command line EDHREC for Netrunner",
        "epilog": "",
        "prefix_chars": "-",
        "color": True,
        "args": [
            {
                "flags": [
                    "-r",
                    "--retrieve"
                ],
                "action": "store_true",
                "type": "str",
                "nargs": 0,
                "required": False,
                "help": "Retrieves latest data for card types, cards, decklists, factions, formats, restrictions, sides and snapshots from NetrunnerDB's API."
            },
            {
                "flags": [
                    "-q",
                    "--query"
                ],
                "action": "store",
                "type": "str",
                "nargs": 1,
                "required": False,
                "help": "Filters decklist input data using jsonquerylang syntax"
            },
            {
                "flags": [
                    "-f",
                    "--format"
                ],
                "action": "store",
                "type": "str",
                "nargs": 1,
                "required": False,
                "help": "Choose which format decklist data is filtered from"
            }
        ]
    }
    
    # Attempt to write the above data to a file
    with open(PATH, 'w', encoding="utf-8") as f:
        json.dump(DATA, f, indent=4)

def get_args():
    CONFIG = get_config()
    parser = argparse.ArgumentParser(prog=CONFIG["prog"],
        description=CONFIG["description"],
        epilog=CONFIG["epilog"],
        prefix_chars=CONFIG["prefix_chars"],
        color=CONFIG["color"])
    
    # Command line arguments for Planogram are based on data from the config file.
    # This allows for an arbitrary number that can be easily changed.
    # The following code fetches every argument from that file and adds it to the
    # parser with the correct type.
    for arg in CONFIG["args"]:
        # First determine whether the argument has a name or flags
        # TODO: Robustly re-implement for all argparse parameters
        if "name" in arg:
            # Positional arguments can't be required by argparse
            if arg["name"][0] == '-':
                # TODO: Support arbitrary argument data types
                parser.add_argument(arg["name"], action=arg["action"], required=arg["required"], help=arg["help"])
            else:
                parser.add_argument(arg["name"], help=arg["help"])
        elif "flags" in arg:
            # Instead, add the argument using it's full name and shortcode
            # But to do that, planogram needs to do more selection to allow for
            # simpler arguments that assume default values.
            # Here we're assuming that all flags begin with a prefix
            if "action" in arg:
                # NOTE: nargs started throwing a tantrum when I tried to support it,
                # so it's been omitted from the selection logic.
                if "default" in arg:
                    if "choices" in arg:
                        if "required" in arg:
                            if "help" in arg:
                                parser.add_argument(arg["flags"][0], arg["flags"][1],
                                    action=arg["action"],
                                    default=arg["default"],
                                    choices=arg["choices"],
                                    required=arg["required"],
                                    help=arg["help"])
                            else:
                                parser.add_argument(arg["flags"][0], arg["flags"][1],
                                    action=arg["action"],
                                    default=arg["default"],
                                    choices=arg["choices"],
                                    required=arg["required"])
                        else:
                            parser.add_argument(arg["flags"][0], arg["flags"][1],
                                action=arg["action"],
                                default=arg["default"],
                                choices=arg["choices"])
                    else:
                        if "required" in arg:
                            if "help" in arg:
                                parser.add_argument(arg["flags"][0], arg["flags"][1],
                                    action=arg["action"],
                                    default=arg["default"],
                                    required=arg["required"],
                                    help=arg["help"])
                            else:
                                parser.add_argument(arg["flags"][0], arg["flags"][1],
                                    action=arg["action"],
                                    default=arg["default"],
                                    required=arg["required"])
                        else:
                            parser.add_argument(arg["flags"][0], arg["flags"][1],
                                action=arg["action"],
                                default=arg["default"])
                else:
                    parser.add_argument(arg["flags"][0], arg["flags"][1],
                        action=arg["action"])
            else:
                parser.add_argument(arg["flags"][0], arg["flags"][1])
        elif "name" in arg and "flags" in arg:
            print("error: argument", arg["name"], "can't also have flags.")
        else:
            print("error: missing name or flags for command line argument in", CONFIG["path"])
    
    # Turn the arguments list into actionable data
    args = vars(parser.parse_args())
    
    return args

def is_installed():
    install_file_name = "install.json"
    installed = False
    
    if os.path.exists(install_file_name):
        installed = True
    
    return installed

def install():
    # Output to let the user know first time setup is being run
    print("Installing...")
    
    # Installation requires variables to be established
    install_file_name = "install.json"
    data_folder_path = "data"
    
    # Cache information about the current install
    # Once this file is cached, planogram should assume it's been installed
    with open(install_file_name, 'w', encoding="utf-8") as f:
        data = {
            "installed": True,
            "date": datetime.today().strftime('%Y-%m-%d')
        }
        json.dump(data, f)
    
    # Create the data folder if it doesn't already exist
    if not os.path.isdir("data"):
        print("NOTICE: Data folder doesn't exist.")
        print("Creating...")
        os.makedirs(data_folder_path)
    
    if not os.path.exists("data/config.json"):
        generate_config_file()
    
    print("Installed!")
    
    return True

def main():
    # Check if first run setup is complete
    installed = is_installed()
    
    if installed:
        # Retrieve argument data both from the file and user input
        args = get_args()
        
        # Then, check which of the flags has been used
        # The retrieve flag is checked for first, and is handled like a seperate program
        if args["retrieve"]:
            # The fetch command requires double verification because of how long it takes.
            selection = input("Are you sure? This will take a lot of clicks! (Y/n): ")
            success = False # TODO: Change back to false
            
            if selection == 'Y':
                # Only attempt a NetrunnerDB fetch if the user agrees.
                success = retrieve.fetch_all()
                
                # Extra user feedback based on how the fetch went
                if success == True:
                    print("Caching...")
                    
                    decklists.cache_legal_decklists()
                    cards.cache_legality()
                    titles.cache_titles()
                    
                    print("Success!")
                else:
                    print("Unsuccessful.")
            elif selection != 'n':
                print("error: selection can only be 'Y' or 'n'.")
            
            return
        
        # I added this output because some operations are quite slow
        print("Please wait...")
        
        # Otherwise, the output data should be modified based on program flags
        # The list of decklists searched starts with every single one being in the cache
        filtered_decklists = decklists.get_all_decklists()
        
        # The query command is for raw json queries
        # This should be deprecated at some stage
        # It's only really for debugging purposes
        if args["query"] != None:
            query = args["query"]
            filtered_decklists = jsonquery(filtered_decklists, query)
        
        # Allows users to search by format
        # NOTE: The method won't use for multiple operands, same as above
        if args["format"] != None:
            filtered_decklists = decklists.get_decklists(args["format"])
        
        # Finally, the output should be displayed
        # By default this is just a big list of top cards
        output = list.list(filtered_decklists)
        
        with open("output_file.txt", 'w', encoding="utf-8") as f:
            f.write(output)
        
        card_titles = titles.get_titles()
    else:
        print("WARNING: First time setup hasn't been run")
        
        install()

if __name__ == "__main__":
    main()