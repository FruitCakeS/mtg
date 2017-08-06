import urllib
url = "http://stackoverflow.com"
f = urllib.urlopen(url)
print f.read()