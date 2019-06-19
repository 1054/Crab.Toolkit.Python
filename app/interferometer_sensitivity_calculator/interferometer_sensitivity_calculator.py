#!/usr/bin/env python
# 
# 
# see also '/Users/dzliu/Cloud/GitLab/AlmaCosmos/Pipelines/a3cosmos-SED-fitting/a_dzliu_patch_code_identify_line_emitters.py'
# 


from __future__ import print_function

import os, sys, json, time, re
import numpy
np = numpy

import astropy
import astropy.io.ascii as asciitable
from astropy.table import Table, Column

from copy import copy
from pprint import pprint
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FuncFormatter, LogLocator, MultipleLocator

np.warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+os.sep+'lib/crab/crabpdbi')
from CrabPdBI import calc_Sensitivity

if sys.version_info.major <= 2:
    pass
else:
    long = int







if __name__ == '__main__':
    # 
    # prepare variables
    Telescope = ''
    Diameter = 0.0
    Frequency = 0.0
    Nant = 0
    Tint = 0.0
    Tsys = []
    dv = 0.0
    bw = 0.0
    # 
    # read user input
    i = 1
    while i < len(sys.argv):
        tmp_str = sys.argv[i].lower().replace('-','')
        if tmp_str == 'ant' or tmp_str == 'antenna' or tmp_str == 'antennae' or tmp_str == 'Nant':
            if i+1 < len(sys.argv):
                i = i+1
                Nant = int(sys.argv[i])
        elif tmp_str == 'tel' or tmp_str == 'telescope':
            if i+1 < len(sys.argv):
                i = i+1
                Telescope = str(sys.argv[i]).strip()
        elif tmp_str == 'dia' or tmp_str == 'diameter':
            if i+1 < len(sys.argv):
                i = i+1
                if re.match(r'([0-9.]+)\s*m', sys.argv[i], re.IGNORECASE):
                    Diameter = float(re.sub(r'([0-9.]+)\s*m', r'\1', sys.argv[i], re.IGNORECASE))
                elif re.match(r'([0-9.]+)\s*dm', sys.argv[i], re.IGNORECASE):
                    Diameter = float(re.sub(r'([0-9.]+)\s*dm', r'\1', sys.argv[i], re.IGNORECASE)) / 10.0
                elif re.match(r'([0-9.]+)\s*cm', sys.argv[i], re.IGNORECASE):
                    Diameter = float(re.sub(r'([0-9.]+)\s*cm', r'\1', sys.argv[i], re.IGNORECASE)) / 100.0
                else:
                    Diameter = float(sys.argv[i])
        elif tmp_str == 'freq' or tmp_str == 'frequency':
            if i+1 < len(sys.argv):
                i = i+1
                if re.match(r'([0-9.]+)\s*GHz', sys.argv[i], re.IGNORECASE):
                    Frequency = float(re.sub(r'([0-9.]+)\s*GHz', r'\1', sys.argv[i], re.IGNORECASE))
                elif re.match(r'([0-9.]+)\s*MHz', sys.argv[i], re.IGNORECASE):
                    Frequency = float(re.sub(r'([0-9.]+)\s*MHz', r'\1', sys.argv[i], re.IGNORECASE)) / 1e3
                elif re.match(r'([0-9.]+)\s*kHz', sys.argv[i], re.IGNORECASE):
                    Frequency = float(re.sub(r'([0-9.]+)\s*kHz', r'\1', sys.argv[i], re.IGNORECASE)) / 1e6
                elif re.match(r'([0-9.]+)\s*Hz', sys.argv[i], re.IGNORECASE):
                    Frequency = float(re.sub(r'([0-9.]+)\s*Hz', r'\1', sys.argv[i], re.IGNORECASE)) / 1e9
                else:
                    Frequency = float(sys.argv[i])
        elif tmp_str == 'tint':
            if i+1 < len(sys.argv):
                i = i+1
                if re.match(r'([0-9.]+)\s*s', sys.argv[i], re.IGNORECASE):
                    Tint = float(re.sub(r'([0-9.]+)\s*s', r'\1', sys.argv[i], re.IGNORECASE))
                elif re.match(r'([0-9.]+)\s*m', sys.argv[i], re.IGNORECASE):
                    Tint = float(re.sub(r'([0-9.]+)\s*m', r'\1', sys.argv[i], re.IGNORECASE)) * 60.0
                elif re.match(r'([0-9.]+)\s*h', sys.argv[i], re.IGNORECASE):
                    Tint = float(re.sub(r'([0-9.]+)\s*h', r'\1', sys.argv[i], re.IGNORECASE)) * 3600.0
                else:
                    Tint = float(sys.argv[i])
        elif tmp_str == 'tsys':
            if i+1 < len(sys.argv):
                i = i+1
                if re.match(r'([0-9.]+)\s*K', sys.argv[i], re.IGNORECASE):
                    Tsys = float(re.sub(r'([0-9.]+)\s*K', r'\1', sys.argv[i], re.IGNORECASE))
                else:
                    Tsys = float(sys.argv[i])
        elif tmp_str == 'bw':
            if i+1 < len(sys.argv):
                i = i+1
                if re.match(r'([0-9.]+)\s*GHz', sys.argv[i], re.IGNORECASE):
                    bw = float(re.sub(r'([0-9.]+)\s*GHz', r'\1', sys.argv[i], re.IGNORECASE))
                elif re.match(r'([0-9.]+)\s*MHz', sys.argv[i], re.IGNORECASE):
                    bw = float(re.sub(r'([0-9.]+)\s*MHz', r'\1', sys.argv[i], re.IGNORECASE)) / 1e3
                elif re.match(r'([0-9.]+)\s*kHz', sys.argv[i], re.IGNORECASE):
                    bw = float(re.sub(r'([0-9.]+)\s*kHz', r'\1', sys.argv[i], re.IGNORECASE)) / 1e6
                elif re.match(r'([0-9.]+)\s*Hz', sys.argv[i], re.IGNORECASE):
                    bw = float(re.sub(r'([0-9.]+)\s*Hz', r'\1', sys.argv[i], re.IGNORECASE)) / 1e9
                else:
                    bw = float(sys.argv[i])
        elif tmp_str == 'dv':
            if i+1 < len(sys.argv):
                i = i+1
                if re.match(r'([0-9.]+)\s*km/s', sys.argv[i], re.IGNORECASE):
                    dv = float(re.sub(r'([0-9.]+)\s*km/s', r'\1', sys.argv[i], re.IGNORECASE))
                else:
                    dv = float(sys.argv[i])
        i = i+1
    # 
    # calc_Sensitivity
    if Nant == '' or Frequency <= 0.0:
        print('Usage: ')
        print('    %s -Nant 27 -Tint 3600s -dia 7m -dv 300km/s -freq 32.9GHz [-Tsys 100]'%(os.path.basename(__file__)))
        sys.exit()
    # 
    out = calc_Sensitivity(Tint=Tint, Tsys=Tsys, Nant=Nant, Npol=2, Bandwidth=0.0, bw=bw, Velowidth=0.0, dv=dv, 
                           Frequency=Frequency, freq=0.0, Telescope=Telescope, Diameter=Diameter, Weather='winter', eta_ap=numpy.nan, 
                           Verbose=True)
    # 
    # 

