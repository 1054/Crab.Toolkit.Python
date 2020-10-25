#!/usr/bin/env python
# 
# To run this code in Blender Python Console:
#    filename = '/Users/dzliu/Cloud/GitLab/AlmaCosmos/Plot/Plot_z_deltaGas_evolution/Plot_z_Mstar_deltaGas_DeltaMS_in_3D/a_dzliu_code_Plot_z_Mstar_deltaGas_DeltaMS_in_Blender.py'
#    exec(compile(open(filename).read(), filename, 'exec'))
# 
# 

import os, sys, re, copy
import numpy as np
import astropy
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.27, Tcmb0=2.725)

# 
# cd
# 
try:
    import bpy
    os.chdir(os.path.dirname(bpy.data.filepath))
    print(os.getcwd())
except:
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        print(os.getcwd())
    except:
        print('Error! Could not change working directory!')
        print(os.getcwd())
        sys.exit()


# 
# Prepare data table file 
# -- better be done outside Blender
# 
if not os.path.isfile('my_data_table.fits'):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+os.sep+'Common_Python_Code')
    from read_z_Mstar_SFR_Mgas_datasets import read_datasets
    all_datasets = read_datasets()
    # 
    DatasetID = []
    DatasetLabel = []
    ID = []
    z = []
    Mstar = []
    SFR = []
    DeltaMS = []
    Mgas = []
    t_dataset_count = 0
    for t_dataset in all_datasets:
        if t_dataset['label'].find('uplims') < 0:
            #print(t_dataset['label'])
            #print(type(t_dataset['ID']))
            #print(t_dataset['ID'].dtype)
            t_dataset_count += 1
            if t_dataset_count == 0:
                ID = copy.copy(t_dataset['ID'].astype(str))
                z = copy.copy(t_dataset['z'])
                Mstar = copy.copy(t_dataset['Mstar'])
                SFR = copy.copy(t_dataset['SFR'])
                DeltaMS = copy.copy(t_dataset['DeltaMS'])
                Mgas = copy.copy(t_dataset['Mmol'])
                DatasetID = np.array([t_dataset_count] * len(t_dataset['SFR']) )
                DatasetLabel = np.array([t_dataset['label']] * len(t_dataset['SFR']) )
            else:
                ID = np.concatenate((ID, t_dataset['ID'].astype(str)) )
                z = np.concatenate((z, t_dataset['z']) )
                Mstar = np.concatenate((Mstar, t_dataset['Mstar']) )
                SFR = np.concatenate((SFR, t_dataset['SFR']) )
                DeltaMS = np.concatenate((DeltaMS, t_dataset['DeltaMS']) )
                Mgas = np.concatenate((Mgas, t_dataset['Mmol']) )
                DatasetID = np.concatenate((DatasetID, [t_dataset_count] * len(t_dataset['SFR']) ) )
                DatasetLabel = np.concatenate((DatasetLabel, np.array([t_dataset['label']] * len(t_dataset['SFR'])) ) )
            print(t_dataset_count, t_dataset['label'], SFR.shape, DeltaMS.shape, Mgas.shape)
    # 
    dump_table_data = {}
    dump_table_data['ID'] = ID
    dump_table_data['z'] = z
    dump_table_data['Mstar'] = Mstar
    dump_table_data['SFR'] = SFR
    dump_table_data['Mgas'] = Mgas
    dump_table_data['DeltaMS'] = DeltaMS
    dump_table_data['DatasetID'] = DatasetID
    dump_table_data['DatasetLabel'] = DatasetLabel
    dump_table = Table(dump_table_data)
    # 
    dump_table.write('my_data_table.fits', format='fits', overwrite=True)
    print('Dumped data to "my_data_table.fits"!')

# 
# Read data table
# 
my_data_table = Table.read('my_data_table.fits')
z = my_data_table['z'].data
cosmoAge = cosmo.age(z).value
lgMstar = np.log10(my_data_table['Mstar'].data)
DeltaGas = np.log10(my_data_table['Mgas'].data / my_data_table['Mstar'].data)
DeltaMS = my_data_table['DeltaMS'].data
DatasetID = [int(t) for t in my_data_table['DatasetID'].data]
ID = [t for t in my_data_table['ID'].astype(str)]



# 
# Normalize data arrays to 0.0-1.0
# 
z_range = (0.0, 7.5)
cosmoAge_range = (0.0, cosmo.age(0).value)
lgMstar_range = (9.0, 13.0)
DeltaGas_range = (-1.5, 1.5)
#DeltaMS_range = (-1.0, 1.5)
#my_cmap = plt.get_cmap('YlOrRd')
#my_cmap = plt.get_cmap('autumn_r')
#my_cmap = plt.get_cmap('bwr')
#DeltaMS_range = (-0.5, 1.0)
#my_cmap = plt.get_cmap('Spectral_r')
DeltaMS_range = (-0.3, 1.0)
my_cmap = plt.get_cmap('viridis')
#plot_x_data = (z - z_range[0]) / (z_range[1] - z_range[0])
plot_x_data = ((cosmo.age(0).value - cosmoAge) - cosmoAge_range[0]) / (cosmoAge_range[1] - cosmoAge_range[0])
plot_y_data = (lgMstar - lgMstar_range[0]) / (lgMstar_range[1] - lgMstar_range[0])
plot_z_data = (DeltaGas - DeltaGas_range[0]) / (DeltaGas_range[1] - DeltaGas_range[0])
plot_labels = ['{}.{}'.format(t1, re.sub(r'[^a-zA-Z0-9_]',r'_','%s'%(t2))) for t1,t2 in zip(DatasetID, ID) ]
plot_colors = [my_cmap((tDeltaMS - DeltaMS_range[0]) / (DeltaMS_range[1] - DeltaMS_range[0])) for tDeltaMS in DeltaMS]
#plot_psizes = [(max([0.0, ((tDeltaMS) - DeltaMS_range[0])])) / (DeltaMS_range[1] - DeltaMS_range[0]) for tDeltaMS in DeltaMS] # scales with tDeltaMS
plot_psizes = [(max([0.0, ((-tDeltaMS/2.0) - DeltaMS_range[0])])) / (DeltaMS_range[1] - DeltaMS_range[0]) for tDeltaMS in DeltaMS] # scales with -tDeltaMS/3.0, so that lower DeltaMS sources have larger size
#plot_psizes = [0.0 for tDeltaMS in DeltaMS]





# 
# Load CrabBlender
# 
sys.path.append(os.path.join(os.path.expanduser('~'),'Cloud','Github','Crab.Toolkit.Python','lib','crab','crabblender'))
import CrabBlender
import importlib
importlib.reload(CrabBlender)


# 
# Delete all mesh objects
# 
CrabBlender.delete_all_sphere_objects()


# 
# Create blender 3D objects
# 
my_axes = CrabBlender.create_3D_axes()

plot_data_point_number = len(plot_x_data)
plot_data_point_size = 0.005 # 1.0 / plot_data_point_number * 5
print('plot_data_point_number = %s'%(plot_data_point_number))
print('plot_data_point_size = %s'%(plot_data_point_size))

sys.stdout.write('Plotting ...')
sys.stdout.flush()
for i in range(plot_data_point_number):
    my_data_point = CrabBlender.create_a_sphere(\
                        (plot_x_data[i], plot_y_data[i], plot_z_data[i]), 
                        plot_data_point_size * (1.0 + plot_psizes[i]), 
                        my_sphere_name = 'My_sphere'+'.'+plot_labels[i], 
                        my_sphere_color = plot_colors[i][0:3], 
                    )
    if i % int(plot_data_point_number / 20) == 0:
        sys.stdout.write(' %.1f%%'%(float(i)/float(plot_data_point_number)*100.0))
        sys.stdout.flush()
    #if i>500:
    #    break
sys.stdout.write(' 100%\n')
sys.stdout.flush()



# 
# Blender
# 
# Axis label text: scale 0.1, extrude 0.01, material emit=1, 
# 













