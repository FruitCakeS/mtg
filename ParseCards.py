import json
import pickle
from MTG_Set import *

#with open("AllCards-x.json") as f:
#    cards = json.load(f)

#print len(cards.keys())
#print json.dumps(cards["Tezzeret the Schemer"], sort_keys=True, indent=4, separators=(',', ': '))
#print cards.keys()

with open("AllSets-x.json") as f:
    sets = json.load(f)

#print len(sets.keys())
#print json.dumps(sets['AER'], sort_keys=True, indent=4, separators=(',', ': '))

mtg_sets = []
for key in sets.keys():
	mtg_sets.append(MTG_Set(sets[key]))


print "pickling sets..."
filehandler = open(b"mtg_sets.obj","wb")
pickle.dump(mtg_sets,filehandler)
print "done"

