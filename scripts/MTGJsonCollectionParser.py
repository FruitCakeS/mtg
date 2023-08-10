import json
from system_consts import * 
from  MTGJsonSetCodeMapper import set_code_map
import csv
from MTGJsonFetcher import read_target
import traceback


#dict_keys(['artist', 'availability', 'borderColor', 'colorIdentity', 'colors', 'convertedManaCost', 'edhrecRank', 'finishes', 'flavorText', 'foreignData', 'frameVersion', 'hasFoil', 'hasNonFoil', 'identifiers', 'isReprint', 'isStarter', 'layout', 'legalities', 'manaCost', 'manaValue', 'name', 'number', 'power', 'printings', 'purchaseUrls', 'rarity', 'rulings', 'setCode', 'signature', 'subtypes', 'supertypes', 'text', 'toughness', 'type', 'types', 'uuid'])
def customParse(line):
    return line.replace('\0','')

#AllIdentifiers = read_target('AllIdentifiers')
AllPrintings = read_target('AllPrintings')


with open(files_path+'collection_parsed.csv', mode='w') as csv_write:
    csv_writer = csv.writer(csv_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    ct=0
    with open(files_path+'collection.csv', encoding='latin-1') as csv_file:
        csv_length = sum(1 for line in csv_file)
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
                if setCode in set_code_map:
                    setCode = set_code_map[setCode]
                number = row[6]
                number = ''.join(filter(str.isdigit, number))
                printing = AllPrintings[setCode]['cards']
                for idx, card in enumerate(printing):
                    c_number = card['number']
                    c_number = ''.join(filter(str.isdigit, c_number))
                    if card['name'] == name and c_number == number:
                        new_row[0] = card['uuid']
                        #print('Card added: ' + name)
                        break
                    elif c_number == number:
                        new_row[0] = card['uuid']
                        print('Fuzzy Card added: %s added as %s. Set code: %s number %s vs %s' % (name, card['name'], str(setCode), str(number), str(c_number)))
                        #print(idx, printing[idx]['name'], printing[idx]['number'])
                        break
                if new_row[0] == "":
                    print("Card not found ", ct, name, setCode, number)
                #else:
                #   print(ct, name, setCode)
                csv_writer.writerow(new_row)
                ct+=1
                if ct%100 == 0:
                    print('parsed '+str(ct)+' of ' +str(csv_length) +' rows...')
            except Exception as e:
                print(traceback.format_exc())
                continue

print("Done.")