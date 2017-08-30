import json
import pickle
"""
a=1
b=2
c=4

print "pickling..."
filehandler = open(b"pickletest.obj","wb")
pickle.dump(a,filehandler)
pickle.dump(b,filehandler)
pickle.dump(c,filehandler)
print "done"

"""

reader = open(b"pickletest.obj","rb")

a = pickle.load(reader)
b = pickle.load(reader)
c = pickle.load(reader)

print a,b,c