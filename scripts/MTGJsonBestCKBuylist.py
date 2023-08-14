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
cards = []
card_names = []
set_exceptions = ['ZNE', 'STA']
prices=[]
try:
    with open(files_path+'collection_parsed.csv') as csv_file:
        reader = csv.reader( (line.replace('\0','') for line in csv_file) )

        for row in reader:
            if len(row) < 6:
                continue
            try:
                uuid = row[0]
                foil = row[9].lower()
            except:
                continue
            if uuid not in AllIdentifiers:
            	continue
            if AllIdentifiers[uuid]['setCode'] in set_exceptions:
            	continue

            ck_buy = None
            tcg_retail = None
            ck_retail = None
            ck_buy = get_latest(nested_idx(AllPrices[uuid], ['paper', 'cardkingdom', 'buylist', foil]))
            tcg_retail =  get_latest(nested_idx(AllPrices[uuid], ['paper', 'tcgplayer', 'retail', foil]))
            if ck_buy != None and tcg_retail != None and ck_buy/tcg_retail > 0.85:
                if uuid in AllIdentifiers and ('isReserved' not in AllIdentifiers[uuid].keys() or not AllIdentifiers[uuid]['isReserved']):
                    prices.append((ck_buy/tcg_retail, ck_buy, tcg_retail, AllIdentifiers[uuid]['name'], AllIdentifiers[uuid]['setCode'], foil, AllIdentifiers[uuid]['number']))
                else:
                    print("Card not found %s" % (uuid))


except Exception as e:
    print(traceback.format_exc())

prices = sorted(prices, key=lambda x: (x[1]))
for price in prices:
    print(price[4], price[6], price[5], price[3], price[1], price[2], price[0])