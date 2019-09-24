#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Usage: 
#    execfile('crabhttp_get_file_size.py')
# 


import urllib2
from BeautifulSoup import BeautifulSoup ## for now we are still using BS3
import re
import numpy
import numpy.lib.recfunctions as rec
import astropy
from datetime import datetime



def get_file_size():
    # -- http://stackoverflow.com/questions/5909/get-size-of-a-file-before-downloading-in-python
    link = "https://github.com/1054/DeepFields.SuperDeblending/blob/master/data/GOODSN_Photo/n_mips_1_s1_v0.37_sci_BS.fits?raw=true"
    link = "https://archive.stsci.edu/pub/hlsp/candels/goods-s/gsd01/v0.5/hlsp_candels_hst_acs_gsd01-sect22_f814w_v0.5_drz.fits"
    print "Opening Url:", link
    site = urllib2.urlopen(link)
    meta = site.info()
    print "Content-Length:", size_of_fmt(long(meta.getheaders("Content-Length")[0]))



def get_file_part():
    # -- http://stackoverflow.com/questions/22774266/read-specific-bytes-using-urlopen
    link = "https://github.com/1054/DeepFields.SuperDeblending/blob/master/data/GOODSN_Photo/n_mips_1_s1_v0.37_sci_BS.fits?raw=true"
    link = "https://archive.stsci.edu/pub/hlsp/candels/goods-s/gsd01/v0.5/hlsp_candels_hst_acs_gsd01-sect22_f814w_v0.5_drz.fits"
    print "Opening Url:", link
    print "Content:"
    fits_header_pointer = 0
    fits_header_grouper = 30
    fits_header_endline = False
    fits_header_content = []
    fits_header_counter = 0
    fits_header_NAXIS1  = 0
    fits_header_NAXIS2  = 0
    while not fits_header_endline:
        req = urllib2.Request(link)
        fits_header_postpos = fits_header_pointer+80*fits_header_grouper-1
        req.add_header('Range', 'bytes=' + str(fits_header_pointer) + '-' + str(fits_header_postpos))
        rep = urllib2.urlopen(req)
        strblock = rep.read()
        for fits_header_iterater in range(fits_header_grouper):
            strline = strblock[80*fits_header_iterater:80*fits_header_iterater+80]
            fits_header_content.append(strline)
            fits_header_counter = fits_header_counter + 1
            print strline
            if strline.startswith("END   "): 
                fits_header_endline = True
                fits_header_pointer = 80*fits_header_endline
                break
            if strline.startswith("NAXIS1  = "):
                if "/" in strline: 
                    fits_header_NAXIS1 = long(strline[10:strline.find("/")])
                else: 
                    fits_header_NAXIS1 = long(strline[10:])
            if strline.startswith("NAXIS2  = "):
                if "/" in strline: 
                    fits_header_NAXIS2 = long(strline[10:strline.find("/")])
                else: 
                    fits_header_NAXIS2 = long(strline[10:])
        # 
        fits_header_pointer = fits_header_postpos+1
        # 
        if fits_header_NAXIS2>0 and fits_header_NAXIS1>0:
            break
        #break



def size_of_fmt(num, suffix='B'):
    # -- http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)




get_file_part()








