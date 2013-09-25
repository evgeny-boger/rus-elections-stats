#!/usr/bin/python
# -*- coding: UTF-8 -*-
import traceback
try:
    import gevent
    from gevent import monkey
    # patches stdlib (including socket and ssl modules) to cooperate with other greenlets
    monkey.patch_all()
    from gevent.pool import Pool
    POOL_SIZE = 1000

    def apply_async(self, func, args = [], kwargs = {}):
        return self.spawn(func, *args, **kwargs)

    Pool.apply_async = apply_async
except ImportError:
    POOL_SIZE = 100

    #~ class Pool(object):
        #~ def __init__(self, size):
            #~ self.size = size
            #~ self.queue = Queue()
            #~
        #~ def spawn(self, func, *args):
            #~ self.queue.put((func, args))
        #~
        #~ def cycle(self):
            #~ while True:
                #~ self.queue.get()
            #~


import urllib, re


regexp_name  = re.compile(r'<td valign="top" width="45%"><b>.*?</b>\s*</td>\s*<td>(.*?)</td>', re.S)


from gevent.timeout import Timeout

def download(url):
	#~ print url
	data = ''
	retries = 0
	timeout = 30.0
	while not data and retries < 30:
		if retries > 0:
			print "retry %d ..."%retries

		try:
			with Timeout(timeout, False):
				data =  urllib.urlopen(url).read().decode('cp1251', 'ignore')
		except:
			data = None
		retries += 1
		timeout *= 1.1

	return data



regexp_subdivisions = re.compile('<option value="(http://.*?)">(.*?)</option>', re.S)
regexp_path = re.compile(r'&gt; <a href=[^>]+>(.*?)</a>')


def get_subdivisions(data):
    return [(url.replace("&amp;", "&"), name) for url, name in  regexp_subdivisions.findall(data)]

#~ regexp_results =   re.compile('<tr bgcolor="#......">\s*<td style="color:black">(\d+)</td>\s*<td style="color:black" align="left">(.*?)</td>\s*<td style="color:black" align="right"><b>(.+?)</b><br></br>\s*(?:\d+\.\d+\%)?\s*</td>\s*</tr>', re.S)
regexp_results =   re.compile('<tr bgcolor="#......">\s*<td style="color:black">(\d+)</td>\s*<td style="color:black" align="left">(.*?)</td>\s*<td style="color:black" align="right"><b>(.+?)</b><br></br>', re.S)

def get_uik_name(data):
    results = regexp_name.findall(data)
    if results:
        return results[0]



field_mapping = {}

import csv,sys

def get_data(data):
	results = regexp_results.findall(data)
	#~ print results
	for field_n, field, value in  results:
		#~ print field_n, field, value
		if not field_n in field_mapping:
			field_mapping[field_n] = field
		else:
			assert field_mapping[field_n] == field

	if results:
#		print len(results)
#		assert  len(results) == 15
		assert len(results) > 9
		return [value for field_n, field, value in  results]



def get_uik_data(uik_url, html):

    #~ html = download(uik_url.replace('type=0', 'type=242'))
    uik_name = get_uik_name(html)
    data = get_data(html)

    path = '/'.join(regexp_path.findall(html))
    print "url: ", url


    if data:
        return [path.encode('utf8'), uik_name.encode('utf8'), uik_url, ] + data


    print 'data', data


def generate_results(results, pool, url,):

    data = download(url.replace('type=0', 'type=242'))
    subdivisions = get_subdivisions(data)

    if subdivisions:
        for subdivision_url, subdivision_name in subdivisions:
            print "process_subdivision",subdivision_name.encode('utf8')

            pool.apply_async(generate_results, (results, pool, subdivision_url))


    else:
        try:
            print "uik found",get_uik_name(data).encode('utf8')
            results.append(get_uik_data(url, data))
        except:
            print "no data for uik"
            traceback.print_exc()

def process_region(url, fname, region):
    csv_file = csv.writer(open(fname, 'wt'))

    pool = Pool(size = POOL_SIZE)

    region_data = download(url)

    results = []
    generate_results(results, pool, url)

    #~ for tik_url, tik_name in get_subdivisions(region_data):
        #~ tik_jobs = [ pool.spawn(get_uik_data, uik_url, uik_name) for uik_url, uik_name in get_subdivisions(download(tik_url))]
        #~
        #~ jobs += tik_jobs
        #~

    print "join"


    pool.join()





    for data in results:
        if data:
            csv_file.writerow([str(region),  ] + data)



mode = sys.argv[1]


if mode == 'regions':
    if len(sys.argv) > 2:
        regions = [int(sys.argv[2]), ]
    else:
        regions =xrange(0,100)

    for region in regions:
        fname = 'results_%s.csv'%(str(region).zfill(2))
        url = 'http://www.khabarovsk.vybory.izbirkom.ru/region/khabarovsk?action=show&global=1&vrn=100100028713299&region=%d&prver=0&pronetvd=null'%region
        url = 'http://www.moscow_reg.vybory.izbirkom.ru/region/moscow_reg?action=show&global=1&vrn=100100031793505&region=%d&prver=0&pronetvd=null'%region
        #~ print url
        process_region(url, fname, region)

elif mode == 'url':
    url = sys.argv[2]
    fname = sys.argv[3]
    process_region(url, fname, 'url')
elif mode =='cont':
    import datetime
    while 1:
        d = datetime.datetime.now()
        prefix = d.strftime('%Y%m%d_%H%M%S') + "_"
        print "Get with prefix", prefix
        if sys.argv[2] == 'all':
            regions = xrange(100)
            prefix = 'all_'
        else:
	    regions = [77,50, 78]
	    prefix = 'regions_'

        prefix +=d.strftime('%Y%m%d_%H%M%S') + "_"
        print "Get with prefix", prefix

        for region in regions:
	    fname = prefix + 'results_%s.csv'%(str(region).zfill(2))
	    url = 'http://www.khabarovsk.vybory.izbirkom.ru/region/khabarovsk?action=show&global=1&vrn=100100028713299&region=%d&prver=0&pronetvd=null'%region
	    url = 'http://www.moscow_reg.vybory.izbirkom.ru/region/moscow_reg?action=show&global=1&vrn=100100031793505&region=%d&prver=0&pronetvd=null' % region

            print url
	    process_region(url, fname, region)

