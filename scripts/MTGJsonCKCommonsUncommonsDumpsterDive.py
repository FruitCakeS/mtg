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
sets_to_compute = ['ZEN', 'WWK', 'ROE', 'SOM', 'MBS', 'NPH', 'ISD', 'DKA', 'AVR', 'M11', 'M12', 'M13', 'RTR', 'GTC', 'KTK', 'FRF', 'DTK', 'SOI', 'KHM', 'STX' ,'AFR', 'MID', 'VOW', 'NEO', 'SNC', 'BRO', 'ONE', 'MOM', 'MAT', 'WOE', 'LCI', 'MH2', '2X2', 'LTR', 'MMA', 'EMA', 'UMA', 'JMP', 'M20']
cards = []
for set_code in sets_to_compute:
    for card in AllPrintings[set_code]['cards']:
        if card['uuid'] not in AllPrices:
            continue
        if card['rarity'] in ['rare', 'mythic']:
            continue
        if card['name'] == 'Wicker Picker':
            print(card['uuid'], AllPrices[card['uuid']])

        tcg_retail =  get_latest(nested_idx(AllPrices[card['uuid']], ['paper', 'tcgplayer', 'retail', 'normal']))
        ck_buylist = get_latest(nested_idx(AllPrices[card['uuid']], ['paper', 'cardkingdom', 'buylist', 'normal']))
        if tcg_retail != None and ck_buylist != None and ck_buylist/tcg_retail > 0.8:
            cards.append([set_code, card['number'], card['name'], 'normal', tcg_retail, ck_buylist, ck_buylist/tcg_retail, card['rarity']])

cards = sorted(cards, key=lambda x:(str(sets_to_compute.index(x[0])).rjust(3,'0')+x[7]+str(x[6])))
for card in cards:
    print('%s%s%s%s %s  TCG RETAIL: $%sCK BUYLIST:%sRATIO: %s'%(card[0].ljust(4), card[7].ljust(9), str(card[1]).ljust(5), card[3].ljust(6), card[2].ljust(30) ,str(card[4]).ljust(8),str(card[5]).ljust(8),str(round(card[6], 3)).ljust(8) ))
print("Done.")