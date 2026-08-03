import json
import helpers
import cards
import titles
import decklists
import inclusion
from jsonquerylang import jsonquery

def list(chosen_decklists):    
    # Use split data instead so the inclusion rates can be seperated
    inclusion_rates = inclusion.get_inclusion_rates(chosen_decklists)
    card_num = len(inclusion_rates)
    card_titles = titles.get_titles()
    inclusion_percentages = {}
    output = ""
    
    for rate in inclusion_rates:
        line = '#' + str(card_num)
        output = output + line
        card_num -= 1
    
    print(output)
    print("Operation played, searched", len(chosen_decklists), "decks")
    
    return output

"""
Lists all cards in Netrunner across all formats based on data scraped using
the fetch command. This should be the default command.
"""
def list_all():
    list(decklists.get_all_decklists())
    
    