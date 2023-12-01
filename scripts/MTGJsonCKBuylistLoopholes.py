import json
from system_consts import * 
import csv
import pprint
from MTGJsonFetcher import read_target
from datetime import date

target_sets = []

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
total = len(AllPrices)
count = 0
prices=[]
set_exceptions = ['30A', '10E', '9ED', 'UPLIST']
for uuid, card in AllPrices.items():
    if (count % 1000 == 0):
        print('parsing '+str(count)+' of '+str(total)+' prices...')
    count+=1
    for foil in ['normal', 'foil']:
        if uuid not in AllIdentifiers or AllIdentifiers[uuid] == None or AllIdentifiers[uuid]['setCode'] == None:
            continue
        if AllIdentifiers[uuid]['setCode'] not in AllPrintings.keys() or AllPrintings[AllIdentifiers[uuid]['setCode']] == None:
            continue
        if AllIdentifiers[uuid]['setCode'] in set_exceptions:
            continue
        if 'releaseDate' not in AllPrintings[AllIdentifiers[uuid]['setCode']].keys():
            continue
        if 'isPaperOnly' in AllPrintings[AllIdentifiers[uuid]['setCode']].keys() and AllPrintings[AllIdentifiers[uuid]['setCode']]['isPaperOnly'] and AllPrintings[AllIdentifiers[uuid]['setCode']]['releaseDate'] < '2020-01-01':
            continue
        if AllPrintings[AllIdentifiers[uuid]['setCode']]['releaseDate'] < '2010-01-01' and foil:
            continue
        if AllPrintings[AllIdentifiers[uuid]['setCode']]['releaseDate'] < '2005-01-01':
            continue
        
        ck_buy = None
        tcg_retail = None
        ck_retail = None
        ck_buy = get_latest(nested_idx(card, ['paper', 'cardkingdom', 'buylist', foil]))
        ck_retail = get_latest(nested_idx(card, ['paper', 'cardkingdom', 'retail', foil]))
        tcg_retail =  get_latest(nested_idx(card, ['paper', 'tcgplayer', 'retail', foil]))
        if ck_buy != None and tcg_retail != None and ck_retail >= 4.99 and ck_retail <=100 and ck_buy/tcg_retail > 0.9:
            if uuid in AllIdentifiers:
                prices.append((ck_buy/tcg_retail, ck_buy, tcg_retail, AllIdentifiers[uuid]['name'], AllIdentifiers[uuid]['setCode'], foil, AllIdentifiers[uuid]['number']))
            else:
                print("Card not found %s" % (uuid))

prices = sorted(prices, key=lambda x: (x[1]-x[2]))
for price in prices:
    print(price[4], price[6], price[5], price[3], price[1], price[2], price[0])

"""
f.close()

print("Finished reading card prices....")

prices = []
try:
    with open(files_path+'collection_parsed.csv') as csv_file:
        reader = csv.reader( (line.replace('\0','') for line in csv_file) )

        for row in reader:
            if len(row) < 6:
                continue
            uuid = row[0]
            foil = row[9].lower()
            ck_buy = nested_idx(AllPrices, [uuid, 'paper', 'cardkingdom', 'buylist', foil, date])
            tcg_retail =  nested_idx(AllPrices, [uuid, 'paper', 'tcgplayer', 'retail', foil, date])
            if ck_buy != None and tcg_retail != None and ck_buy/tcg_retail > 0.77 and ck_buy >=1:
                prices.append([uuid, row[4], row[5], ck_buy/tcg_retail, ck_buy, tcg_retail, foil, row[1]])
except:
    pass
prices = sorted(prices, key=lambda x: (x[-1], x[3]))
for price in prices:
    print(price[-1], price[1], price[2],price[4],price[3], price[-2])"""

    

