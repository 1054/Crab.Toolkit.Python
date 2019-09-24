#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 

import os, sys
import sys

if sys.version_info[0] <= 2:
    # Python 2.6-2.7 
    from BeautifulSoup import BeautifulSoup ## for now we are still using BS3
    from urllib2 import urlopen
    from HTMLParser import HTMLParser
    html_parser = HTMLParser()
else:
    # Python 3
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    #from html.parser import HTMLParser
    import html as html_parser

if sys.version_info[0] <= 2:
    reload(sys) # reload sys so that we can setdefaultencoding (but only for Python2)
    sys.setdefaultencoding("UTF-8")
    #print(sys.getdefaultencoding())
elif sys.version_info[0] == 3 and sys.version_info[1] <= 3:
    import imp
    imp.reload(sys)
    #sys.setdefaultencoding("UTF-8")
    #print(sys.getdefaultencoding())
else:
    import importlib
    importlib.reload(sys)
    #sys.setdefaultencoding("UTF-8")
    #print(sys.getdefaultencoding())
    # Python 3 has no sys.setdefaultencoding() function. 
    # It cannot be reinstated by reload(sys) like it can on Python 2 (which you really shouldn't do in any case).

import requests
import re
import numpy
import numpy.lib.recfunctions as rec
import astropy
from datetime import datetime
from termcolor import colored # https://stackoverflow.com/questions/37340049/how-do-i-print-colored-output-to-the-terminal-in-python



RED     = u"\033[1;31m"  
BLUE    = u"\033[1;34m"
CYAN    = u"\033[1;36m"
GREEN   = u"\033[0;32m"
BOLD    = u"\033[;1m"
REVERSE = u"\033[;7m"
RESET   = u"\033[0;0m"





if len(sys.argv) <= 1:
    print('Usage: crabhttp_adsabstract.py "2016ApJS..224...24L" "Output_dir"')
    sys.exit()


# 
# define functions
# 
def check_bibcode(bibcode):
    if type(bibcode) is not str:
        return False
    if len(bibcode) != len('2016ApJS..224...24L'):
        return False
    return True


# 
# Read bibcode
# 
bibtype = 'abs'
bibcode = sys.argv[1]
if not check_bibcode(bibcode):
    bibtype = 'doi'


# 
# Read outdir
# 
outdir = ''
if len(sys.argv) > 2:
    outdir = sys.argv[2]
    if not outdir.endswith(os.sep):
        outdir = outdir + os.sep
    if not os.path.isdir(outdir):
        os.makedirs(outdir)


# 
# Read web page
# 
url = 'http://adsabs.harvard.edu/%s/%s'%(bibtype, bibcode)
response = urlopen(url)
#print response.info()
content = response.read()
response.close()  # best practice to close the file


# 
# Parse web page
# 
soup = BeautifulSoup(content, "lxml")
#print(soup.prettify())


# 
# Get ads_authors
# 
ads_authors = []
for a in soup.findAll('a', href=True):
    if a['href'].find('author_form') > 0:
        ads_authors.append(html_parser.unescape(a.text.strip()))

#print(colored('[Authors]', 'red', attrs=['reverse', 'blink']))
print(colored('[Authors]', 'red', attrs=['reverse']))
for ads_author in ads_authors:
    #sys.stdout.buffer.write(ads_author.encode('utf8'))
    sys.stdout.buffer.write(ads_author.split(',')[1].strip().encode('utf8'))
    sys.stdout.buffer.write(' '.encode('utf8'))
    sys.stdout.buffer.write(RED.encode('utf8'))
    sys.stdout.buffer.write(ads_author.split(',')[0].strip().encode('utf8'))
    sys.stdout.buffer.write(RESET.encode('utf8'))
    sys.stdout.buffer.write('\n'.encode('utf8'))

with open(outdir+'authors','w') as fp:
    for ads_author in ads_authors:
        fp.write(ads_author.split(',')[1].strip() + ' ' + ads_author.split(',')[0].strip() + '\n')
    fp.close()

# 
# Get ads_abstract
# 
ads_abstract = ''
for a in soup.findAll('h3'):
    if a.text.strip() == 'Abstract':
        while True:
            a = a.next_sibling
            #print(a.name, a)
            if a.name == 'hr' or a.name == 'table':
                break
            if a.name == None:
                ads_abstract = ads_abstract + a
            else:
                ads_abstract = ads_abstract + a.text
        #ads_abstract.append(html_parser.unescape(a.text.strip()))
print('')
print(colored('[Abstract]', 'green', attrs=['reverse']))
print(ads_abstract)
with open(outdir+'abstract','w') as fp:
    fp.write(ads_abstract)
    fp.close()

# 
# Get ads_online_data
# 
ads_online_data_url = ''
for a in soup.findAll('a', href=True):
    if a.text.strip() == 'On-line Data':
        ads_online_data_url = a['href']
print('')
print(colored('[OnlineData]', 'blue', attrs=['reverse']))
print(ads_online_data_url)
with open(outdir+'onlinedata','w') as fp:
    fp.write(ads_online_data_url)
    fp.close()








# 
# Read online-data web page and find VizieR Catalogue Service (CDS) link
# 
response = urlopen(ads_online_data_url)
#print response.info()
content = response.read()
response.close()  # best practice to close the file

soup_od = BeautifulSoup(content, "lxml")

cds_redirect_url = ''
for a in soup_od.findAll('a', href=True):
    if a.text.strip() == 'VizieR Catalogue Service':
        cds_redirect_url = a['href']
print('')
print(colored('[VizieR_Catalogue_URL]', 'blue', attrs=['reverse']))
print(cds_redirect_url)

cds_code = ''
response = urlopen(cds_redirect_url)
#print(response.url)
cds_code = response.url
if cds_code != '':
    cds_code = re.search('.*source=([a-zA-Z0-9/+-]+)$', cds_code).group(1)
#print(cds_code)
cds_data_url = 'http://vizier.cfa.harvard.edu/viz-bin/Cat?%s'%(cds_code)
cds_data_url = 'http://vizier.cfa.harvard.edu/viz-bin/nph-Cat/tar.gz?%s'%(cds_code)
print(cds_data_url)
with open(outdir+'VizieR_Catalogue_URL','w') as fp:
    fp.write(cds_data_url)
    fp.close()








