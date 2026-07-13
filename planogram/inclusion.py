import json

def get_inclusion_rates(decklists):
    inclusion_rates = {}
    
    # Using a brute force approach, this loop creates a key for each unique card
    # it finds in the provided decklists, 
    for decklist in decklists:
        card_slots = decklist["attributes"]["card_slots"]
        
        for card in card_slots:
            if card not in inclusion_rates:
                inclusion_rates[card] = 1
            else:
                inclusion_rates[card] += 1
    
    # Sort by inclusion rate
    inclusion_rates = dict(sorted(inclusion_rates.items(), key=lambda item: item[1]))
    
    return inclusion_rates