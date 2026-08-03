import json
import helpers

def get_inclusion_rates(decklists):
    inclusion_rates = []
    
    # Using a brute force approach, this loop creates a key for each unique card
    # it finds in the provided decklists, then stores the quantity as an int
    for decklist in decklists:
        card_slots = decklist["attributes"]["card_slots"]
        
        for card in card_slots:
            if card not in inclusion_rates:
                inclusion_rates[card] = {
                    "side": decklist["attributes"]["side_id"],
                    "quantity": 1
                }
            else:
                inclusion_rates[card]["quantity"] += 1
    
    # Sort by inclusion rate
    inclusion_rates = dict(sorted(inclusion_rates, key=lambda item: item["quantity"]))
    
    helpers.pretty_print_json(inclusion_rates)
    
    return inclusion_rates