import json
from system_consts import * 
from  MTGJsonSetCodeMapper import p_code_exceptions
import csv
#dict_keys(['artist', 'availability', 'borderColor', 'colorIdentity', 'colors', 'convertedManaCost', 'edhrecRank', 'finishes', 'flavorText', 'foreignData', 'frameVersion', 'hasFoil', 'hasNonFoil', 'identifiers', 'isReprint', 'isStarter', 'layout', 'legalities', 'manaCost', 'manaValue', 'name', 'number', 'power', 'printings', 'purchaseUrls', 'rarity', 'rulings', 'setCode', 'signature', 'subtypes', 'supertypes', 'text', 'toughness', 'type', 'types', 'uuid'])

def customParse(line):
    return line.replace('\0','')


f = open(files_path+'AllIdentifiers.json')
AllIdentifiers = json.load(f)['data']

f.close()


with open(files_path+'collection_parsed.csv', mode='w') as csv_write:
    csv_writer = csv.writer(csv_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    ct=0
    with open(files_path+'collection.csv', encoding='latin-1') as csv_file:
        csv_file_fixed = (customParse(line) for line in csv_file)
        reader = csv.reader(csv_file_fixed)

        for row in reader:
            try:
                if len(row) < 6:
                    continue
                new_row = [""]+row
                name = row[3]
                setCode = row[4]
                if setCode[0] == 'P' and setCode not in p_code_exceptions:
                    setCode = setCode[1:]

                number = row[6]
                number = ''.join(filter(str.isdigit, number))
                for card in AllIdentifiers:
                    if AllIdentifiers[card]['name'] == name and AllIdentifiers[card]['setCode'] == setCode and AllIdentifiers[card]['number'] == number:
                        new_row[0] = card
                        #print('Card added: ' + name)
                if new_row[0] == "":
                    print("Card not found ", ct, name, setCode, number)
                #else:
                #   print(ct, name, setCode)
                csv_writer.writerow(new_row)
                ct+=1
            except Exception as e:
                print(e)
                continue

