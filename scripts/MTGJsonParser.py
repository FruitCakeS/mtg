import json
from system_consts import * 
import csv
import pprint


def nested_idx(obj, idxes):
    intermediate = obj
    for idx in idxes:
        if idx in intermediate:
            intermediate = intermediate[idx]
        else:
            return None
    return intermediate


"""

f = open(files_path+'AllIdentifiers.json')
AllIdentifiers = json.load(f)['data']
f.close()

print("Finished reading card identifiers....")
"""
f = open(files_path+'AllPrices.json')

AllPrices = json.load(f)

date = AllPrices['meta']['date']
AllPrices=AllPrices['data']
"""
total = len(data)
count = 0

for uuid, card in data.items():
    if (count % 1000 == 0):
        print('parsing '+str(count)+' of '+str(total)+' prices...')
    count+=1
    ck_buy = nested_idx(card, ['paper', 'cardkingdom', 'buylist', 'normal', date])
    tcg_retail =  nested_idx(card, ['paper', 'tcgplayer', 'retail', 'normal', date])
    if ck_buy != None and tcg_retail != None and ck_buy/tcg_retail > 0.9 and ck_buy >=1:
        print(uuid, ck_buy, tcg_retail, AllIdentifiers[uuid]['name'],AllIdentifiers[uuid]['setCode'])
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
            ck_buy = nested_idx(AllPrices, [uuid, 'paper', 'cardkingdom', 'buylist', 'normal', date])
            tcg_retail =  nested_idx(AllPrices, [uuid, 'paper', 'tcgplayer', 'retail', 'normal', date])
            if ck_buy != None and tcg_retail != None and ck_buy/tcg_retail > 0.7 and ck_buy >=1:
                prices.append([uuid, row[4], row[5], ck_buy/tcg_retail, ck_buy, tcg_retail, row[1]])
except:
    pass
prices = sorted(prices, key=lambda x: (x[-1], x[3]))
for price in prices:
    print(price[-1], price[1], price[2],price[4],price[3])

