import json
import helpers
import cards
import decklists
import inclusion
from jsonquerylang import jsonquery

def list(chosen_decklists, sided=True):
    # This is my hack solution to being able to list optionally based on sides
    # This should 1000% be fixed up ASAP
    if sided:
        # Use split data instead so the inclusion rates can be seperated
        inclusion_rates = {
            "corp": inclusion.get_inclusion_rates(chosen_decklists["corp"]),
            "runner": inclusion.get_inclusion_rates(chosen_decklists["runner"])
        }
        card_num = len(inclusion_rates["corp"]) + len(inclusion_rates["runner"])
        inclusion_percentages = {}
        
        for side in inclusion_rates:
            for card in inclusion_rates[side]:
                print('#' + str(card_num) + '.',
                    card,
                    "included in",
                    str(
                        helpers.get_percentage_of_whole(inclusion_rates[side][card],
                            len(chosen_decklists[side]))) + "% of all " + side + " decklists")
                card_num -= 1
    else:
        inclusion_rates = inclusion.get_inclusion_rates(chosen_decklists)
        card_num = len(inclusion_rates)
        
        # Search the list of inclusion rates and output them to command line
        for card in inclusion_rates:
            print('#' + str(card_num) + '.',
                card,
                "included in",
                str(helpers.get_percentage_of_whole(inclusion_rates[card],
                    len(chosen_decklists))) + "% of all decklists")
            card_num -= 1
        
        print("Operation played, searched", len(chosen_decklists), "decks")

"""
Lists all cards in Netrunner across all formats based on data scraped using
the fetch command. This should be the default command.
"""
def list_all():
    list(decklists.get_all_decklists())
    
    