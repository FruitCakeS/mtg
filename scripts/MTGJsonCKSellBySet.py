# Parse through collection and find the best cards to buylist
# Based on high value cards that have not been reprinted for a while

import json
from system_consts import * 
import csv
import pprint
from MTGJsonFetcher import *
import traceback


AllPrintings = read_target('AllPrintings')
AllPrices = read_target('AllPrices')
sets_to_compute = ['MH3']
cards = []
for set_code in sets_to_compute:
    for card in AllPrintings[set_code]['cards']:
        if card['uuid'] not in AllPrices:
            continue
        if card['name'] == 'Wicker Picker':
            print(card['uuid'], AllPrices[card['uuid']])

        tcg_retail =  get_latest(nested_idx(AllPrices[card['uuid']], ['paper', 'tcgplayer', 'retail', 'normal']))
        tcg_retail_foil = get_latest(nested_idx(AllPrices[card['uuid']], ['paper', 'tcgplayer', 'retail', 'foil']))
        ck_buylist = get_latest(nested_idx(AllPrices[card['uuid']], ['paper', 'cardkingdom', 'buylist', 'normal']))
        ck_buylist_foil = get_latest(nested_idx(AllPrices[card['uuid']], ['paper', 'cardkingdom', 'buylist', 'foil']))
        if tcg_retail != None and ck_buylist != None and  (card['rarity'] in ['rare', 'mythic'] or (ck_buylist/tcg_retail > 0.77 and card['rarity'] in ['common', 'uncommon'])):
            cards.append([set_code, card['number'], card['name'], 'normal', tcg_retail, ck_buylist, ck_buylist/tcg_retail, card['rarity']])
        #if tcg_retail_foil != None and ck_buylist_foil:
        #    cards.append([set_code, card['number'], card['name'], 'foil', tcg_retail_foil, ck_buylist_foil, ck_buylist_foil/tcg_retail_foil, card['rarity']])

cards = sorted(cards, key=lambda x:(x[0]+x[7]+str(x[6])))
for card in cards:
    print('%s%s%s%s %s  TCG RETAIL: $%sCK BUYLIST:%sRATIO: %s'%(card[0].ljust(4), card[7].ljust(9), str(card[1]).ljust(5), card[3].ljust(6), card[2].ljust(40) ,str(card[4]).ljust(8),str(card[5]).ljust(8),str(round(card[6], 3)).ljust(8) ))
print("Done.")