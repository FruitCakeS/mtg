import json
import pickle
from MTG_Set import *
from Scrape import *
from time import gmtime, strftime

reader = open(b"mtg_sets.obj","rb")

mtg_sets = pickle.load(reader)

for s in mtg_sets:
    print "{:>50}{:>10}{:>20}".format(s.name, s.code, s.type)
