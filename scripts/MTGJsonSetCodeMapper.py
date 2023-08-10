import json
from system_consts import * 
import csv


f = open(files_path+'AllIdentifiers.json')
AllIdentifiers = json.load(f)['data']
p_code_exceptions=[]
numbers=[]


set_code_map = {
    'PSLD': 'SLD',
}


cards_to_check = [
    #'Wall of Blossoms'
]

for card in AllIdentifiers:
    if AllIdentifiers[card]['setCode'][0] == 'P' and AllIdentifiers[card]['setCode'] not in p_code_exceptions:
        p_code_exceptions.append(AllIdentifiers[card]['setCode'])
    """
    if AllIdentifiers[card]['number'] not in numbers:
        numbers.append(AllIdentifiers[card]['number'])"""

    if AllIdentifiers[card]['name'] in cards_to_check:
        print(AllIdentifiers[card]['name'], AllIdentifiers[card]['number'], AllIdentifiers[card]['setCode'])

    #if AllIdentifiers[card]['setCode'] == 'PM20':
    #   print(AllIdentifiers[card]['name'], AllIdentifiers[card]['number'], AllIdentifiers[card]['setCode'])
f.close()
