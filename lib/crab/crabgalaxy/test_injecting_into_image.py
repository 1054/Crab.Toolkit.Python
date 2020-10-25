#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# 

import os, sys, re, copy
import numpy as np
from astropy.io import fits
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CrabGalaxy import CrabGalaxy

my_galaxy_1 = CrabGalaxy(shape = 'sersic', size = {'major':10.0, 'minor':5.0, 'PA':20.0, 'n':1.0})
my_galaxy_2 = CrabGalaxy(shape = 'sersic', size = {'major':1.0, 'minor':0.5, 'PA':20.0, 'n':0.5})
my_galaxy_3 = CrabGalaxy(shape = 'Gaussian', size = {'major':3.0, 'minor':2.0, 'PA':20.0})

my_image_blank = np.random.normal(0.0, 0.2, size=(150, 200))

#print('\rWriting to "dump_my_image.fits" ...')
#dump_hdu = fits.PrimaryHDU(my_image_blank)
#dump_hdu.writeto('dump_my_image.fits', overwrite=True)
#print('\rWritten to "dump_my_image.fits"')



# no convolution
my_image = copy.copy(my_image_blank)
my_image = my_galaxy_1.inject_into_image(my_image, 1.0, flux = 250, x = 100.25, y = 100.25)
my_image = my_galaxy_2.inject_into_image(my_image, 1.0, flux = 250, x = 150.25, y = 100.25)
my_image = my_galaxy_3.inject_into_image(my_image, 1.0, flux = 250, x = 100.25, y = 50.25)

print('\rWriting to "dump_my_image_with_galaxy_no_convolution.fits" ...')
dump_hdu = fits.PrimaryHDU(my_image)
dump_hdu.writeto('dump_my_image_with_galaxy_no_convolution.fits', overwrite=True)
print('\rWritten to "dump_my_image_with_galaxy_no_convolution.fits"')



# do convolution
my_image = copy.copy(my_image_blank)
my_image = my_galaxy_1.inject_into_image(my_image, 1.0, flux = 250, x = 100.25, y = 100.25, convolving_beam = 2.0, oversampling_factor = -1)
my_image = my_galaxy_2.inject_into_image(my_image, 1.0, flux = 250, x = 150.25, y = 100.25, convolving_beam = 2.0, oversampling_factor = -1)
my_image = my_galaxy_2.inject_into_image(my_image, 1.0, flux = 250, x = 100.25, y = 50.25, convolving_beam = 2.0, oversampling_factor = -1)

print('\rWriting to "dump_my_image_with_galaxy_with_convolution.fits" ...')
dump_hdu = fits.PrimaryHDU(my_image)
dump_hdu.writeto('dump_my_image_with_galaxy_with_convolution.fits', overwrite=True)
print('\rWritten to "dump_my_image_with_galaxy_with_convolution.fits"')



# do convolution
my_image = copy.copy(my_image_blank)
my_image = my_galaxy_1.inject_into_image(my_image, 1.0, flux = 250, x = 100.25, y = 100.25, convolving_beam = 2.0)
my_image = my_galaxy_2.inject_into_image(my_image, 1.0, flux = 250, x = 150.25, y = 100.25, convolving_beam = 2.0)
my_image = my_galaxy_2.inject_into_image(my_image, 1.0, flux = 250, x = 100.25, y = 50.25, convolving_beam = 2.0)

print('\rWriting to "dump_my_image_with_galaxy_with_convolution_with_fractional_pixel.fits" ...')
dump_hdu = fits.PrimaryHDU(my_image)
dump_hdu.writeto('dump_my_image_with_galaxy_with_convolution_with_fractional_pixel.fits', overwrite=True)
print('\rWritten to "dump_my_image_with_galaxy_with_convolution_with_fractional_pixel.fits"')







