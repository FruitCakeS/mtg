import json
from system_consts import * 
import csv
#dict_keys(['artist', 'availability', 'borderColor', 'colorIdentity', 'colors', 'convertedManaCost', 'edhrecRank', 'finishes', 'flavorText', 'foreignData', 'frameVersion', 'hasFoil', 'hasNonFoil', 'identifiers', 'isReprint', 'isStarter', 'layout', 'legalities', 'manaCost', 'manaValue', 'name', 'number', 'power', 'printings', 'purchaseUrls', 'rarity', 'rulings', 'setCode', 'signature', 'subtypes', 'supertypes', 'text', 'toughness', 'type', 'types', 'uuid'])


f = open(files_path+'AllIdentifiers.json')
AllIdentifiers = json.load(f)['data']
p_code_exceptions=[]
numbers=[]


cards_to_check = []

for card in AllIdentifiers:
    if AllIdentifiers[card]['setCode'][0] == 'P' and AllIdentifiers[card]['setCode'] not in p_code_exceptions:
        p_code_exceptions.append(AllIdentifiers[card]['setCode'])
    """
    if AllIdentifiers[card]['number'] not in numbers:
        numbers.append(AllIdentifiers[card]['number'])"""

    #if AllIdentifiers[card]['name'] in cards_to_check:
    #    print(AllIdentifiers[card]['name'], AllIdentifiers[card]['number'], AllIdentifiers[card]['setCode'])
f.close()