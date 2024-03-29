import json
from system_consts import * 
import csv
import pprint
from MTGJsonFetcher import read_target



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


prices = []
try:
    with open(files_path+'collection_parsed.csv') as csv_file:
        reader = csv.reader( (line.replace('\0','') for line in csv_file) )

        for row in reader:
            if len(row) < 6:
                continue
            uuid = row[0]
            foil = row[9].lower()

            ck_buy = get_latest(nested_idx(AllPrices, [uuid, 'paper', 'cardkingdom', 'buylist', foil]))
            tcg_retail =  get_latest(nested_idx(AllPrices, [uuid, 'paper', 'tcgplayer', 'retail', foil, date]))
            print(uuid, ck_buy, tcg_retail)
            if ck_buy != None and tcg_retail != None and ck_buy/tcg_retail > 0.77 and ck_buy >=1:
                prices.append({
                    'uuid': uuid,
                    'folder': row[1],
                    'name': row[4],
                    'set': row[5],
                    'ck_buy': ck_buy,
                    'ratio': ck_buy/tcg_retail,
                    'tcg_retail': tcg_retail,
                    'foil': foil,
                    'types': AllIdentifiers[uuid]['types'] if len( AllIdentifiers[uuid]['types']) == 1 else  [AllIdentifiers[uuid]['types'][0]],
                    'colors': AllIdentifiers[uuid]['colors'] if len( AllIdentifiers[uuid]['colors']) == 1 else ['M'],
                })
except:
    print("!!!")
    pass
prices = sorted(prices, key=lambda x: 1000+x['ck_buy']-x['tcg_retail'])
for price in prices:
    print(price['types'], price['colors'],price['name'], price['set'], price['ck_buy'],str(round(price['ratio']*100, 1))+'%', price['foil'])

print("Done.")