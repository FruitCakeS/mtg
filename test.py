import pickle
from MTG_Set import *

reader = open(b"raw_price_list/2017-08-06 20:22:35.obj","rb")

prices = pickle.load(reader)

out = open("raw_price_list/2017-08-06 20:22:35.txt", "w")
for k in prices.keys():
    if k != "time":
        #print k
        for card in prices[k]:
            out.write(card[0]+ "("+k[0]+") "+str(card[1])+"\n")
        if k[0] == "LEA":
            print prices[k]
