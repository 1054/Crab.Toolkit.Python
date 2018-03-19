#!/usr/bin/env python2.7
# 

try:
    import pkg_resources
except ImportError:
    raise SystemExit("Error! Failed to import pkg_resources!")

pkg_resources.require("numpy")
pkg_resources.require("scipy")
pkg_resources.require("astropy")

import numpy
import scipy
from scipy import optimize
from pprint import pprint
import astropy.io.ascii as asciitable
from CrabCurveFit import *


data = asciitable.read('CrabCurveFitTest_1/dump_fit_func_x_y_1.53.txt')
x = data['col0'].data
x = numpy.power(10,x)
y = data['col1'].data
p_fit = fit_func_gravity_energy_field(x,y)
pprint(p_fit)


import sys
sys.path.insert(1,'/Users/dzliu/Softwares/Python/lib/crab/crabplot')
from CrabPlot import *
p_plot = CrabPlot(x,y)
p_plot.plot_line(x,p_fit['y_fit'],overplot=True)
pyplot.show(block=True)




















