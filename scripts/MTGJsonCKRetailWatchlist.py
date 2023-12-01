# Fetches price trends from CK retail for expensive cards that I want
# python3 MTGJsonCKRetailWatchlist.py

import json
from system_consts import * 
import csv
import pprint
from MTGJsonFetcher import *


cards_to_check = [
    "Tundra",
    "Underground Sea",
    "Badlands",
    "Taiga",
    "Savannah",
    "Scrubland",
    "Bayou",
    "Tropical Island",
    "Volcanic Island",
    "Plateau",
    "Mox Diamond",
    "Null Rod",
    "Metalworker",
    "Tolarian Academy",
    "Moat",
    "Black Lotus",
    "Time Walk",
    "Ancestral Recall",
    "Timetwister",
    "Mox Pearl",
    "Mox Sapphire",
    "Mox Jet",
    "Mox Ruby",
    "Mox Emerald",
    "Chains of Mephistopheles",
    "Survival of the Fittest",
    "Bazaar of Baghdad",
    "City of Traitors",
    "Crystalline Crawler",
    "Druid of Purification",
    "Gamekeeper",
    "Ley Weaver",
    "Pitiless Plunderer",
    "Primeval Herald",
    "Alena, Kessig Trapper",
    "Seedguide Ash",
    #"Defiler of Vigor",
    #"Inkmoth Nexus",
    #"Arcbound Ravager",
]

specific_cards_to_check = [
    ("Polluted Delta", "EXP", None),
    ("Flooded Strand", "EXP", None),
    ("Bloodstained Mire", "EXP", None)
]

cards_to_check = [(card, None, None) for card in cards_to_check] + specific_cards_to_check

max_name_len = max([len(name[0]) for name in cards_to_check])

AllPrices = read_target('AllPrices')
AllIdentifiers = read_target('AllIdentifiers')
set_exceptions = ['CED', 'CEI', '30A']
for specific_card_to_check in cards_to_check:
    card_to_check = specific_card_to_check[0]
    specific_edition = specific_card_to_check[1]
    specific_foil = specific_card_to_check[2]
    for card in AllIdentifiers:
        if AllIdentifiers[card]['name'] == card_to_check:
            for foil in ['normal', 'foil']:
                if specific_foil != None and specific_foil != foil:
                    continue
                if specific_edition != None and AllIdentifiers[card]['setCode'] != specific_edition:
                    continue
                if card in AllPrices:
                    prices = nested_idx(AllPrices[card], ['paper', 'cardkingdom', 'retail', foil])
                    tcg_price = get_latest(nested_idx(AllPrices[card], ['paper', 'tcgplayer', 'retail', foil]))
                    print_str = "%s %s %s %s" % (AllIdentifiers[card]['setCode'].ljust(5), AllIdentifiers[card]['number'].ljust(6), foil.ljust(7), AllIdentifiers[card]['name'].ljust(max_name_len + 1))
                    prev_price = None
                    last_price = None
                    high_price = None
                    low_price = None
                    price_history = ""
                    if 'borderColor' in AllIdentifiers[card].keys() and AllIdentifiers[card]['borderColor'] == 'gold':
                        continue
                    if AllIdentifiers[card]['setCode'] in set_exceptions:
                        continue
                    if prices != None and len(prices) > 0:
                        for date in prices.keys():
                            last_price = prices[date]
                            if high_price == None or last_price > high_price:
                                high_price = last_price
                            if low_price == None or last_price < low_price:
                                low_price = last_price
                            if prev_price == None:
                                price_history += str(last_price).ljust(8)
                            else:
                                if prev_price == last_price:
                                    price_history += '-'
                                elif prev_price > last_price:
                                    price_history += '↓'
                                else:
                                    price_history += '↑'
                            prev_price = last_price
                        print_str += 'CU%s HI%s LO%s TCG%s %s%s'%(str(last_price).ljust(8), str(high_price).ljust(8), str(low_price).ljust(8), str(tcg_price).ljust(8), str(price_history), str(last_price))
                        if low_price == last_price and low_price != high_price:
                            print_str += " LOWEST!!"
                        if tcg_price != None and last_price < tcg_price:
                            print_str += " BEATS TCG!!"
                        print(print_str)
            continue
