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
    split_decklists = decklists.split_by_side(chosen_decklists)
    card_num = len(inclusion_rates)
    card_titles = titles.get_titles()
    inclusion_percentages = {}
    output = ""
    
    # Determine the output by iterating over the calculated inclusion rates
    for rate in inclusion_rates:
        line = '#' + str(card_num) + ". " + card_titles[rate["id"]] + " included in " + str(helpers.get_percentage_of_whole(rate["quantity"], len(split_decklists[rate["side_id"]]))) + "% of all " + rate["side_id"] + " decklists\n"
        output = output + line
        card_num -= 1
    
    # Print the total output to the screen
    print(output)
    print("Operation played, searched", len(chosen_decklists), "total decks")
    print("(" + str(len(split_decklists["corp"])), "corp,", len(split_decklists["runner"]), "runner)")
    
    return output

"""
Lists all cards in Netrunner across all formats based on data scraped using
the fetch command. This should be the default command.
"""
def list_all():
    list(decklists.get_all_decklists())
    
    