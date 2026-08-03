import json
import helpers
import cards

def get_inclusion_rates(decklists):
    inclusion_rates = []
    
    # NOTE: This method is extremely slow as it has to search every card in every decklist
    # and then every quantity in the local list. Sorting a dictionary where the id can be
    # used to find a ke
    for decklist in decklists:
        card_slots = decklist["attributes"]["card_slots"]
        
        for card_id in card_slots:
            # Find if there is an entry with the specified card id already in the list
            search_key = "id"
            search_value = card_id
            found = any(inclusion_rate.get(search_key) == search_value for inclusion_rate in inclusion_rates)
            
            # If an entry for that id doesn't already exist
            if not found:
                # Add it to the list with an assumed quantity of 1
                inclusion_rates.append({
                    "id": card_id,
                    "side_id": decklist["attributes"]["side_id"],
                    "faction_id": decklist["attributes"]["faction_id"],
                    "quantity": 1
                })
            else:
                # Find that dictionary in the list and increase the quantity
                search_result = next((rate for rate in inclusion_rates if rate["id"] == card_id), None)
                search_result["quantity"] += 1
    
    # Sort by inclusion rate
    inclusion_rates = sorted(inclusion_rates, key=lambda item: item["quantity"])
    
    return inclusion_rates