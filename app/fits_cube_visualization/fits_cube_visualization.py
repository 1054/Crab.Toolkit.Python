#!/usr/bin/env python3
# 
# ipython-3.6 --pylab=qt __file__

import os, sys, re, numpy as np
sys.path.append(os.path.expanduser('~')+os.sep+'Cloud/Github/Crab.Toolkit.Python/lib/crab')
from crabfitscube.CrabFitsCube import CrabFitsCube
from crabfitscube.CrabFitsCube import test_mayavi_points3d
from crabfitscube.CrabFitsCube import test_plotly_points3d
import time


#start = time.time()
#test_mayavi_points3d()
#end = time.time()
#print("Took %f ms" % ((end - start) * 1000.0))
#sys.exit()

#test_plotly_points3d()
#sys.exit()

data = CrabFitsCube('DataCube_Merged.lmv.fits')
#print(data.dimension())
#print(data.Cube.shape)

data.plot3d()

