from random import *

USD_TO_GEM = 20000/100
REPEATS = 100000

#festival in a box
ENTRY = 5000
MAX_WINS = 6
MAX_LOSSES = 1
PRIZE_TABLE = [0,0,0,0,2000,5000,200*USD_TO_GEM]
"""
#premier draft
ENTRY = 1500
MAX_WINS = 7
MAX_LOSSES = 3
PRIZE_TABLE = [50,100,250,1000,1400,1600,1800,2200]

#arena open
ENTRY = 5000	
MAX_WINS = 7
MAX_LOSSES = 3
PRIZE_TABLE = [0,0,0,0,0,1000,2500,5000+2500]
"""






wr = 0.5

total_entry = ENTRY * REPEATS
while wr < 0.8:
	total_winnings = 0
	for iefjaowiefj in range(REPEATS):
		losses = 0
		wins = 0
		while losses<MAX_LOSSES and wins<MAX_WINS:
			win = random() < wr
			if win:
				wins+=1
			else:
				losses+=1
		total_winnings+=PRIZE_TABLE[wins]
	print("At %s win rate expected winnings is %sx entry" % (str(round(wr,2)).ljust(4,'0'), str(round(total_winnings/total_entry,3))))
	wr+=0.01