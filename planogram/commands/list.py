import json
import helpers
import cards
import decklists
import inclusion
from jsonquerylang import jsonquery

def list(chosen_decklists):
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
    
    