# Parse through collection and find the best cards to buylist
# Based on high value cards that have not been reprinted for a while

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
set_exceptions = ['PLIST', 'SLD', 'PTK', 'J11', 'J12', 'J13', 'J14', 'J15', 'J16', 'J17', 'J18', 'J19', 'J20', 'ZNE', 'PNAT']
cards = []
card_names = []
try:
    with open(files_path+'collection_parsed.csv') as csv_file:
        reader = csv.reader( (line.replace('\0','') for line in csv_file) )

        for row in reader:
            if len(row) < 6:
                continue
            try:
                uuid = row[0]
                foil = row[9].lower()
                card = AllIdentifiers[uuid]
            except:
                continue
            printings = card['printings']
            latest_edition = None
            latest_release_date = None
            lowest_price = 999999999
            for printing in printings:
                if 'isOnlineOnly' in AllPrintings[printing].keys() and AllPrintings[printing]['isOnlineOnly'] == True:
                    continue
                for p_card in AllPrintings[printing]['cards']:
                    if 'isOversized' in p_card.keys() and p_card['isOversized'] == True:
                        continue
                    if 'legalities' not in p_card.keys() or len(p_card['legalities']) == 0:
                        continue    
                    if p_card['name'] == card['name']:
                        if latest_release_date == None or latest_release_date < AllPrintings[printing]['releaseDate']:
                            if not printing in set_exceptions:
                                latest_edition = p_card
                                latest_release_date = AllPrintings[printing]['releaseDate']

                        tcg_retail =  get_latest(nested_idx(AllPrices, [p_card['uuid'], 'paper', 'tcgplayer', 'retail', 'normal']))
                        tcg_retail_foil =  get_latest(nested_idx(AllPrices, [p_card['uuid'], 'paper', 'tcgplayer', 'retail', 'foil']))
                        if tcg_retail != None and tcg_retail < lowest_price:
                            lowest_price = tcg_retail    
                        if tcg_retail_foil != None and tcg_retail_foil < lowest_price:
                            lowest_price = tcg_retail_foil   
            if latest_release_date is not None and latest_release_date < '2021-01-01' and ('isReserved' not in latest_edition.keys() or not latest_edition['isReserved']):
                if lowest_price < 99999999 and lowest_price > 2 and card['name'] not in card_names:
                    card_names.append(card['name'])
                    cards.append([card['name'], latest_release_date, lowest_price])


except Exception as e:
    print(traceback.format_exc())
cards = sorted(cards, key=lambda x:x[2])
for card in cards:
    print(card)
print("Done.")