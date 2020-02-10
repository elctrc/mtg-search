import json
import requests

def main():
    end_query = False
    final_list = []
    while end_query == False:
        query = get_input()
        if query == "q":
            end_query = True
        else:
            new_card = build_card(query)
            final_list.append(new_card)
    print(final_list)

def get_input():
    return(input("Enter card name (q for quit): "))

def get_request(card):
    r = requests.get('https://api.scryfall.com/cards/search?q={}'.format(card))
    r_text = r.text
    r_json = json.loads(r_text)
    return(r_json["data"][0])

def get_atts(card):
    card_name = card["name"]
    set_name = card["set_name"]
    prices = card["prices"]
    card_atts = {
        "name": card_name,
        "set": set_name,
        "prices": prices
    }
    print("Card Name: {}\nSet: {}".format(card_name, set_name))
    print("Normal: {}\nFoil: {}".format(prices["usd"], prices["usd_foil"]))
    return(card_atts)

def build_card(q):
    card_request = get_request(q)
    atts = get_atts(card_request)
    return(atts)

if __name__ == "__main__":
    main()

# @TODO:
# Pretty print results
# Store results in text file
# More fuzzy searching, return multiple results

