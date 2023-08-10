import json
from system_consts import * 
import csv
import pprint


cards_to_check = [
    "Kozilek, Butcher of Truth",
    "Emrakul, the Aeons Torn",
    "Ulamog, the Infinite Gyre",
]

def nested_idx(obj, idxes):
    intermediate = obj
    for idx in idxes:
        if idx in intermediate:
            intermediate = intermediate[idx]
        else:
            return None
    return intermediate



f = open(files_path+'AllPrices.json')

AllPrices = json.load(f)

date = AllPrices['meta']['date']
AllPrices=AllPrices['data']
f.close()
print("Finished reading card prices....")

f = open(files_path+'AllIdentifiers.json')
AllIdentifiers = json.load(f)['data']

for card in AllIdentifiers:
    if AllIdentifiers[card]['name'] in cards_to_check:
        for foil in ['normal', 'foil']:
            print(AllIdentifiers[card]['name'], 
                AllIdentifiers[card]['number'], 
                AllIdentifiers[card]['setCode'], 
                foil,
                nested_idx(AllPrices, [card, 'paper', 'cardkingdom', 'buylist', foil]),
            )


f.close()

print("Finished reading card identifiers....")