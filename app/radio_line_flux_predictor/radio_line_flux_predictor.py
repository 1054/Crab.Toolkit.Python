#!/usr/bin/env python
# 
# 
# see also '/Users/dzliu/Cloud/GitLab/AlmaCosmos/Pipelines/a3cosmos-SED-fitting/a_dzliu_patch_code_identify_line_emitters.py'
# 


from __future__ import print_function

import os, sys, json, time, re
import numpy as np

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
from CrabPdBI import convert_Wavelength_um_to_Frequency_GHz, \
                    find_radio_lines_in_frequency_range, \
                    calc_radio_line_flux_from_IR_luminosity

if sys.version_info.major <= 2:
    pass
else:
    long = int







if __name__ == '__main__':
    # 
    # prepare variables
    line_name = ''
    line_flux = 0.0
    line_FWZI = 0.0
    line_freq = 0.0
    Redshift = 0.0
    SFR = 0.0 # Star Formation Rate
    IR_luminosity = 0.0
    # 
    # read user input
    i = 1
    while i < len(sys.argv):
        tmp_str = sys.argv[i].lower().replace('-','')
        if tmp_str == 'linename' or tmp_str == 'line':
            if i+1 < len(sys.argv):
                i = i+1
                line_name = sys.argv[i]
        elif tmp_str == 'sfr':
            if i+1 < len(sys.argv):
                i = i+1
                IR_luminosity = float(sys.argv[i]) * 1e10
        elif tmp_str == 'logsfr':
            if i+1 < len(sys.argv):
                i = i+1
                IR_luminosity = 10**(float(sys.argv[i])) * 1e10
        elif tmp_str == 'ir' or tmp_str == 'lir' or tmp_str == 'irluminosity':
            if i+1 < len(sys.argv):
                i = i+1
                IR_luminosity = float(sys.argv[i])
        elif tmp_str == 'loglir':
            if i+1 < len(sys.argv):
                i = i+1
                IR_luminosity = 10**float(sys.argv[i])
        elif tmp_str == 'z' or tmp_str == 'redshift':
            if i+1 < len(sys.argv):
                i = i+1
                Redshift = float(sys.argv[i])
        i = i+1
    # 
    # call function to compute line flux
    # for now we only support CO, CI, CII, NII lines and common transitions
    if line_name == '':
        print('Usage: ')
        print('    %s -linename CO(7-6) -LIR 5e10 -z 6.0'%(os.path.basename(__file__)))
        sys.exit()
    # 
    calc_radio_line_flux_from_IR_luminosity(line_name, IR_luminosity, Redshift, verbose=True)
    # 
    # 

