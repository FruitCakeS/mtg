import json
from system_consts import * 
import csv
import pprint

target_sets = []

def nested_idx(obj, idxes):
    intermediate = obj
    for idx in idxes:
        if idx in intermediate:
            intermediate = intermediate[idx]
        else:
            return None
    return intermediate



f = open(files_path+'AllIdentifiers.json')
AllIdentifiers = json.load(f)['data']
f.close()

print("Finished reading card identifiers....")

f = open(files_path+'AllPrices.json')

AllPrices = json.load(f)

date = AllPrices['meta']['date']
AllPrices=AllPrices['data']
total = len(AllPrices)
count = 0
prices=[]
for uuid, card in AllPrices.items():
    if (count % 1000 == 0):
        print('parsing '+str(count)+' of '+str(total)+' prices...')
    count+=1
    for foil in ['normal', 'foil']:
        ck_buy = None
        tcg_retail = None
        ck_retail = None
        ck_buy = nested_idx(card, ['paper', 'cardkingdom', 'buylist', foil, date])
        ck_retail = nested_idx(card, ['paper', 'cardkingdom', 'retail', foil, date])
        tcg_retail =  nested_idx(card, ['paper', 'tcgplayer', 'retail', foil, date])
        if ck_buy != None and tcg_retail != None and ck_retail >= 4.99 and ck_retail <=100:
            prices.append((ck_retail/tcg_retail, ck_retail, tcg_retail, AllIdentifiers[uuid]['name'], AllIdentifiers[uuid]['setCode'], foil, AllIdentifiers[uuid]['number']))

prices = sorted(prices, key=lambda x: (x[1]-x[2]))
for price in prices:
    print(price[4], price[6], price[5], price[3], price[1], price[0])

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

    

