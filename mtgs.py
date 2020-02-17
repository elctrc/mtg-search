import json
import logging
import time
import pandas as pd
import requests

def main():
    # Setup logging
    # lformat = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig()

    end_query = False
    final_list = []
    while end_query == False:
        query = get_input()
        if query == "q":
            end_query = True
        else:
            # new_card = build_card(query)
            card_request = get_request(query)
            if card_request == "Error":
                pass
            else:
                card_list = get_atts(card_request)
                final_list.append(card_list)

    df = pd.DataFrame(final_list)
    # Get current time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    # Export final list to csv
    df.to_csv("data/export_{}.csv".format(timestr))
    print("\n------ Your Pricelist ------")
    print(df)

def get_input():
    """Get user input"""
    return(input("Enter card name (q for quit): "))

def get_request(card):
    """Take user input and make API request"""
    r = requests.get('https://api.scryfall.com/cards/search?q={}&unique=prints'.format(card))
    r_text = r.text
    r_json = json.loads(r_text)
    try:
        return(r_json["data"])
    except KeyError:
        logging.warning("Card not found")
        return("Error")

def get_atts(data):
    """Return dict with name, set, and price of card"""
    cards = []
    for i, card in enumerate(data):
        card_name = card["name"]
        set_name = card["set_name"]
        prices = card["prices"]
        card_atts = {
            "name": card_name,
            "set": set_name,
            "price_normal": prices["usd"],
            "price_foil": prices["usd_foil"]
        }
        print("Result: {}".format(i))
        print("Card Name: {}\nSet: {}".format(card_name, set_name))
        print("Normal: {}\nFoil: {}".format(prices["usd"], prices["usd_foil"]))
        print("\n")
        cards.append(card_atts)
    return(card_selector(cards))
    # return(cards)

def card_selector(card_list):
    card_select = input("Select result number (N)one: ")
    card = card_list[int(card_select)]
    print("\n------ YOUR SELECTION ------")
    print("Card Name: {}\nSet: {}".format(card['name'], card['set']))
    print("Normal: {}\nFoil: {}".format(card["price_normal"], card["price_foil"]))
    print("\n")
    return(card)


# def build_card(q):
#     card_request = get_request(q)
#     return(get_atts(card_request))


if __name__ == "__main__":
    main()

# @TODO:
# Pretty print results
# Store results in text file
# More fuzzy searching, return multiple results
# Send to Google Sheets
