from random import *

USD_TO_GEM = 20000/100
REPEATS = 1000000


#arena open day 1
ENTRY = 5000	
MAX_WINS = 7
MAX_LOSSES = 3
PRIZE_TABLE = [0,0,0,0,0,1000,2500,5000]





wr = 0.5

total_entry = ENTRY * REPEATS
while wr < 0.8:
	total_winnings = 0
	total_scrub = 0
	total_day2 = 0
	total_draft2 = 0
	total_USD = 0
	total_money = 0
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
		if wins<5:
			total_scrub += 1
		if wins==7:
			total_day2 += 1
			bo3_wins = 0
			for awfaew in range(4):
				match_win = 0
				for faewa in range(3):
					win = random()<wr
					if win:
						match_win+=1
				if match_win >= 2:
					bo3_wins+=1
			total_winnings += [500,1500,2500,0,0][bo3_wins]
			if bo3_wins>=3:
				total_draft2 += 1
				draft_2_wins = 0
				draft_2_losses = 0
				for awfaew in range(4):
					match_win = 0
					match_loss = 0
					for f2aewa in range(3):
						win = random()<wr
						if win:
							match_win+=1
						else:
							match_loss+=1
						if match_win>=2 or match_loss>=2:
							break
					if match_win >= 2:
						draft_2_wins+=1
					else:
						draft_2_losses+=1
					if draft_2_losses>0 and bo3_wins<=3:
						break
					if draft_2_losses>1:
						break
				total_winnings += [5000,15000,500*USD_TO_GEM, 1000*USD_TO_GEM, 2000*USD_TO_GEM][draft_2_wins]
				total_USD += [0,0,500,1000,2000][draft_2_wins]
				if draft_2_wins >=2:
					total_money += 1
	print("At %s win rate expected winnings is %sx entry, %s scrub, %s day2, %s draft2, %s make money, %s expected USD" % (
		str(round(wr,2)).ljust(4,'0'),
		str(round(total_winnings/total_entry,3)).ljust(6),
		str(round(total_scrub/REPEATS,3)).ljust(5),
		str(round(total_day2/REPEATS,3)).ljust(5),
		str(round(total_draft2/REPEATS,3)).ljust(5),
		str(round(total_money/REPEATS,3)).ljust(5),
		str(round(total_USD/REPEATS,3)),
	))
	wr+=0.01