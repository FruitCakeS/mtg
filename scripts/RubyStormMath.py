cards = {
	'lands_untapped':17,
	'lands_tapped':2,
	'impulse':8,
	'ritual':8,
	'manamorphose':4,
	'glimpse':4,
	'ruby':8,
	'strike': 4,
	'other':5,
}

for card in cards.keys():
	print('%s %s'%(cards[card], card))
print('%s total cards' % sum([cards[card] for card in cards.keys()]))

num_simulations = 1000000
from random import *
deck = []
for card in cards:
	for i in range(cards[card]):
		deck.append(card)
results={
	'turn_2_safe':0,
	'turn_2_missing_land':0,
	'turn_2_missing_12_hits':0,
	'turn_2_missing_8_hits':0,
	'turn_2_missing_land_with_strike':0,
	'turn_2_missing_12_hits_with_strike':0,
	'turn_2_missing_8_hits_with_strike':0,
	'turn_3_great':0,
	'turn_3_safe':0,
	'turn_3_keepable':0,
	'turn_3_keepable_on_mulligan':0,
}
for awjfeoiwja in range(num_simulations):
	shuffle(deck)
	hand = deck[:7]
	if hand.count('lands_tapped') + hand.count('lands_untapped') >= 2 and hand.count('lands_untapped') >=1 and hand.count('impulse') >=1 and hand.count('ritual') + hand.count('strike') >=1 and hand.count('ritual') + hand.count('manamorphose') +hand.count('strike') >=2 and hand.count('ritual') + hand.count('manamorphose') >= 1 and hand.count('ruby') >=1:
		results['turn_2_safe'] +=1
	elif hand.count('lands_tapped') + hand.count('lands_untapped') == 1 and hand.count('impulse') >=1 and hand.count('ritual') + hand.count('strike') >=1 and hand.count('ritual') + hand.count('manamorphose') +hand.count('strike') >=2 and hand.count('ritual') + hand.count('manamorphose') >= 1 and hand.count('ruby') >=1:
		#missing land
		if hand.count('strike') >= 1 and hand.count('ritual') + hand.count('manamorphose') == 1:
			results['turn_2_missing_land_with_strike'] +=1
		else:
			results['turn_2_missing_land'] +=1

	elif hand.count('lands_tapped') + hand.count('lands_untapped') >= 2 and hand.count('lands_untapped') >=1 and hand.count('impulse') == 0 and hand.count('ritual') + hand.count('strike') >=1 and hand.count('ritual') + hand.count('manamorphose') +hand.count('strike') >=2 and hand.count('ritual') + hand.count('manamorphose') >= 1 and hand.count('ruby') >=1:
		#missing impulse
		if hand.count('strike') >= 1 and hand.count('ritual') + hand.count('manamorphose') == 1:
			results['turn_2_missing_8_hits_with_strike'] +=1
		else:
			results['turn_2_missing_8_hits'] +=1
	elif hand.count('lands_tapped') + hand.count('lands_untapped') >= 2 and hand.count('lands_untapped') >=1 and hand.count('impulse') >= 1 and hand.count('ritual') + hand.count('strike') == 0 and hand.count('manamorphose') >= 1 and hand.count('ruby') >=1:
		#missing 1st ritual
		results['turn_2_missing_8_hits'] +=1
	elif hand.count('lands_tapped') + hand.count('lands_untapped') >= 2 and hand.count('lands_untapped') >=1 and hand.count('impulse') >=1 and hand.count('ritual') + hand.count('strike') >=1 and hand.count('ritual') + hand.count('manamorphose') +hand.count('strike') >=2 and hand.count('ritual') + hand.count('manamorphose') >= 1 and hand.count('ruby') ==0:
		#missing ruby
		if hand.count('strike') >= 1 and hand.count('ritual') + hand.count('manamorphose') == 1:
			results['turn_2_missing_8_hits_with_strike'] +=1
		else:
			results['turn_2_missing_8_hits'] +=1
	elif hand.count('lands_tapped') + hand.count('lands_untapped') >= 2 and hand.count('lands_untapped') >=1 and hand.count('impulse') >=1 and (hand.count('ritual') + hand.count('strike') == 1 or (hand.count('ritual') == 0 and hand.count('strike') >=1)) and hand.count('manamorphose') == 0 and hand.count('ruby') >=1:
		#missing 2nd ritual
		if hand.count('strike') >= 1:
			results['turn_2_missing_12_hits_with_strike'] +=1
		else:
			results['turn_2_missing_12_hits'] +=1
	if hand.count('lands_tapped') + hand.count('lands_untapped') >= 2 and hand.count('lands_untapped') >=1 and hand.count('impulse') >=1 and hand.count('ruby') >=1 and hand.count('ritual') + hand.count('impulse') + hand.count('glimpse') + hand.count('manamorphose') >=2:
		results['turn_3_great'] +=1
	if hand.count('lands_tapped') + hand.count('lands_untapped') >= 2 and hand.count('lands_untapped') >=1 and hand.count('ruby') >=1 and hand.count('ritual') + hand.count('impulse') + hand.count('glimpse') + hand.count('manamorphose') >=2:
		results['turn_3_safe'] +=1
	if hand.count('lands_tapped') + hand.count('lands_untapped') >= 1 and hand.count('ruby') + hand.count('ritual') + hand.count('impulse') + hand.count('glimpse') + hand.count('manamorphose') >=3:
		results['turn_3_keepable'] +=1
	if hand.count('lands_tapped') + hand.count('lands_untapped') >= 1 and hand.count('ruby') + hand.count('ritual') + hand.count('impulse') + hand.count('glimpse') + hand.count('manamorphose') >=2:
		results['turn_3_keepable_on_mulligan'] +=1

for result in results.keys():
	print('%s %s' % (str(float(results[result])*100/num_simulations)+'%', result))