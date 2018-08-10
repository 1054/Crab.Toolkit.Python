#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 

################################
# 
# 
################################

try:
    import pkg_resources
except ImportError:
    raise SystemExit("Error! Failed to import pkg_resources!")

pkg_resources.require("numpy>=1.7")
pkg_resources.require("astropy>=1.3")

import os
import sys
import re
import math
import numpy
import astropy
from astropy.io import ascii as asciitable
from astropy.io import fits
from astropy.wcs import WCS
from pprint import pprint
from copy import copy
from astropy.utils.exceptions import AstropyWarning, AstropyUserWarning
import warnings
#warnings.simplefilter('ignore', category=AstropyUserWarning)
warnings.simplefilter('ignore', category=AstropyWarning)

#import vispy
import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.interactive(True)
import matplotlib.cm

#import mayavi
def import_mayavi():
    import importlib
    try:
        import mayavi
        import mayavi.mlab as mlab
        from tvtk.api import tvtk
        globals()['mayavi'] = mayavi
        globals()['mlab'] = mlab
        globals()['tvtk'] = tvtk
    except Exception as e:
        raise

#import plotly
def import_plotly():
    import importlib
    try:
        import plotly
        globals()['plotly'] = plotly
    except Exception as e:
        raise
    plotly.tools.set_credentials_file(username='liudz1054', api_key='679YxuqlHHa6OnxSgsh2')
        








def scale_data_value(val, min=numpy.nan, max=numpy.nan, clip_min=numpy.nan, clip_max=numpy.nan, power=numpy.nan, cmap='', alpha=1.0, 
                        set_clipped_data_invalid=True, 
                        set_alpha=True, invert_cmap=False, invert_alpha=False, 
                        log10=False, loge=False, compute_log_after_power=False):
    # Example:
    #     grayscale = scale_data_value(val, 0, 255)
    val_scaled = copy(val)
    # 
    if not numpy.isnan(clip_min):
        mask = (val_scaled<clip_min)
        if set_clipped_data_invalid:
            val_scaled[mask] = numpy.nan
        else:
            val_scaled[mask] = clip_min
    if not numpy.isnan(clip_max):
        mask = (val_scaled>clip_max)
        if set_clipped_data_invalid:
            val_scaled[mask] = numpy.nan
        else:
            val_scaled[mask] = clip_max
    # 
    if not compute_log_after_power:
        if log10 or loge:
            mask = (val_scaled>0)
            val_scaled[~mask] = numpy.nan
            if log10:
                val_scaled[mask] = numpy.log10(val_scaled[mask])
            elif loge:
                val_scaled[mask] = numpy.log(val_scaled[mask])
    # 
    if not numpy.isnan(power):
        if power >= 1.0:
            val_scaled = numpy.power(val_scaled, power)
        else:
            mask = (val_scaled>0)
            val_scaled[~mask] = numpy.nan
            val_scaled[mask] = numpy.power(val_scaled[mask], power)
    # 
    if compute_log_after_power:
        if log10 or loge:
            mask = (val_scaled>0)
            val_scaled[~mask] = numpy.nan
            if log10:
                val_scaled[mask] = numpy.log10(val_scaled[mask])
            elif loge:
                val_scaled[mask] = numpy.log(val_scaled[mask])
    # 
    min_val = numpy.nanmin(val_scaled)
    max_val = numpy.nanmax(val_scaled)
    # 
    if numpy.isnan(min):
        min = min_val
    if numpy.isnan(max):
        max = max_val
    if max < min:
        min, max = max, min
    if max_val < min_val:
        print('Warning! The input of CrabFitsCube::scale_data_value() is a flat data cube, min equals max! Nothing to scale!')
    else:
        # 
        mask = (~numpy.isnan(val_scaled))
        val_scaled[mask] = (val_scaled[mask]-min_val) / float(max_val-min_val) * float(max-min) + float(min)
    # 
    # 
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() min_val = ')
    print(min_val)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() max_val = ')
    print(max_val)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() clip_min = ')
    print(clip_min)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() clip_max = ')
    print(clip_max)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() min = ')
    print(min)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() max = ')
    print(max)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() val.shape = ')
    print(val.shape)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() val_scaled.shape = ')
    print(val_scaled.shape)
    # 
    val_scaled = val_scaled.reshape(val.shape)
    # 
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() val.shape = ')
    print(val.shape)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() val_scaled.shape = ')
    print(val_scaled.shape)
    # 
    mask = (~numpy.isnan(val_scaled))
    # 
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() val_scaled.size = ')
    print(val_scaled.size)
    sys.stdout.write('DEBUG: CrabFitsCube::scale_data_value() val_scaled[mask].size = ')
    print(val_scaled[mask].size)
    # 
    # 
    if cmap != '':
        # scale data value into color RGBA values
        cmap_lib = matplotlib.cm.get_cmap(cmap)
        min_val = numpy.nanmin(val_scaled)
        max_val = numpy.nanmax(val_scaled)
        val_scaled_rgba = cmap_lib((val_scaled-min_val)/float(max_val-min_val)) # cmap() needs value in range 0.0-1.0
        val_scaled_rgba[:,:,:,-1] = val_scaled_rgba[:,:,:,-1] * 0.0 + alpha # set alpha by alpha value
        if set_alpha:
            if not invert_alpha:
                val_scaled_rgba[:,:,:,-1] = (val_scaled_rgba[:,:,:,-1] * 0.0) + (val_scaled-min_val)/float(max_val-min_val) # set alpha by data value
            else:
                val_scaled_rgba[:,:,:,-1] = (val_scaled_rgba[:,:,:,-1] * 0.0) + (1.0-(val_scaled-min_val)/float(max_val-min_val)) # set alpha by inverted data value
        val_scaled = val_scaled_rgba
    # 
    # 
    return val_scaled

def generate_3D_Normal_Distribution(dim=[], shape=[], mu=[], sigma=[]):
    import scipy
    from scipy.stats import multivariate_normal
    if len(shape) == 0 :
        if len(dim) == 0:
            dim = [55, 35, 45] # dim is in the order of [nx,ny,nz]
        shape = dim[::-1] # shape is in the order of (nz,ny,nx)
    elif len(shape) < 3:
        raise Exception('Error! The input shape should be an array with three elements!')
    z, y, x = numpy.meshgrid(numpy.arange(shape[0]), numpy.arange(shape[1]), numpy.arange(shape[2]), sparse=False, indexing='ij')
    if len(mu) == 0:
        mu = numpy.array([(z.shape[2]-1)/2.0, (z.shape[1]-1)/2.0, (z.shape[0]-1)/2.0] )
    elif type(mu) is not numpy.ndarray:
        mu = numpy.array(mu)
    if len(sigma) == 0:
        sigma = numpy.array([0.9, 0.9, 0.9] )
    elif type(sigma) is not numpy.ndarray:
        sigma = numpy.array(sigma)
    covariance = numpy.diag(sigma**2)
    xyz = numpy.column_stack((x.flatten(), y.flatten(), z.flatten() ) )
    val = multivariate_normal.pdf(xyz, mean=mu, cov=covariance).reshape(x.shape)
    grayscale = scale_data_value(val, 0, 255, log10=True, clip_min=1e-60) # , clip_min=1e-30 # , clip_min=1e-300
    data = {}
    data['grayscale'] = grayscale
    data['val'] = val
    data['x'] = x
    data['y'] = y
    data['z'] = z
    data['mu'] = mu
    data['sigma'] = sigma
    data['covariance_matrix'] = covariance
    return data




class CrabFitsCubeDimension(object):
    def __init__(self, dshapes): 
        if len(dshapes) >= 3:
            self.X = dshapes[2]
            self.Y = dshapes[1]
            self.Z = dshapes[0]
        else:
            raise Exception('Error! The input of CrabFitsCubeDimension() should have be a dtype array with at least 3 elements!')
    # 
    def __str__(self):
        return 'Dimension: X=%d Y=%d Z=%d'%(self.X, self.Y, self.Z)



class CrabFitsCube(object):
    # 
    def __init__(self, FitsCubeFile, FitsCubeExtension=0):
        self.FitsCubeFile = FitsCubeFile
        print("Reading Fits Cube: %s"%(self.FitsCubeFile))
        self.FitsStruct = fits.open(self.FitsCubeFile)
        self.Cube = []
        self.Header = []
        self.Dimension = []
        self.WCS = []
        self.PixScale = [numpy.nan, numpy.nan]
        self.World = {}
        #print FitsCubePointer.info()
        # 
        CubeCount = 0
        for CubeId in range(len(self.FitsStruct)):
            if type(self.FitsStruct[CubeId]) is astropy.io.fits.hdu.image.PrimaryHDU:
                if CubeCount == FitsCubeExtension:
                    # 
                    # read fits image and header
                    self.Cube = self.FitsStruct[CubeId].data
                    self.Header = self.FitsStruct[CubeId].header
                    # 
                    # fix NAXIS to 2 if NAXIS>2, this is useful for VLA images
                    if int(self.Header['NAXIS']>3):
                        while(self.Header['NAXIS']>3):
                            self.Cube = self.Cube[0]
                            for TempStr in ('NAXIS','CTYPE','CRVAL','CRPIX','CDELT','CUNIT','CROTA'):
                                TempKey = '%s%d'%(TempStr,self.Header['NAXIS'])
                                if TempKey in self.Header:
                                    del self.Header[TempKey]
                                    #print("del %s"%(TempKey))
                            for TempInt in range(int(self.Header['NAXIS'])):
                                TempKey = 'PC%02d_%02d'%(TempInt+1,self.Header['NAXIS'])
                                if TempKey in self.Header:
                                    del self.Header[TempKey]
                                    #print("del %s"%(TempKey))
                                TempKey = 'PC%02d_%02d'%(self.Header['NAXIS'],TempInt+1)
                                if TempKey in self.Header:
                                    del self.Header[TempKey]
                                    #print("del %s"%(TempKey))
                            self.Header['NAXIS'] = self.Header['NAXIS']-1
                        for TempStr in ('NAXIS','CTYPE','CRVAL','CRPIX','CDELT','CUNIT','CROTA'):
                            for TempInt in (3,4):
                                TempKey = '%s%d'%(TempStr,TempInt)
                                if TempKey in self.Header:
                                    del self.Header[TempKey]
                    # 
                    self.Dimension = CrabFitsCubeDimension(self.Cube.shape)
                    self.WCS = WCS(self.Header)
                    self.PixScale = astropy.wcs.utils.proj_plane_pixel_scales(self.WCS) * 3600.0 # arcsec
                    # 
                    CubeCount = CubeCount + 1
                    break
                else:
                    CubeCount = CubeCount + 1
                # 
        if(CubeCount==0):
            print("Error! The input FitsCubeFile does not contain any data image!")
        # 
    # 
    def image(self):
        return self.Cube
    # 
    def getCube(self):
        return self.Cube
    # 
    def dimension(self):
        return self.Dimension
    # 
    def getDimension(self):
        return self.Dimension
    # 
    def wcs(self):
        return self.WCS
    # 
    def getWCS(self):
        return self.WCS
    # 
    def pixscale(self):
        return self.PixScale
    # 
    def getPixScale(self):
        return self.PixScale
    # 
    def plot3d_with_plotly(self):
        # WARNGING! plotly is a commercial software and is web-based!
        import_plotly()
        if len(self.Cube)>0:
            # print(numpy.meshgrid(numpy.arange(5), numpy.arange(2), numpy.arange(3)))
            x, y, z = numpy.meshgrid(numpy.arange(self.Dimension.Z), numpy.arange(self.Dimension.Y), numpy.arange(self.Dimension.X), sparse=False, indexing='ij' )
            val = self.Cube
            val_scaled = scale_data_value(val, 0, 255, log10=True, clip_min=1e-30)
            cmap = matplotlib.cm.get_cmap('hot')
            rgba = cmap(numpy.linspace(0, 1, cmap.N)) # cmap() needs value in range 0.0-1.0
            rgba[:,-1] = numpy.linspace(0, 1, cmap.N) # set alpha
            colorscale = []
            for ck in range(len(rgba)):
                colorscale.append([float(ck), 'rgba(%d,%d,%d,%.2f)'%(rgba[ck][0]*255, rgba[ck][1]*255, rgba[ck][2]*255, rgba[ck][3]) ] ) # define colorscale, see -- https://plot.ly/python/marker-style/ -- and -- https://plot.ly/python/colorscales/
            trace = plotly.graph_objs.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=6, color=val_scaled, colorscale=colorscale) )
            layout = plotly.graph_objs.Layout(margin=dict(l=0, r=0, b=0, t=0) )
            fig = plotly.graph_objs.Figure(data=[trace], layout=layout)
            plotly.plotly.iplot(fig)
    # 
    def plot3d_with_mayavi(self):
        import_mayavi()
        if len(self.Cube)>0:
            # print(numpy.meshgrid(numpy.arange(5), numpy.arange(2), numpy.arange(3)))
            z, y, x = numpy.meshgrid(numpy.arange(self.Dimension.Z), numpy.arange(self.Dimension.Y), numpy.arange(self.Dimension.X), sparse=False, indexing='ij' )
            val = self.Cube
            val_sigma = numpy.nanstd(val)
            val_scaled = scale_data_value(val, 0, 255, log10=True, clip_min=val_sigma*3.0) # clip at 3-sigma
            #print(x.shape)
            #print(y.shape)
            #print(z.shape)
            #print(val.shape)
            
            mask = (~numpy.isnan(val_scaled))
            
            #pts = mlab.points3d(x, y, z, val_scaled, scale_factor=1-0.618, colormap='hot', transparent=True) # see -- https://stackoverflow.com/questions/10755060/plot-a-cube-of-3d-intensity-data
            pts = mlab.points3d(x[mask], y[mask], z[mask], val_scaled[mask], scale_factor=0.618, colormap='hot', transparent=True, scale_mode='none', mode='cube') # see -- https://stackoverflow.com/questions/38962015/10-000-point-3d-scatter-plots-in-python-with-quick-rendering
            lut = pts.module_manager.scalar_lut_manager.lut.table.to_array() # Retrieve the LUT of the surf object. See -- http://docs.enthought.com/mayavi/mayavi/auto/example_custom_colormap.html
            lut[:, -1] = numpy.linspace(0, 255*0.618, 256) # We modify the alpha channel to add a transparency gradient
            #pts.glyph.color_mode = 'color_by_scalar' # Color by scalar, see --  https://stackoverflow.com/questions/18537172/specify-absolute-colour-for-3d-points-in-mayavi
            #pts.glyph.scale_mode = 'data_scaling_off'
            # 
            #--xx--# # Create the dataset.
            #--xx--# xyz = numpy.column_stack((x.ravel(), y.ravel(), z.ravel() ) )
            #--xx--# sg = tvtk.StructuredGrid(dimensions=val_scaled.shape[::-1], points=xyz)
            #--xx--# #sg.point_data.scalars = val_scaled[mask].ravel()
            #--xx--# #sg.point_data.scalars.name = 'data'
            #--xx--# ###sg.point_data.vectors = vectors
            #--xx--# ###sg.point_data.vectors.name = 'velocity'
            #--xx--# ds = mlab.pipeline.add_dataset(sg)
            #--xx--# # 
            #--xx--# # Create three simple grid plane modules.
            #--xx--# gpx = mlab.pipeline.grid_plane(ds) # see -- http://nullege.com/codes/search/mayavi.mlab.pipeline.grid_plane
            #--xx--# #gpy = mlab.pipeline.grid_plane(pts, opacity=0.5)
            #--xx--# #gpz = mlab.pipeline.grid_plane(pts, opacity=0.5)
            #--xx--# #gpx.grid_plane.axis = 'x'
            #--xx--# #gpy.grid_plane.axis = 'y'
            #--xx--# #gpz.grid_plane.axis = 'z'
            #--xx--# # Error! -- TypeError: The GridPlane component does not support the vtkPolyData dataset.
            # 
            # make grid
            scalarfieldspacingX = 10**(numpy.ceil(numpy.log10(self.Dimension.X))-1)
            scalarfieldspacingY = 10**(numpy.ceil(numpy.log10(self.Dimension.Y))-1)
            scalarfieldspacingZ = 10**(numpy.ceil(numpy.log10(self.Dimension.Z))-1)
            scalarfielddimensionX = int(numpy.ceil(float(self.Dimension.X)/scalarfieldspacingX)+1)
            scalarfielddimensionY = int(numpy.ceil(float(self.Dimension.Y)/scalarfieldspacingY)+1)
            scalarfielddimensionZ = int(numpy.ceil(float(self.Dimension.Z)/scalarfieldspacingZ)+1)
            print('DEBUG: scalarfieldspacingX = %s'%(scalarfieldspacingX))
            print('DEBUG: scalarfieldspacingY = %s'%(scalarfieldspacingY))
            print('DEBUG: scalarfieldspacingZ = %s'%(scalarfieldspacingZ))
            print('DEBUG: scalarfielddimensionX = %s'%(scalarfielddimensionX))
            print('DEBUG: scalarfielddimensionY = %s'%(scalarfielddimensionY))
            print('DEBUG: scalarfielddimensionZ = %s'%(scalarfielddimensionZ))
            scalarfielddata = mlab.pipeline.scalar_field(numpy.zeros((scalarfielddimensionX, scalarfielddimensionY, scalarfielddimensionZ)) )
            scalarfielddata.origin = [0.0, 0.0, 0.0]
            scalarfielddata.spacing = [scalarfieldspacingX, scalarfieldspacingY, scalarfieldspacingZ]
            gridplanex = mlab.pipeline.grid_plane(scalarfielddata)
            gridplanex.grid_plane.axis = 'z'
            # 
            mlab.axes(pts, ranges = [numpy.min(x[mask]), numpy.max(x[mask]), numpy.min(y[mask]), numpy.max(y[mask]), numpy.min(z[mask]), numpy.max(z[mask])] ) # see -- https://stackoverflow.com/questions/22164335/scale-mayavi-scatter-plot
            mlab.draw() # We need to force update of the figure now that we have changed the LUT.
            mlab.show()
            
            #--# # Another plotting method which is much faster but poorer qualitiy
            #--# mlab.pipeline.volume(mlab.pipeline.scalar_field(val_scaled), color=(1.0,0.0,0.0))
            #--# mlab.show()
            
            # 
            #val_contour = self.Cube.flatten()
            #pts = mlab.contour3d(x, y, z, val_contour, contours=4, transparent=True) # see -- https://docs.enthought.com/mayavi/mayavi/auto/mlab_helper_functions.html#contour3d
            
            #mlab.savefig(‘foo.png’, size=(300, 300))
            #mlab.view(azimuth=45, elevation=54, distance=1.)
    # 
    def plot3d(self):
        self.plot3d_with_mayavi()







def test_numpy_array_mesh_grid():
    val = numpy.random.random((3,2,5)) # NX=5, NY=2, NZ=3
    z, y, x = numpy.meshgrid(numpy.arange(3), numpy.arange(2), numpy.arange(5), sparse=False, indexing='ij')
    return
    # Note: numpy.meshgrid must be used with indexing='ij' instead of indexing='xy' (New in version 1.7.0)

def test_mayavi_points3d():
    import_mayavi()
    data = generate_3D_Normal_Distribution(dim=[101,101,101])
    data_noise = numpy.random.random(data['grayscale'].shape) * numpy.nanmax(data['grayscale']) * 0.05
    data['grayscale'] = data['grayscale'] + data_noise
    data_mask = (~numpy.isnan(data['grayscale']))
    sys.stdout.write('DEBUG: test_mayavi_points3d() len(data[\'grayscale\'][data_mask]) = ')
    print(len(data['grayscale'][data_mask]))
    
    #pts = mlab.points3d(data['x'], data['y'], data['z'], data['grayscale'], scale_factor=1-0.618, colormap='hot', transparent=True) # see -- https://stackoverflow.com/questions/10755060/plot-a-cube-of-3d-intensity-data
    #pts = mlab.points3d(data['x'], data['y'], data['z'], data['grayscale'], scale_factor=1-0.618, colormap='hot', transparent=True, scale_mode='none')
    pts = mlab.points3d(data['x'][data_mask], data['y'][data_mask], data['z'][data_mask], data['grayscale'][data_mask], scale_factor=1-0.618, colormap='hot', transparent=True, scale_mode='none')
    lut = pts.module_manager.scalar_lut_manager.lut.table.to_array() # Retrieve the LUT of the surf object. See -- http://docs.enthought.com/mayavi/mayavi/auto/example_custom_colormap.html
    print(lut)
    lut[:, -1] = numpy.linspace(0, 255, 256) # We modify the alpha channel to add a transparency gradient
    #pts.glyph.color_mode = 'color_by_scalar' # Color by scalar, see --  https://stackoverflow.com/questions/18537172/specify-absolute-colour-for-3d-points-in-mayavi
    pts.glyph.scale_mode = 'data_scaling_off'
    
    #--# mlab.pipeline.volume(mlab.pipeline.scalar_field(data['grayscale']), color=(1.0,0.0,0.0)) # http://docs.enthought.com/mayavi/mayavi/auto/mlab_pipeline_other_functions.html#volume
    
    #mlab.draw() # We need to force update of the figure now that we have changed the LUT.
    #mlab.view()
    mlab.show()

def test_plotly_points3d():
    import_plotly()
    data = generate_3D_Normal_Distribution()
    cmap = matplotlib.cm.get_cmap('hot')
    rgba = cmap(numpy.linspace(0, 1, cmap.N)) # cmap() needs value in range 0.0-1.0
    rgba[:,-1] = numpy.linspace(0, 1, cmap.N) # set alpha
    colorscale = []
    for ck in range(len(rgba)):
        colorscale.append([float(ck)/float(len(rgba)-1), 'rgba(%d,%d,%d,%.2f)'%(rgba[ck][0]*255, rgba[ck][1]*255, rgba[ck][2]*255, rgba[ck][3]) ] ) # define colorscale, see -- https://plot.ly/python/marker-style/ -- and -- https://plot.ly/python/colorscales/
    #print(type(colorscale))
    #print(colorscale[0])
    #print(colorscale[-1])
    trace = plotly.graph_objs.Scatter3d(x=data['x'], y=data['y'], z=data['z'], mode='markers', marker=dict(size=6, color=data['grayscale'], colorscale=colorscale) )
    layout = plotly.graph_objs.Layout(margin=dict(l=0, r=0, b=0, t=0) )
    fig = plotly.graph_objs.Figure(data=[trace], layout=layout)
    plotly.plotly.iplot(fig, filename='test_plotly_points3d')








