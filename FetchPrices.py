import json
import pickle
from MTG_Set import *
from Scrape import *
from time import gmtime, strftime

reader = open(b"mtg_sets.obj","rb")

mtg_sets = pickle.load(reader)

try:
    reader = open(b"mtg_sets_count.meta","rb")
    mtg_sets_count = pickle.load(reader)
except:
    mtg_sets_count = {}

sets_to_fetch = ["PZ1","PZ2"]
for s in mtg_sets:
    if s.type in ["expansion", "core", "masters", "reprint", "from the vault", "starters", "premium deck", "duel deck", "commander", "planechase", "archenemy", "conspiracy", "masterpiece"]:
        sets_to_fetch.append(s.code)

print "fetching prices for sets: " + str(sets_to_fetch)

current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

prices = {"time":current_time}

outfile = open("raw_price_list/"+current_time+".txt", "w")

set_count = 0
for s in sets_to_fetch:
    set_count += 1
    print "fetching prices for set " + s + "... (set "+str(set_count)+" of "+str(len(sets_to_fetch))+")"
    for (k, online, foil) in [
        (s+" online nonfoil", True, False),
        (s+" online foil", True, True),
        (s+" paper nonfoil", False, False),
        (s+" paper foil", False, True)]:

        expected_count = 0
        if k in mtg_sets_count.keys():
            expected_count = mtg_sets_count[k]
            if k+" exists" in mtg_sets_count.keys() and mtg_sets_count[k+" exists"] == 0:
                continue

        retries = 3
        set_prices = []
        actual_count = 0
        while retries>0:
            retries -= 1
            set_prices = fetch_prices(s, online, foil)
            actual_count = len(set_prices)
            if (actual_count >= expected_count):
                break

        prices[k] = set_prices
        for card in set_prices:
            outfile.write(card[0]+ " "+k+" "+str(card[1])+"\n")

        
        print k+" expected "+str(expected_count)+" cards got "+str(actual_count)+" cards"

        mtg_sets_count[k] = max(expected_count,actual_count)
        if (expected_count == 0 and actual_count == 0):
            mtg_sets_count[k+" exists"] = 0
        else:
            mtg_sets_count[k+" exists"] = 1


    print "done fetching set "+s



print "pickling prices..."
filehandler = open(b"raw_price_list/"+current_time+".obj","wb")
pickle.dump(prices,filehandler)
print "done"

print "pickling counts..."
filehandler = open(b"mtg_sets_count.meta","wb")
pickle.dump(mtg_sets_count,filehandler)
print "done"
