import pickle
from MTG_Set import *

reader = open(b"mtg_sets.obj","rb")

mtg_sets = pickle.load(reader)

for s in mtg_sets:
    if s.code == "SOI":
        print s.cards