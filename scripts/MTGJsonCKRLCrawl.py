# Fetches price trends from CK retail for expensive cards that I want
# python3 MTGJsonCKRetailWatchlist.py

import json
from system_consts import * 
import csv
import pprint
from MTGJsonFetcher import *


max_name_len = 20

AllPrices = read_target('AllPrices')
AllIdentifiers = read_target('AllIdentifiers')
set_exceptions = ['CED', 'CEI', '30A']
cards = []
for card in AllIdentifiers:
    if 'isReserved' not in AllIdentifiers[card].keys() or not AllIdentifiers[card]['isReserved']:
        continue
    for foil in ['normal', 'foil']:
        if card in AllPrices:
            prices = nested_idx(AllPrices[card], ['paper', 'cardkingdom', 'retail', foil])
            tcg_price = get_latest(nested_idx(AllPrices[card], ['paper', 'tcgplayer', 'retail', foil]))
            if tcg_price == None or tcg_price < 10:
                continue   
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
            if prices != None and len(prices) > 0 and tcg_price != None:
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
                if (last_price/tcg_price < 1.2):
                    cards.append((last_price/tcg_price, print_str))
            else:
                continue

cards = sorted(cards, key=lambda x:x[0])
for card in cards:
    print(card[1])
print("Done.")