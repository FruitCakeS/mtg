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
set_values = {}
set_values['overall'] = {}
set_values['overall']['ck_buy_total'] = 0
set_values['overall']['ck_retail_total'] = 0
set_values['overall']['tcg_retail_total'] = 0
set_values['overall']['ck_retail_buylist_total'] = 0
set_values['overall']['tcg_retail_buylist_total'] = 0
set_values['overall']['release'] = ''
set_values['overall']['type'] = ''

for set_code in AllPrintings.keys():
    #if set_code != 'MH2':
        #continue
    if AllPrintings[set_code]['isOnlineOnly']:
        continue
    set_type = AllPrintings[set_code]['type']
    year = AllPrintings[set_code]['releaseDate'][:4]
    set_values[set_code] = {}
    set_values[set_code]['ck_buy_total'] = 0
    set_values[set_code]['ck_retail_total'] = 0
    set_values[set_code]['tcg_retail_total'] = 0
    set_values[set_code]['ck_retail_buylist_total'] = 0
    set_values[set_code]['tcg_retail_buylist_total'] = 0
    set_values[set_code]['release'] = AllPrintings[set_code]['releaseDate']
    set_values[set_code]['type'] = set_type
    if set_type not in set_values:
        set_values[set_type] = {}
        set_values[set_type]['ck_buy_total'] = 0
        set_values[set_type]['ck_retail_total'] = 0
        set_values[set_type]['tcg_retail_total'] = 0
        set_values[set_type]['ck_retail_buylist_total'] = 0
        set_values[set_type]['tcg_retail_buylist_total'] = 0
        set_values[set_type]['release'] = ''
        set_values[set_type]['type'] = ''
    if year not in set_values:
        set_values[year] = {}
        set_values[year]['ck_buy_total'] = 0
        set_values[year]['ck_retail_total'] = 0
        set_values[year]['tcg_retail_total'] = 0
        set_values[year]['ck_retail_buylist_total'] = 0
        set_values[year]['tcg_retail_buylist_total'] = 0
        set_values[year]['release'] = ''
        set_values[year]['type'] = ''


    for card in AllPrintings[set_code]['cards']:
        uuid=card['uuid']
        for foil in ['foil', 'nonfoil']:
            if uuid not in AllPrices:
                continue
            ck_buylist = get_latest(nested_idx(AllPrices[uuid], ['paper', 'cardkingdom', 'buylist', foil])) 
            ck_retail = get_latest(nested_idx(AllPrices[uuid], ['paper', 'cardkingdom', 'retail', foil])) 
            tcg_retail = get_latest(nested_idx(AllPrices[uuid], ['paper', 'tcgplayer', 'retail', foil]))
            if ck_retail != None and tcg_retail != None and ck_retail >=0.3:
                if ck_buylist != None:
                    set_values[set_code]['ck_buy_total'] += ck_buylist
                    set_values['overall']['ck_buy_total'] += ck_buylist
                    set_values[set_type]['ck_buy_total'] += ck_buylist
                    set_values[year]['ck_buy_total'] += ck_buylist
                    set_values[set_code]['ck_retail_buylist_total'] += ck_retail
                    set_values['overall']['ck_retail_buylist_total'] += ck_retail
                    set_values[set_type]['ck_retail_buylist_total'] += ck_retail
                    set_values[year]['ck_retail_buylist_total'] += ck_retail
                    set_values[set_code]['tcg_retail_buylist_total'] += tcg_retail
                    set_values['overall']['tcg_retail_buylist_total'] += tcg_retail
                    set_values[set_type]['tcg_retail_buylist_total'] += tcg_retail
                    set_values[year]['tcg_retail_buylist_total'] += tcg_retail

                set_values[set_code]['ck_retail_total'] += ck_retail
                set_values[set_code]['tcg_retail_total'] += tcg_retail
                set_values[set_type]['ck_retail_total'] += ck_retail
                set_values[set_type]['tcg_retail_total'] += tcg_retail
                set_values[year]['ck_retail_total'] += ck_retail
                set_values[year]['tcg_retail_total'] += tcg_retail
                set_values['overall']['ck_retail_total'] += ck_retail
                set_values['overall']['tcg_retail_total'] += tcg_retail
                #print(card['name'].ljust(50), str(ck_buylist).ljust(10), str(ck_retail).ljust(10), set_values[set_code]['ck_buy_total'], set_values[set_code]['ck_retail_total'])


list_of_sets = set_values.keys()
list_of_sets = sorted(list_of_sets, key=lambda x:(set_values[x]['type'],set_values[x]['release'], x))
list_of_sets = ['overall']+list_of_sets

for set_code in list_of_sets:
    if set_values[set_code]['tcg_retail_total'] == 0 and set_values[set_code]['tcg_retail_buylist_total'] == 0 and set_values[set_code]['ck_retail_buylist_total'] ==0:
        continue
    print('%s %s %s ck_retail/tcg_retail:%s ck_buylist/tcg_retail:%s ck_buylist/ck_retail:%s weight:%s' % (
        set_code.ljust(16),
        set_values[set_code]['release'].ljust(10),
        set_values[set_code]['type'].ljust(20),
        (str(round(set_values[set_code]['ck_retail_total']/set_values[set_code]['tcg_retail_total']*100,2))+'%').ljust(16) if set_values[set_code]['tcg_retail_total'] != 0 else 'NaN'.ljust(16),
        (str(round(set_values[set_code]['ck_buy_total']/set_values[set_code]['tcg_retail_buylist_total']*100,2))+'%').ljust(16) if set_values[set_code]['tcg_retail_buylist_total'] != 0 else 'NaN'.ljust(16),
        (str(round(set_values[set_code]['ck_buy_total']/set_values[set_code]['ck_retail_buylist_total']*100,2))+'%').ljust(16) if set_values[set_code]['ck_retail_buylist_total'] != 0 else 'NaN'.ljust(16),
        (str(round(set_values[set_code]['tcg_retail_total']/set_values['overall']['tcg_retail_total']*100,2))+'%').ljust(16),
    ))










