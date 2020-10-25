#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# 

import os, sys, re
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CrabGalaxy import CrabGalaxy

my_galaxy = CrabGalaxy(shape = 'sersic', size = {'major':1.0, 'minor':0.5, 'PA':20.0, 'n':0.5})



y, x = np.mgrid[0:3, 0:5] # nx=5, ny=3
oversampling_factor = 4

yy, xx = my_galaxy.Morph.resample_mgrid(y, x, oversampling_factor)
print('y:', y, '\nyy:', yy)
print('x:', x, '\nxx:', xx)

print('y:', y, '\nyy[::oversampling_factor,::oversampling_factor]', yy[::oversampling_factor,::oversampling_factor])
print('x:', x, '\nxx[::oversampling_factor,::oversampling_factor]', xx[::oversampling_factor,::oversampling_factor])

