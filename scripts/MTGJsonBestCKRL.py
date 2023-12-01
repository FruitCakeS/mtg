# Parse through collection and find the best cards to buylist to Card Kingdom
# Based on % value of TCG price

import json
from system_consts import * 
import csv
import pprint
from MTGJsonFetcher import read_target
import traceback



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


AllIdentifiers = read_target('AllIdentifiers')
AllPrices = read_target('AllPrices')
AllPrintings = read_target('AllPrintings')
cards = []
card_names = []
total = len(AllPrices)
count = 0
set_exceptions = []
set_limits = []
count = 0
prices=[]
set_exceptions = ['30A', '10E', '9ED', 'UPLIST', 'WC00', 'WC99']
for uuid, card in AllPrices.items():
    if (count % 1000 == 0):
        print('parsing '+str(count)+' of '+str(total)+' prices...')
    count+=1
    foil = 'normal'
    if uuid not in AllIdentifiers or AllIdentifiers[uuid] == None or AllIdentifiers[uuid]['setCode'] == None:
        continue
    if AllIdentifiers[uuid]['setCode'] not in AllPrintings.keys() or AllPrintings[AllIdentifiers[uuid]['setCode']] == None:
        continue
    if AllIdentifiers[uuid]['setCode'] in set_exceptions:
        continue
    if 'releaseDate' not in AllPrintings[AllIdentifiers[uuid]['setCode']].keys():
        continue
    if AllPrintings[AllIdentifiers[uuid]['setCode']]['releaseDate'] > '2005-01-01':
        continue
    if 'isReserved' not in AllIdentifiers[uuid].keys() or not AllIdentifiers[uuid]['isReserved']:
        continue   
    
    ck_retail = get_latest(nested_idx(card, ['paper', 'cardkingdom', 'retail', foil]))
    tcg_retail =  get_latest(nested_idx(card, ['paper', 'tcgplayer', 'retail', foil]))
    if ck_retail != None and tcg_retail != None and ck_retail >= 4.99 and ck_retail <=100 and ck_retail/tcg_retail < 1.1:
        if uuid in AllIdentifiers:
            prices.append((ck_retail/tcg_retail, ck_retail, tcg_retail, AllIdentifiers[uuid]['name'], AllIdentifiers[uuid]['setCode'], foil, AllIdentifiers[uuid]['number']))
        else:
            print("Card not found %s" % (uuid))

prices = sorted(prices, key=lambda x: (x[2]-x[1]))
for price in prices:
    print(price[4], price[6], price[5], price[3], price[1], price[2], price[0])

