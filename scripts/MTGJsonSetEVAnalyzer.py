# Parse through collection and find the best cards to buylist to Card Kingdom
# Based on % value of TCG price

import json
from system_consts import * 
import csv
import pprint
from MTGJsonFetcher import *
import traceback



AllPrintings = read_target('AllPrintings')
AllPrices = read_target('AllPrices')
sets_to_compute = ['OTJ', 'MKM', 'LCI', 'WOE', 'MAT', 'MOM', 'ONE', 'BRO', 'DMU', 'SNC', 'NEO', 'VOW', 'MID', 'AFR', 'STX', 'KHM', 'ZNR', 'RVR','WHO', 'CMM', 'LTR', 'DMR','CLB', 'MH3', 'MH2', 'MH1', '2X2', 'UNF', 'J22', 'BFZ','AER']
boosters_to_compute = [
    'play',
    'default',
    'draft',
    'set',
    'jumpstart',
    'collector',
    'collector-special'
    ]

for booster_type in boosters_to_compute:
    for set_code in sets_to_compute:
        if set_code not in AllPrintings.keys():
            continue
        if 'booster' not in AllPrintings[set_code].keys():
            continue
        if booster_type not in AllPrintings[set_code]['booster'].keys():
            continue
        booster_full = AllPrintings[set_code]['booster'][booster_type]
        weighted_slots = {}
        for booster in booster_full['boosters']:
            for (content,amount) in booster['contents'].items():
                if content not in weighted_slots:
                    weighted_slots[content] = 0
                weighted_slots[content] += amount * booster['weight'] / booster_full['boostersTotalWeight']

        slot_prices_tcg_retail = {}
        slot_prices_ck_buylist = {}
        slot_prices_tcg_retail_non_bulk = {}
        slot_prices_tcg_retail_expensive = {}
        for (sheet, sheet_contents) in booster_full['sheets'].items():
            if sheet not in slot_prices_ck_buylist:
                slot_prices_ck_buylist[sheet] = 0
            if sheet not in slot_prices_tcg_retail:
                slot_prices_tcg_retail[sheet] = 0
            if sheet not in slot_prices_tcg_retail_non_bulk:
                slot_prices_tcg_retail_non_bulk[sheet] = 0
            if sheet not in slot_prices_tcg_retail_expensive:
                slot_prices_tcg_retail_expensive[sheet] = 0
            foil = 'foil' if sheet_contents['foil'] else 'normal'
            totalWeight = sheet_contents['totalWeight']
            for (card,card_weight) in sheet_contents['cards'].items():
                if card not in AllPrices:
                    continue
                tcg_retail = get_latest(nested_idx(AllPrices[card], ['paper', 'tcgplayer', 'retail', foil]))
                #print(card,card_weight, weighted_slots[sheet], tcg_retail, AllPrices[card])
                if tcg_retail != None:
                    slot_prices_tcg_retail[sheet] += tcg_retail * weighted_slots[sheet] * card_weight / totalWeight
                    if tcg_retail >= 1:
                        slot_prices_tcg_retail_non_bulk[sheet] += tcg_retail * weighted_slots[sheet] * card_weight / totalWeight
                    if tcg_retail >= 5:
                        slot_prices_tcg_retail_expensive[sheet] += tcg_retail * weighted_slots[sheet] * card_weight / totalWeight
                ck_buylist = get_latest(nested_idx(AllPrices[card], ['paper', 'cardkingdom', 'buylist', foil]))
                if ck_buylist != None:
                    slot_prices_ck_buylist[sheet] += ck_buylist * weighted_slots[sheet] * card_weight / totalWeight
        print('%s %s:tcg%s, nonbulk%s, valuables%s, ckbuy%s' % (set_code.ljust(4), booster_type.ljust(9), str(round(sum(slot_prices_tcg_retail.values()), 3)).ljust(8), str(round(sum(slot_prices_tcg_retail_non_bulk.values()), 3)).ljust(8), str(round(sum(slot_prices_tcg_retail_expensive.values()), 3)).ljust(8), str(round(sum(slot_prices_ck_buylist.values()), 3)).ljust(8) ))
        #print(slot_prices_ck_buylist, slot_prices_tcg_retail, slot_prices_tcg_retail_expensive, slot_prices_tcg_retail_non_bulk)



show_freshness()




