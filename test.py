import pickle
from MTG_Set import *

reader = open(b"mtg_sets.obj","rb")

mtg_sets = pickle.load(reader)

for s in mtg_sets:
	print s.name
	print "code: " + str(s.code)
	print "mkm_name: " + str(s.mkm_name)
	print "mkm_id: " + str(s.mkm_id)
	print "border: " + str(s.border)
	print "type: " + str(s.type)
	print "magicCardsInfoCode: " + str(s.magicCardsInfoCode)
	print "magicRaritiesCodes: " + str(s.magicRaritiesCodes)
	print "gathererCode: " + str(s.gathererCode)
	print "oldCode: " + str(s.oldCode)
	print "alternativeNames: " + str(s.alternativeNames)
	print "\n\n\n\n"

