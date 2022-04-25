import urllib.request
from datetime import date
from os.path import exists



url_base = 'https://mtgjson.com/api/v5/'
appendix = '.json.gz'

target = 'AllPrices'

filename = target+str(date.today())+appendix

file_exists = exists('./'+filename)
if not file_exists:
	url = url_base+target+appendix
	print('url: '+url)
	u = urllib.request.urlopen(url)
	f = open(filename, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print("Downloading: %s Bytes: %s" % (filename, file_size))

	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print(status)

	f.close()
	print("Completed")