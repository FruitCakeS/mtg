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
    "Metalworker",
    "Tolarian Academy",
    "Moat",
    "The Tabernacle at Pendrell Vale",
    "Library of Alexandria",
    "Black Lotus",
    "Time Walk",
    "Ancestral Recall",
    "Timetwister",
    "Mox Pearl",
    "Mox Sapphire",
    "Mox Jet",
    "Mox Ruby",
    "Mox Emerald",
    "Bazaar of Baghdad",
    "Grim Tutor",
    "Culling the Weak",
    "Lake of the Dead",
    "Druid of Purification",
    "Seedguide Ash",
    "Test of Endurance",
    "Academy Rector",
]

specific_cards_to_check = [
    ("Polluted Delta", "EXP", None, None),
    ("Flooded Strand", "EXP", None, None),
    ("Bloodstained Mire", "EXP", None, None),
    ("Polluted Delta", "MH3", 'foil', '438'),
    ("Flooded Strand", "MH3", 'foil', '436'),
    ("Bloodstained Mire", "MH3", 'foil', '435'),
    ("Ulamog, the Infinite Gyre", "2X2", None, '577'),
    ("Sorin of House Markov", "MH3", None, '470'),
    ("Tamiyo, Inquisitive Student", "MH3", None, '469'),
]

cards_to_check = [(card, None, None, None) for card in cards_to_check] + specific_cards_to_check

max_name_len = max([len(name[0]) for name in cards_to_check])

AllPrices = read_target('AllPrices')
AllIdentifiers = read_target('AllIdentifiers')
set_exceptions = ['CED', 'CEI', '30A']
for specific_card_to_check in cards_to_check:
    card_to_check = specific_card_to_check[0]
    specific_edition = specific_card_to_check[1]
    specific_foil = specific_card_to_check[2]
    specific_number = specific_card_to_check[3]
    for card in AllIdentifiers:
        if AllIdentifiers[card]['name'] == card_to_check:
            for foil in ['normal', 'foil']:
                if specific_foil != None and specific_foil != foil:
                    continue
                if specific_edition != None and AllIdentifiers[card]['setCode'] != specific_edition:
                    continue
                if specific_number != None and AllIdentifiers[card]['number'] != specific_number:
                    continue
                if card in AllPrices:
                    prices = nested_idx(AllPrices[card], ['paper', 'cardkingdom', 'retail', foil])
                    tcg_price = get_latest(nested_idx(AllPrices[card], ['paper', 'tcgplayer', 'retail', foil]))
                    print_str = "%s %s %s %s" % (str(AllIdentifiers[card]['setCode']).ljust(5), str(AllIdentifiers[card]['number']).ljust(6), str(foil).ljust(7), str(AllIdentifiers[card]['name']).ljust(max_name_len + 1))
                    prev_price = None
                    last_price = None
                    high_price = None
                    low_price = None
                    first_price = 0
                    price_history = ""
                    if 'borderColor' in AllIdentifiers[card].keys() and AllIdentifiers[card]['borderColor'] == 'gold':
                        continue
                    if AllIdentifiers[card]['setCode'] in set_exceptions:
                        continue
                    if prices != None and len(prices) > 0:
                        price_history += '-'*(90-len(prices.keys()))
                        for date in prices.keys():
                            last_price = prices[date]
                            if high_price == None or last_price > high_price:
                                high_price = last_price
                            if low_price == None or last_price < low_price:
                                low_price = last_price
                            if prev_price == None:
                                first_price += last_price
                            else:
                                if prev_price == last_price:
                                    price_history += '-'
                                elif prev_price > last_price:
                                    price_history += '\x1b[6;30;42m'+'↓'
                                else:
                                    price_history += '\x1b[0;37;41m'+'↑'
                            prev_price = last_price
                        price_history += '\x1b[0m'

                        print_str += '%sCU%s%s HI%s LO%s TCG%s %s%s'%(
                            '\x1b[6;30;43m' if last_price == low_price and tcg_price != None and last_price < tcg_price else'\x1b[6;31;42m' if last_price == low_price and tcg_price == None else '\x1b[0;37;41m' if last_price != low_price else '\x1b[2;30;42m',
                            str(last_price).ljust(10),
                            '\x1b[0m', 
                            str(high_price).ljust(10), 
                            str(low_price).ljust(10), 
                            str(tcg_price).ljust(10), 
                            str(price_history), 
                            str(last_price).ljust(8))
                        print(print_str)
            continue
show_freshness()
