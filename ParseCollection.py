import xml.etree.ElementTree
import pickle
from MTG_Set import *

basics = ["Plains", "Island", "Swamp", "Mountain", "Forest"]

e = xml.etree.ElementTree.parse('collection.dek').getroot()

reader = open(b"mtg_sets.obj","rb")
mtg_sets = pickle.load(reader)
soi_cards = []
for s in mtg_sets:
    if s.code == "SOI":
        soi_cards = s.cards

cards = []
for card in e.findall('Cards'):
    if card.get('Name') not in basics:
        cards.append([card.get('Name'), card.get('CatID'), card.get('Quantity')])

soi_collection = []

for card in cards:
    soi_collection.append(card)

soi_collection = sorted(soi_collection, key=lambda x:int(x[1]))
for card in soi_collection:
    print card