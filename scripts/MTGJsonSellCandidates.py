# Parse through collection and find the best cards to buylist to Card Kingdom

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
AllPrintings = read_target('AllPrintings')
AllPrices = read_target('AllPrices')
cards = []
try:
    with open(files_path+'collection_parsed.csv') as csv_file:
        reader = csv.reader( (line.replace('\0','') for line in csv_file) )

        for row in reader:
            if len(row) < 6:
                continue
            uuid = row[0]
            foil = row[9].lower()
            card = AllIdentifiers[uuid]
            printings = card['printings']
            latest_edition = None
            latest_release_date = None
            for printing in printings:
                for p_card in AllPrintings[printing]['cards']:
                    if p_card['name'] == card['name']:
                        if latest_release_date == None or latest_release_date < AllPrintings[printing]['releaseDate']:
                            latest_edition = p_card
                            latest_release_date = AllPrintings[printing]['releaseDate']

            if latest_release_date < '2019-01-01' and ('isReserved' not in latest_edition.keys() or not latest_edition['isReserved']):
                tcg_retail =  get_latest(nested_idx(AllPrices, [latest_edition['uuid'], 'paper', 'tcgplayer', 'retail', foil]))
                if tcg_retail == None:
                    tcg_retail =  get_latest(nested_idx(AllPrices, [latest_edition['uuid'], 'paper', 'tcgplayer', 'retail', 'normal']))
                if tcg_retail == None:
                    cards.append([card['name'], latest_release_date, 0])
                else:
                    cards.append([card['name'], latest_release_date, tcg_retail])


except Exception as e:
    print(traceback.format_exc())
cards = sorted(cards, key=lambda x:x[2])
for card in cards:
    print(card)
print("Done.")