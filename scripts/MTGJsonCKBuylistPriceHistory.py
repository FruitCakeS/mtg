import json
from system_consts import * 
import csv
import pprint
from MTGJsonFetcher import read_target


cards_to_check = [
    "Mox Diamond",
    "Null Rod",
    "Candelabra of Tawnos",
    "Metalworker",
    "Tolarian Academy",
    "Moat",
]


def nested_idx(obj, idxes):
    intermediate = obj
    for idx in idxes:
        if idx in intermediate:
            intermediate = intermediate[idx]
        else:
            return None
    return intermediate

def get_latest(prices):
    if prices == None:
        return None
    return prices[max(prices.keys())]



AllPrices = read_target('AllPrices')
AllIdentifiers = read_target('AllIdentifiers')

for card in AllIdentifiers:
    if AllIdentifiers[card]['name'] in cards_to_check:
        for foil in ['normal', 'foil']:
            if card in AllPrices:
                prices = nested_idx(AllPrices[card], ['paper', 'cardkingdom', 'retail', foil])
                print_str = "%s %s %s " % (AllIdentifiers[card]['setCode'].ljust(4), AllIdentifiers[card]['number'].ljust(6), AllIdentifiers[card]['name'].ljust(30))
                prev_price = None
                last_price = None
                high_price = None
                low_price = None
                price_history = ""
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
                    print_str += 'CU%s HI%s LO%s %s%s'%(str(last_price).ljust(8), str(high_price).ljust(8), str(low_price).ljust(8), str(price_history), str(last_price))
                    if low_price == last_price:
                        print_str += " LOWEST!!"
                    print(print_str)
