import json
import pickle
from MTG_Set import *
from Scrape import *
from time import gmtime, strftime

reader = open(b"mtg_sets.obj","rb")

mtg_sets = pickle.load(reader)

sets_to_fetch = [] 
for s in mtg_sets:
    if s.type in ["expansion", "core", "masters", "reprint", "from the vault", "starters", "premium deck", "duel deck", "commander", "planechase", "archenemy", "conspiracy", "masterpiece"]:
        sets_to_fetch.append(s.code)

print "fetching prices for sets: " + str(sets_to_fetch)

current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

prices = {"time":current_time}

outfile = open("raw_price_list/"+current_time+".txt", "w")

for s in sets_to_fetch:
    print "fetching prices for set " + s + "..."
    set_prices = fetch_prices(s, True, False)
    prices[s+"TrueFalse"] = set_prices
    for card in set_prices:
        outfile.write(card[0]+ " "+s+" online nonfoil "+str(card[1])+"\n")
    
    set_prices = fetch_prices(s, True, True)
    prices[s+"TrueTrue"] = set_prices
    for card in set_prices:
        outfile.write(card[0]+ " "+s+" online foil "+str(card[1])+"\n")

    set_prices = fetch_prices(s, False, False)
    prices[s+"FalseFalse"] = set_prices
    for card in set_prices:
        outfile.write(card[0]+ " "+s+" paper nonfoil "+str(card[1])+"\n")

    set_prices = fetch_prices(s, False, True)
    prices[s+"FalseTrue"] = set_prices
    for card in set_prices:
        outfile.write(card[0]+ " "+s+" paper foil "+str(card[1])+"\n")

    print "done fetching set "+s



print "pickling prices..."
filehandler = open(b"raw_price_list/"+current_time+".obj","wb")
pickle.dump(prices,filehandler)
print "done"
