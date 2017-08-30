import json
import pickle

old_ids = open("OldCatID.txt", "r").read().split("\n")
cards={}
ids={}
alpha="abcdefghijklmnopqrstuvwxyz "
ae = old_ids[0]
print ae
ALPHA=alpha.upper()
for old_id in old_ids[1:]:
	(rs, rc, nid, fid) = old_id.split("#")
	s=""
	for l in rs.upper():
		if l in ALPHA:
			s+=l
	c=u""
	rc = rc.lower()
	for l in rc:
		if l in alpha:
			c+=l
		else:
			print l
		#print l
		if l == ae[0]:
			c+="ae"
	print rc, s, c
	#if nid != "":
	#	cards[c+" online nonfoil"] = old
