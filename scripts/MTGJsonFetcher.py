# Downloads files from MTGJson and unzips them
# python3 MTGJsonFetcher.py

from system_consts import * 
import urllib.request
from datetime import date
from os.path import exists
import gzip
import shutil
import json
from  MTGJsonSetCodeMapper import set_code_map
import csv

file_targets = ['AllPrices', 'AllIdentifiers', 'AllPrintings']
opened_json = {}

date_today = str(date.today())


def get_filename(target):
	return files_path+target+date_today+'.json'

def read_target(target):
	if not target in file_targets:
		print("file %s doesn't exist!" % (target))
		return None
	if target in opened_json:
		return opened_json[target]
	else:
		update_file(target)
		print("Reading %s..." % (target))
		f = open(get_filename(target))
		json_result = json.load(f)['data']
		f.close()
		print("Finished reading %s..." % (target))
		opened_json[target] = json_result
		return json_result


def update_files():
	for target in file_targets:
		update_file(target)


def update_file(target):
	url_base = 'https://mtgjson.com/api/v5/'

	filename = get_filename(target)+'.gz'

	opener=urllib.request.build_opener()
	opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
	urllib.request.install_opener(opener)

	file_exists = exists(filename)
	if file_exists:
		print('%s already exists!' % (filename))
	else:
		url = url_base+target+'.json.gz'
		print(url)
		"""
		r = requests.get(url, stream=True)
		if r.status_code == 200:
		    with open(filename, 'wb') as f:
		        r.raw.decode_content = True
		        shutil.copyfileobj(r.raw, f)

		"""
		u = urllib.request.urlopen(url)
		f = open(filename, 'wb')
		meta = u.info()
		file_size = int(meta["Content-Length"])
		print("Downloading: %s Bytes: %s" % (filename, file_size))

		file_size_dl = 0
		block_sz = 2097152
		while True:
		    buffer = u.read(block_sz)
		    if not buffer:
		        break

		    file_size_dl += len(buffer)
		    f.write(buffer)
		    status = r"%s: %10d  [%3.2f%%]" % (filename, file_size_dl, file_size_dl * 100. / file_size)
		    status = status + chr(8)*(len(status)+1)
		    print(status)

		f.close()
		print("Completed downloading %s" % (filename))


	unzip_filename = get_filename(target)

	file_exists = exists(unzip_filename)
	if file_exists:
		print('%s already unzipped!' % (unzip_filename))
	else:
		with gzip.open(filename, 'rb') as f_in:
		    with open(unzip_filename, 'wb') as f_out:
		        shutil.copyfileobj(f_in, f_out)
		print("Completed unzipping %s" % (unzip_filename))

#update_files()



def nested_idx(obj, idxes):
    intermediate = obj
    for idx in idxes:
        if idx in intermediate:
            intermediate = intermediate[idx]
        else:
            return None
    return intermediate

def get_latest(prices):
    if prices == None:
        return None
    if date_today in prices:
        return prices[date_today]
    else:
        return None