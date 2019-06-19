#!/usr/bin/env python
# 

from __future__ import print_function
import pkg_resources
pkg_resources.require('astropy>=2.0') # since 2.0 astropy.modeling.blackbody
import os, sys, re, json, time, astropy
import numpy as np
import astropy.io.ascii as asciitable
from astropy.table import Table, Column, hstack
#from astropy.convolution import convolve_fft
from numpy.fft import fft, ifft, fftfreq, fftshift, ifftshift
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
from copy import copy
from pprint import pprint
from datetime import datetime
#from astropy.cosmology import WMAP9 as cosmo
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.27, Tcmb0=2.725)
from astropy import units as u
from astropy import constants as const
from astropy.modeling.blackbody import blackbody_lambda, blackbody_nu
import scipy
from scipy.interpolate import interp1d
import matplotlib as mpl
mpl.rcParams['axes.labelsize'] = '12' # https://matplotlib.org/users/customizing.html
mpl.rcParams['axes.grid'] = True
mpl.rcParams['axes.axisbelow'] = True
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.minor.visible'] = True
mpl.rcParams['ytick.minor.visible'] = True
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
#mpl.rcParams['grid.color'] = 'b0b0b0'
mpl.rcParams['grid.linestyle'] = '--'
mpl.rcParams['grid.linewidth'] = 0.25
mpl.rcParams['grid.alpha'] = 0.8
mpl.rcParams['text.usetex'] = True

sys.path.append(os.path.expanduser('~')+os.sep+'Cloud/Github/Crab.Toolkit.Python/lib/crab/crabpdbi/')
from CrabPdBI import ( find_radio_lines_in_frequency_range, 
                       calc_radio_line_frequencies, 
                       calc_radio_line_flux_from_IR_luminosity, 
                       convert_flux2lprm, 
                       convert_flux2lsun, 
                       convert_lprm2lsun, 
                     )

sys.path.append(os.path.expanduser('~')+os.sep+'Cloud/Github/Crab.Toolkit.Python/lib/crab/crabplot/')
from CrabPlot import ( CrabPlot )












if __name__ == '__main__':
    lgLIR = np.arange(8.0,14.0,0.1)
    x = []
    y = []
    x2 = []
    y2 = []
    for i in range(len(lgLIR)):
        IR_luminosity = 10**(lgLIR[i])
        z = 3.0
        IR_color = 0.6
        rest_freq, line_name = calc_radio_line_frequencies('OIII 88', set_output_line_names = True)
        dL = cosmo.luminosity_distance(z).to(u.Mpc).value
        line_flux = calc_radio_line_flux_from_IR_luminosity(line_name, IR_luminosity, z, starburstiness = 0.0, IR_color = IR_color, verbose = False)
        line_lprm = convert_flux2lprm(line_flux, rest_freq, z)
        line_lsun = convert_lprm2lsun(line_lprm, rest_freq)
        x.append(line_lprm)
        y.append(IR_luminosity)
        print('IR_luminosity = %e, line_lsun = %e, line_flux = %g'%(IR_luminosity, line_lsun, line_flux) )
        
        line_flux = calc_radio_line_flux_from_IR_luminosity(line_name, IR_luminosity, z, starburstiness = 1.0, IR_color = IR_color, verbose = False)
        line_lprm = convert_flux2lprm(line_flux, rest_freq, z)
        line_lsun = convert_lprm2lsun(line_lprm, rest_freq)
        x2.append(line_lprm)
        y2.append(IR_luminosity)
        
    cplot = CrabPlot()
    cplot.plot_xy(x, y, xlog=1, ylog=1, xtitle=r'$L_{\mathrm{[OIII]}}$', ytitle=r'$L_{\mathrm{IR}}$', label='dzliu model MS')
    cplot.plot_xy(x2, y2, overplot=1, color='red', label='dzliu model SB')
    
    lgLsunOIII88 = ((lgLIR-10+0.05) + 7.48) / 1.12 # De Looze et al. 2014 Table 3 "SFR calibration: entire literature sample". Note that they are using Kroupa IMF
    cplot.plot_line(10**lgLsunOIII88, 10**lgLIR, overplot=1, linewidth=20, alpha=0.5, color='gold', label='De Looze+2014')
    
    cplot.ax().legend(fontsize=20)
    
    cplot.save('Plot_test_1_OIII.pdf')







