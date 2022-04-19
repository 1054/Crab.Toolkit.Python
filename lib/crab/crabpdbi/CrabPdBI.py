#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# 
# subroutines:
#   def calc_radio_line_frequencies(line_names, set_output_line_names = False)
#   def find_radio_lines_in_frequency_range(Frequency_Range_GHz, Redshift = 0.0, set_output_line_names = True, include_faint_lines = True)
#   def convert_Frequency_GHz_to_ALMA_Band_Info(Frequency_GHz)
#   def convert_Frequency_GHz_to_ALMA_Band_Number(Frequency_GHz)
#   def convert_Wavelength_um_to_Frequency_GHz(Wavelength_um)
#   def calc_BeamSize(Frequency_GHz, Diameter_m)
#   def calc_SolidAngle(BeamSize_arcsec)
#   def calc_JanskyPerKelvin(Aeff_m2, Frequency_GHz, Diameter_m)
#   def calc_ALMA_Bands(Frequency_GHz)
#   def calc_Sensitivity(Tint=[], Tsys=[], Nant=0, Npol=2, Bandwidth=0.0, bw=0.0, Velowidth=0.0, dv=0.0,
#   def convert_flux2lprm(S_Jy_km_s, rest_freq_GHz, z = 0.0, dL = 0.0)
#   def convert_lprm2flux(L_K_km_s__1_pc_2, rest_freq_GHz, z = 0.0, dL = 0.0)
#   def convert_flux2lsun(S_Jy_km_s, rest_freq_GHz, z = 0.0, dL = 0.0)
#   def convert_lsun2flux(L_L_sun, rest_freq_GHz, z = 0.0, dL = 0.0)
#   def convert_lprm2lsun(L_K_km_s__1_pc_2, rest_freq_GHz)
#   def convert_lsun2lprm(L_L_sun, rest_freq_GHz)
#   def get_CO_excitation_ladder_for_BzKs(Jansky_scale = True)
#   def calc_CII_based_on_DeLooze2011(IR_luminosity, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_CII_based_on_dzliu_model_2017a(IR_luminosity, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_NII_based_on_Zhao2016(IR_luminosity, line_J_up, IR_color, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_HCN_based_on_Gao2004(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_HCN_based_on_Zhang2014(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_CS_based_on_Zhang2014(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_CO_based_on_Daddi2010(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_CO_based_on_Sargent2014(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_CO_based_on_Liudz2015(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_CI_based_on_Liudz2015(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = False)
#   def calc_radio_line_flux_from_IR_luminosity(line_name, IR_luminosity, z, starburstiness = 0.0, IR_color = 1.0, verbose = True)
# 
# 

import os, sys, re, time
import numpy
import scipy
import astropy
import itertools
from datetime import datetime
from scipy.constants import speed_of_light
from scipy.constants import Boltzmann as k_B
from scipy.interpolate import interp1d
from scipy.interpolate import InterpolatedUnivariateSpline
#from astropy.cosmology import WMAP9 as cosmo
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.27, Tcmb0=2.725)


def calc_radio_line_frequencies(line_names, set_output_line_names = False):
    if type(line_names) is not list and type(line_names) is not tuple:
        line_names = [line_names]
        is_input_a_list = False
    else:
        is_input_a_list = True
    # 
    # https://1054.github.io/Wiki/radio_line_frequencies/
    table_CO = []
    table_CO.append(115.2712018)
    table_CO.append(230.5380000)
    table_CO.append(345.7959899)
    table_CO.append(461.0407682)
    table_CO.append(576.2679305)
    table_CO.append(691.4730763)
    table_CO.append(806.6518060)
    table_CO.append(921.7997000)
    table_CO.append(1036.9123930)
    table_CO.append(1151.9854520) # up to CO(10-9)
    #table_CO.append(1267.0144860)
    #table_CO.append(1381.9951050)
    #table_CO.append(1496.9229090)
    #table_CO.append(1611.7935180)
    #table_CO.append(1726.6025057)
    #table_CO.append(1841.3455060)
    #table_CO.append(1956.0181390)
    #table_CO.append(2070.6159930)
    #table_CO.append(2185.1346800)
    #table_CO.append(2299.5698420)
    table_OIII = []
    table_OIII.append(3393.) # [OIII]3P1-3P0, 88.36um, Draine (2011)
    table_OIII.append(5786.) # [OIII]3P2-3P1, 51.81um, Draine (2011)
    table_NIII = []
    table_NIII.append(5229.) # [NIII]2P3/2−2P1/2, 57.32um, Malhotra et al. (2001)
    table_OI = []
    table_OI.append(2.99792458e5/145.525439) # [OI]3P0−3P1, 145.53um, Draine (2011)
    table_OI.append(2.99792458e5/63.183705) # [OI]3P1-3P2, 63um, http://www.ipac.caltech.edu/iso/lws/atomic.html
    table_CII = []
    table_CII.append(1900.53690) # [CII]2P3/2−2P1/2
    table_CI = []
    table_CI.append(492.16065)
    table_CI.append(809.34197)
    table_NII = []
    table_NII.append(1461.13141)
    #table_NII.append(2459.38010)
    table_HCN = []
    table_HCN.append(88.6316023)
    table_HCN.append(177.2611115)
    table_HCN.append(265.8864343)
    table_HCN.append(354.5054779)
    table_HCN.append(443.1161493)
    table_CS = []
    table_CS.append(48.9909549)
    table_CS.append(97.9809533)
    table_CS.append(146.9690287)
    table_CS.append(195.9542109)
    table_CS.append(244.9355565)
    table_CS.append(293.9120865)
    table_CS.append(342.8828503)
    table_CS.append(391.8468898)
    table_H2O = {}
    #table_H2O['1_{1,0}-1_{0,1}'] = 556.93599
    #table_H2O['1_{1,1}-0_{0,0}'] = 1113.34301
    #table_H2O['2_{0,2}-1_{1,1}'] = 987.92676
    #table_H2O['2_{1,1}-2_{0,2}'] = 752.03314
    #table_H2O['2_{1,2}-1_{0,1}'] = 1669.90477
    #table_H2O['2_{2,0}-2_{1,1}'] = 1228.78872
    #table_H2O['2_{2,1}-2_{1,2}'] = 1661.00764
    #table_H2O['3_{0,2}-2_{1,2}'] = 1716.76963
    table_H2O['3_{1,2}-2_{2,1}'] = 1153.12682
    #table_H2O['3_{1,2}-3_{0,3}'] = 1097.36479
    #table_H2O['3_{2,1}-3_{1,2}'] = 1162.91160
    #table_H2O['3_{2,2}-3_{1,3}'] = 1919.35953
    #table_H2O['3_{3,1}-4_{0,4}'] = 1893.68651
    #table_H2O['4_{1,3}-4_{0,4}'] = 1602.21937
    #table_H2O['4_{2,2}-3_{3,1}'] = 916.17158
    #table_H2O['4_{2,2}-4_{1,3}'] = 1207.63873
    #table_H2O['4_{2,3}-3_{3,0}'] = 448.00108
    #table_H2O['4_{3,2}-5_{0,5}'] = 1713.88297
    #table_H2O['5_{2,3}-4_{3,2}'] = 1918.48535
    #table_H2O['5_{2,3}-5_{1,4}'] = 1410.61807
    #table_H2O['5_{2,4}-4_{3,1}'] = 970.31505
    #table_H2O['5_{3,2}-4_{4,1}'] = 620.70095
    #table_H2O['6_{2,4}-6_{1,5}'] = 1794.78895
    #table_H2O['6_{2,5}-5_{2,3}'] = 1322.06480
    #table_H2O['6_{3,3}-5_{4,2}'] = 1541.96701
    #table_H2O['6_{3,3}-6_{2,4}'] = 1762.04279
    #table_H2O['6_{3,4}-5_{4,1}'] = 1158.32385
    # 
    output_frequencies_GHz = []
    output_line_names = []
    # 
    for line_name in line_names:
        # CO molecule
        if re.match(r'CO\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = int(re.sub(r'CO\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', r'\1', line_name.strip(), re.IGNORECASE)) - 1
            output_frequency_GHz = table_CO[table_index]
            output_line_name = 'CO(%d-%d)' % (table_index+1, table_index)
        elif re.match(r'CO', line_name.strip(), re.IGNORECASE):
            table_index = -99
            output_frequency_GHz = table_CO 
            output_line_name = ['CO(%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_CO))]
            # output the whole table if the input has only molecule/atom name
        # HCN molecule
        elif re.match(r'HCN\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = int(re.sub(r'HCN\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', r'\1', line_name.strip(), re.IGNORECASE)) - 1
            output_frequency_GHz = table_HCN[table_index]
            output_line_name = 'HCN(%d-%d)' % (table_index+1, table_index)
        elif re.match(r'HCN', line_name.strip(), re.IGNORECASE):
            table_index = -99
            output_frequency_GHz = table_HCN 
            output_line_name = ['HCN(%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_HCN))]
            # output the whole table if the input has only molecule/atom name
        # next molecule
        elif re.match(r'[\[]?CII[\]]?\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = int(re.sub(r'[\[]?CII[\]]?\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', r'\1', line_name.strip(), re.IGNORECASE)) - 1
            output_frequency_GHz = table_CII[table_index]
            output_line_name = '[CII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?CII[\]]?\s*158.*', line_name.strip(), re.IGNORECASE):
            table_index = 0
            output_frequency_GHz = table_CII[table_index]
            output_line_name = '[CII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?CII[\]]?', line_name.strip(), re.IGNORECASE):
            table_index = -99
            output_frequency_GHz = table_CII 
            output_line_name = ['[CII](%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_CII))]
            # output the whole table if the input has only molecule/atom name
        # next molecule
        elif re.match(r'[\[]?OIII[\]]?\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = int(re.sub(r'[\[]?OIII[\]]?\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', r'\1', line_name.strip(), re.IGNORECASE)) - 1
            output_frequency_GHz = table_OIII[table_index]
            output_line_name = '[OIII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?OIII[\]]?\s*88.*', line_name.strip(), re.IGNORECASE):
            table_index = 0
            output_frequency_GHz = table_OIII[table_index]
            output_line_name = '[OIII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?OIII[\]]?\s*(51|52).*', line_name.strip(), re.IGNORECASE):
            table_index = 1
            output_frequency_GHz = table_OIII[table_index]
            output_line_name = '[OIII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?OIII[\]]?', line_name.strip(), re.IGNORECASE):
            table_index = -99
            output_frequency_GHz = table_OIII 
            output_line_name = ['[OIII](%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_OIII))]
            # output the whole table if the input has only molecule/atom name
        # next molecule
        elif re.match(r'[\[]?OI[\]]?\s*[\(\[]?3P([0-9]+)\-3P([0-9]+)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = int(re.sub(r'[\[]?OI[\]]?\s*[\(\[]?3P([0-9]+)\-3P([0-9]+)[\)\]]?', r'\2', line_name.strip(), re.IGNORECASE)) - 1 # note the naming: 3P0-3P1, 3P1-3P2
            output_frequency_GHz = table_OI[table_index]
            output_line_name = '[OI](3P%d-3P%d)' % (table_index, table_index+1) # note the naming: 3P0-3P1, 3P1-3P2
        elif re.match(r'[\[]?OI[\]]?\s*63.*', line_name.strip(), re.IGNORECASE):
            table_index = 1
            output_frequency_GHz = table_OI[table_index]
            output_line_name = '[OI](3P%d-3P%d)' % (table_index, table_index+1) # note the naming: 3P0-3P1, 3P1-3P2
        elif re.match(r'[\[]?OI[\]]?\s*(145|146).*', line_name.strip(), re.IGNORECASE):
            table_index = 0
            output_frequency_GHz = table_OI[table_index]
            output_line_name = '[OI](3P%d-3P%d)' % (table_index, table_index+1) # note the naming: 3P0-3P1, 3P1-3P2
        elif re.match(r'[\[]?OI[\]]?', line_name.strip(), re.IGNORECASE):
            table_index = -99
            output_frequency_GHz = table_OI 
            output_line_name = ['[OI](3P%d-3P%d)' % (table_index, table_index+1) for table_index in range(len(table_OI))] # note the naming: 3P0-3P1, 3P1-3P2
            # output the whole table if the input has only molecule/atom name
        # next molecule
        elif re.match(r'[\[]?CI[\]]?\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = int(re.sub(r'[\[]?CI[\]]?\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', r'\1', line_name.strip(), re.IGNORECASE)) - 1
            output_frequency_GHz = table_CI[table_index]
            output_line_name = '[CI](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?CI[\]]?\s*[\(\[]?(3\_?P\_?1)\-(3\_?P\_?0)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = 0
            output_frequency_GHz = table_CI[table_index]
            output_line_name = '[CI](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?CI[\]]?\s*[\(\[]?(3\_?P\_?2)\-(3\_?P\_?1)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = 1
            output_frequency_GHz = table_CI[table_index]
            output_line_name = '[CI](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?CI[\]]?\s*609.*', line_name.strip(), re.IGNORECASE):
            table_index = 0
            output_frequency_GHz = table_CI[table_index]
            output_line_name = '[CI](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?CI[\]]?\s*370.*', line_name.strip(), re.IGNORECASE):
            table_index = 1
            output_frequency_GHz = table_CI[table_index]
            output_line_name = '[CI](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?CI[\]]?', line_name.strip(), re.IGNORECASE):
            table_index = -99
            output_frequency_GHz = table_CI 
            output_line_name = ['[CI](%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_CI))]
            # output the whole table if the input has only molecule/atom name
        # next molecule
        elif re.match(r'[\[]?NII[\]]?\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = int(re.sub(r'[\[]?NII[\]]?\s*[\(\[]?([0-9]+)\-([0-9]+)[\)\]]?', r'\1', line_name.strip(), re.IGNORECASE)) - 1
            output_frequency_GHz = table_NII[table_index]
            output_line_name = '[NII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?NII[\]]?\s*[\(\[]?(3\_?P\_?1)\-(3\_?P\_?0)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = 0
            output_frequency_GHz = table_NII[table_index]
            output_line_name = '[NII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?NII[\]]?\s*[\(\[]?(3\_?P\_?2)\-(3\_?P\_?1)[\)\]]?', line_name.strip(), re.IGNORECASE):
            table_index = 1
            output_frequency_GHz = table_NII[table_index]
            output_line_name = '[NII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?NII[\]]?\s*205.*', line_name.strip(), re.IGNORECASE):
            table_index = 0
            output_frequency_GHz = table_NII[table_index]
            output_line_name = '[NII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?NII[\]]?\s*122.*', line_name.strip(), re.IGNORECASE):
            table_index = 1
            output_frequency_GHz = table_NII[table_index]
            output_line_name = '[NII](%d-%d)' % (table_index+1, table_index)
        elif re.match(r'[\[]?NII[\]]?', line_name.strip(), re.IGNORECASE):
            table_index = -99
            output_frequency_GHz = table_NII 
            output_line_name = ['[NII](%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_NII))]
        
        elif line_name.strip().startswith('H2O'):
            output_line_name = ''
            if output_line_name == '':
                regex_matcher = re.match(r'H2O\(?([0-9])_?{?([0-9]),?([0-9])}?-?([0-9])_?{?([0-9]),?([0-9])}?\)?', line_name.strip(), re.IGNORECASE)
                if regex_matcher is not None:
                    if len(regex_matcher.groups()) == 6:
                        table_key = '%d_{%d,%d}-%d_{%d,%d}'%(int(regex_matcher.groups()[0]), int(regex_matcher.groups()[1]), int(regex_matcher.groups()[2]), 
                                                             int(regex_matcher.groups()[3]), int(regex_matcher.groups()[4]), int(regex_matcher.groups()[5]))
                        if table_key in table_H2O:
                            output_frequency_GHz = table_H2O[table_key]
                            output_line_name = 'H2O(%s)'%(table_key)
        
        elif '*' == line_name.strip():
            table_index = -99
            output_frequency_GHz = []
            output_line_name = []
            output_frequency_GHz.extend(table_CO)
            output_line_name.extend(['CO(%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_CO))])
            output_frequency_GHz.extend(table_CII)
            output_line_name.extend(['[CII](%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_CII))])
            output_frequency_GHz.extend(table_OI)
            output_line_name.extend(['[OI](3P%d-3P%d)' % (table_index, table_index+1) for table_index in range(len(table_OI))]) # note the naming: 3P0-3P1, 3P1-3P2
            output_frequency_GHz.extend(table_OIII)
            output_line_name.extend(['[OIII](%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_OIII))])
            output_frequency_GHz.extend(table_CI)
            output_line_name.extend(['[CI](%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_CI))])
            output_frequency_GHz.extend(table_NII)
            output_line_name.extend(['[NII](%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_NII))])
            output_frequency_GHz.extend(table_HCN)
            output_line_name.extend(['HCN(%d-%d)' % (table_index+1, table_index) for table_index in range(len(table_HCN))])
            for table_key in table_H2O:
                output_frequency_GHz.append(table_H2O[table_key])
                output_line_name.append('H2O(%s)' % (table_key))
            # output the whole table if the input has only molecule/atom name
        else:
            #print('Error! calc_radio_line_frequencies() could not understand line_name "%s"' % (line_name))
            #sys.exit()
            raise ValueError('Error! calc_radio_line_frequencies() could not understand line_name "%s"' % (line_name))
        # end
        if is_input_a_list:
            output_frequencies_GHz.append(output_frequency_GHz)
            output_line_names.append(output_line_name)
        else:
            if type(output_frequency_GHz) is list or type(output_frequency_GHz) is tuple:
                output_frequencies_GHz.extend(output_frequency_GHz)
                output_line_names.extend(output_line_name)
            else:
                if len(line_names) == 1:
                    output_frequencies_GHz = output_frequency_GHz # if input is not a list and has only one item, we return one item
                    output_line_names = output_line_name # if input is not a list and has only one item, we return one item
                else:
                    output_frequencies_GHz.append(output_frequency_GHz) # this should not happen, because if the input is not a list, then it should not have more than one items.
                    output_line_names.append(output_line_name) # this should not happen, because if the input is not a list, then it should not have more than one items.
    if set_output_line_names:
        return output_frequencies_GHz, output_line_names
    return output_frequencies_GHz


def find_radio_lines_in_frequency_range(Frequency_Range_GHz, Redshift = 0.0, set_output_line_names = True, include_faint_lines = True, set_invalid_edge_width = None):
    freqs, lines = calc_radio_line_frequencies('*', set_output_line_names = True)
    freqs = numpy.array(freqs) / (1.0+Redshift)
    output_line_freqs = []
    output_line_names = []
    #print('find_radio_lines_in_frequency_range() type(Frequency_Range_GHz) =', type(Frequency_Range_GHz))
    if type(Frequency_Range_GHz) is list or type(Frequency_Range_GHz) is tuple:
        Frequency_Range_GHz = numpy.hstack(Frequency_Range_GHz) # flatten the input list
        for j in range(0,len(Frequency_Range_GHz),2):
            freq_range = [Frequency_Range_GHz[j], Frequency_Range_GHz[j+1]]
            if type(freq_range) is list or type(freq_range) is tuple:
                if len(freq_range) >= 2:
                    for i in range(len(freqs)):
                        edge_width = [0.0, 0.0]
                        if set_invalid_edge_width is not None:
                            if numpy.isscalar(set_invalid_edge_width):
                                edge_width = [float(set_invalid_edge_width), float(set_invalid_edge_width)]
                            elif len(set_invalid_edge_width) == 1:
                                edge_width = [float(set_invalid_edge_width[0]), float(set_invalid_edge_width[0])]
                            else:
                                edge_width = [float(set_invalid_edge_width[0]), float(set_invalid_edge_width[1])]
                        if freqs[i] >= freq_range[0]+edge_width[0] and freqs[i] <= freq_range[1]-edge_width[0]:
                            if not include_faint_lines:
                                if not lines[i].startswith('CO') and \
                                   not lines[i].startswith('[CI]') and \
                                   not lines[i].startswith('[CII]') and \
                                   not lines[i].startswith('[NII]') and \
                                   not lines[i].startswith('[OI]') and \
                                   not lines[i].startswith('[OIII]') and \
                                   not lines[i].startswith('H2O'):
                                    continue
                            #print(freqs[i], lines[i])
                            output_line_freqs.append(freqs[i])
                            output_line_names.append(lines[i])
                else:
                    print('Error! The input of find_radio_lines_in_frequency_range() should be a list or tuple, each element is a two-element list or tuple indicating the frequency range!')
                    sys.exit()
            else:
                print('Error! The input of find_radio_lines_in_frequency_range() should be a list or tuple, each element is a two-element list or tuple indicating the frequency range!')
                sys.exit()
    else:
        print('Error! The input of find_radio_lines_in_frequency_range() should be a list or tuple, each element is a two-element list or tuple indicating the frequency range!')
        sys.exit()
    if set_output_line_names:
        return output_line_freqs, output_line_names
    return output_line_freqs


def convert_Frequency_GHz_to_ALMA_Band_Info(Frequency_GHz):
    # 
    BandInfo = {}
    BandInfo['BandNumber'] = int(-99)
    BandInfo['Tsys'] = [] # [(freq1,Tsys1),(freq2,Tsys2),...] # TODO
    BandInfo['IF'] = 0.0
    BandInfo['IF_Range'] = []
    BandInfo['LO_Range'] = []
    BandInfo['Bandwidth'] = 0.0
    BandInfo['SidebandMode'] = '' # DSB, 2SB, SSB
    BandInfo['FrequencyRange'] = []
    # 
    # ALMA_Cycle6_Technical_Handbook.pdf, page 32, Table 4.1
    # 
    if Frequency_GHz >= 84.0 and Frequency_GHz <= 116.0:
        BandInfo['BandNumber'] = 3                                                # ALMA Band 3 (EU)
        BandInfo['FrequencyRange'] = [84.0, 116.0]
        BandInfo['SidebandMode'] = '2SB'
        BandInfo['IF_Range'] = [4.0,8.0]
        BandInfo['LO_Range'] = [92.0,108.0]
        BandInfo['Bandwidth'] = 7.5
        IF = 6.0
    # 
    elif Frequency_GHz >= 125.0 and Frequency_GHz <= 163.0:
        BandInfo['BandNumber'] = 4                                                # ALMA Band 4 (JP)
        BandInfo['FrequencyRange'] = [125.0, 163.0]
        BandInfo['SidebandMode'] = '2SB'
        BandInfo['IF_Range'] = [4.0,8.0]
        BandInfo['LO_Range'] = [133.0,155.0]
        BandInfo['Bandwidth'] = 7.5
    # 
    elif Frequency_GHz >= 158.0 and Frequency_GHz <= 211.0:
        BandInfo['BandNumber'] = 5                                                # ALMA Band 5 (EU)
        BandInfo['FrequencyRange'] = [158.0, 211.0]
        BandInfo['SidebandMode'] = '2SB'
        BandInfo['IF_Range'] = [4.0,8.0]
        BandInfo['LO_Range'] = [166.0,203.0]
        BandInfo['Bandwidth'] = 7.5
    # 
    elif Frequency_GHz >= 211.0 and Frequency_GHz <= 275.0:
        BandInfo['BandNumber'] = 6                                                # ALMA Band 6 (US-EU)
        BandInfo['FrequencyRange'] = [211.0, 275.0]
        BandInfo['SidebandMode'] = '2SB'
        BandInfo['IF_Range'] = [4.5,10.0]
        BandInfo['LO_Range'] = [221.0,265.0]
        BandInfo['Bandwidth'] = 7.5
    # 
    elif Frequency_GHz >= 275.0 and Frequency_GHz <= 373.0:
        BandInfo['BandNumber'] = 7                                                # ALMA Band 7 (US-EU)
        BandInfo['FrequencyRange'] = [275.0, 373.0]
        BandInfo['SidebandMode'] = '2SB'
        BandInfo['IF_Range'] = [4.0,8.0]
        BandInfo['LO_Range'] = [283.0,365.0]
        BandInfo['Bandwidth'] = 7.5
    # 
    elif Frequency_GHz >= 385.0 and Frequency_GHz <= 500.0:
        BandInfo['BandNumber'] = 8                                                # ALMA Band 8 (JP)
        BandInfo['FrequencyRange'] = [385.0, 500.0]
        BandInfo['SidebandMode'] = '2SB'
        BandInfo['IF_Range'] = [4.0,8.0]
        BandInfo['LO_Range'] = [393.0,492.0]
        BandInfo['Bandwidth'] = 7.5
    # 
    elif Frequency_GHz >= 602.0 and Frequency_GHz <= 720.0:
        BandInfo['BandNumber'] = 9                                                # ALMA Band 9 (US-EU)
        BandInfo['FrequencyRange'] = [602.0, 720.0]
        BandInfo['SidebandMode'] = 'DSB'
        BandInfo['IF_Range'] = [4.0,8.0]
        BandInfo['LO_Range'] = [610.0,712.0]
        BandInfo['Bandwidth'] = 7.5
    # 
    elif Frequency_GHz >= 787.0 and Frequency_GHz <= 950.0:
        BandInfo['BandNumber'] = 10                                               # ALMA Band 10 (JP)
        BandInfo['FrequencyRange'] = [787.0, 950.0]
        BandInfo['SidebandMode'] = 'DSB'
        BandInfo['IF_Range'] = [4.0,8.0]
        BandInfo['LO_Range'] = [795.0,942.0]
        BandInfo['Bandwidth'] = 7.5
    # 
    return BandInfo


def convert_Frequency_GHz_to_ALMA_Band_Number(Frequency_GHz):
    BandInfo = convert_Frequency_GHz_to_ALMA_Band_Info(Frequency_GHz)
    return BandInfo['BandNumber']


def convert_Wavelength_um_to_Frequency_GHz(Wavelength_um):
    # 
    return (speed_of_light/1e3/numpy.array(Wavelength_um)) # GHz


def calc_BeamSize(Frequency_GHz, Diameter_m):
    # ALMA_Cycle4_Technical_Handbook_08Sep2016.pdf -- Equation(3.4)
    #return 1.02 * (speed_of_light/1e9/Frequency_GHz) / Diameter_m / numpy.pi * 180.0 * 3600.0 # arcsec
    # 
    # 20180108
    return 1.22 * (speed_of_light/1e9/Frequency_GHz) / Diameter_m / numpy.pi * 180.0 * 3600.0 # arcsec


def calc_SolidAngle(BeamSize_arcsec):
    # 
    return (numpy.pi * (BeamSize_arcsec/3600.0/180.0*numpy.pi)**2) / (4.0 * numpy.log(2.0))


def calc_JanskyPerKelvin(Aeff_m2, Frequency_GHz, Diameter_m):
    # 
    # 1 / Aeff * Omega / lambda**2 [Jy/K]
    # [W s K^-1 m^-2] -> [W m^-2 Hz-1 K^-1] -> 1e26 [Jy K^-1]
    #return (1.0 / Aeff_m2) / (2.99792458e8/(Frequency_GHz*1e9))**2 * calc_SolidAngle(calc_BeamSize(Frequency_GHz, Diameter_m))
    # 
    # 2 * k_B * Omega / lambda**2 [Jy/K]
    # [W s K^-1 m^-2] -> [W m^-2 Hz-1 K^-1] -> 1e26 [Jy K^-1]
    #return (2.0 * 1.38e-23 * calc_SolidAngle(calc_BeamSize(Frequency_GHz, Diameter_m))) / ((2.99792458e8/(Frequency_GHz*1e9))**2) / 1e-26
    # 
    # 2 * k_B / Aeff
    # [W s K^-1 m^-2] -> [W m^-2 Hz-1 K^-1] -> 1e26 [Jy K^-1]
    #return (2.0 * 1.38e-23 / Aeff_m2 * 1e26) # this is better because "Aeff_m2" considers "eta_ap".
    return (2.0 * k_B / Aeff_m2 * 1e26) # this is better because "Aeff_m2" considers "eta_ap".
    # 
    # More references:
    # S(Jy)/T_mb(K)=8.18E-7*theta(")^2*nu(GHz)^2 (Rohlfs & Wilson, Tools of Radioastronomy (2. ed., Eq. 8.20) -- http://www1.ynao.ac.cn/~jinhuahe/know_base/instruments/millimeter_radio/iram30m.htm


def calc_ALMA_Bands(Frequency_GHz, edge_GHz=0.0):
    # 
    List_of_ALMA_Bands = [ 
                        {'band number':1, 'lower frequency':35.0+edge_GHz, 'higher frequency':50.0-edge_GHz}, 
                        {'band number':2, 'lower frequency':65.0+edge_GHz, 'higher frequency':90.0-edge_GHz}, 
                        {'band number':3, 'lower frequency':84.0+edge_GHz, 'higher frequency':116.0-edge_GHz}, 
                        {'band number':4, 'lower frequency':125.0+edge_GHz, 'higher frequency':163.0-edge_GHz}, 
                        {'band number':5, 'lower frequency':163.0+edge_GHz, 'higher frequency':211.0-edge_GHz}, 
                        {'band number':6, 'lower frequency':211.0+edge_GHz, 'higher frequency':275.0-edge_GHz}, 
                        {'band number':7, 'lower frequency':275.0+edge_GHz, 'higher frequency':373.0-edge_GHz}, 
                        {'band number':8, 'lower frequency':385.0+edge_GHz, 'higher frequency':500.0-edge_GHz}, 
                        {'band number':9, 'lower frequency':602.0+edge_GHz, 'higher frequency':720.0-edge_GHz}, 
                        {'band number':10, 'lower frequency':787.0+edge_GHz, 'higher frequency':950.0-edge_GHz}, 
                    ]
    if type(Frequency_GHz) is astropy.table.column.Column:
        t_freq = Frequency_GHz.data
    elif type(Frequency_GHz) is list:
        t_freq = numpy.array(Frequency_GHz)
    else:
        t_freq = Frequency_GHz
    # 
    ALMA_Bands = numpy.full(len(t_freq), -99, dtype=int)
    # 
    for b_i in range(len(List_of_ALMA_Bands)):
        #t_in_range = (t_freq>=List_of_ALMA_Bands[b_i]['lower frequency'] & t_freq<=List_of_ALMA_Bands[b_i]['higher frequency']) # -- this is buggy -- must have brackets not covering &
        t_in_range = (t_freq>=List_of_ALMA_Bands[b_i]['lower frequency']) & (t_freq<=List_of_ALMA_Bands[b_i]['higher frequency'])
        #print(t_in_range)
        if len(numpy.argwhere(t_in_range))>0:
            ALMA_Bands[t_in_range] = List_of_ALMA_Bands[b_i]['band number'] # use numpy boolean array as numpy array index
    return ALMA_Bands


def calc_Sensitivity(Tint=[], Tsys=[], Nant=0, Npol=2, Bandwidth=0.0, bw=0.0, Velowidth=0.0, dv=0.0, 
                     Frequency=0.0, freq=0.0, Telescope='NOEMA', Diameter=0, Weather='winter', eta_ap=numpy.nan, eta_mb=numpy.nan, 
                     Verbose=True):
    # 
    # NOEMACapabilities.pdf 
    # 
    # The rms noise can be computed from
    #     {\sigma} = \frac{ t_JpK * Tsys }{ \eta * \sqrt{Nant*(Nant-1)*Tint*Bandwidth*Npol} }
    # where
    #     t_JpK is the conversion factor from Kelvin to Jansky, 
    #         t_JpK = (1.0/Aeff) * lambda^2 / Omega, 
    #               Aeff = eta_ap * Area, 
    #                      eta_ap = 0.72 * exp(-16*pi^2*sigma^2/lambda^2), 
    #                               sigma is the rms surface accuracy of the antenna.
    #               Omega = (pi * theta^2) / (4.0*ln(2))
    #         e.g. ALMA 12m, band 3, eta_ap = 0.71, Area = 113.1 m^2, so t_JpK = 0.71 * 1.38e-16 erg/K / 113.1 m^2 = 0.71 * 1.38e-16 * 1e23 / 113.1e4 [Jy/K * s cm^2 Hz cm^2] = 8.663129973 [Jy/K]
    #         e.g. ALMA 7m, band 3, eta_ap = 0.71, Area = 38.5 m^2, so t_JpK = 0.71 * 1380 / 38.5 = 25.44935065 [Jy/K]
    #         e.g., IRAM 30m, 110GHz, eta_a = 0.75 * 0.79 = 0.59, see -- http://www.iram.es/IRAMES/t_Telescope/t_TelescopeSummary/t_Telescope_summary.html
    #     \eta is an additional efficiency factor due to atmospheric phase noise
    #     Bandwidth in GHz (or Velowidth in km/s)
    #     Frequency in GHz
    # 
    # Example
    #     from CrabPdBI import *
    #     calc_Sensitivity(Tint=3600.0, Tsys=160.0, Nant=1, Npol=2, dv=500.0, freq=90.0, Telescope='ALMA 12m')
    # 
    # check input nan
    if numpy.isnan(Velowidth):
        Velowidth = -99.0
    if numpy.isnan(Bandwidth):
        Bandwidth = -99.0
    # 
    # If input Frequency by argument freq
    if Frequency <= 0.0 and freq > 0.0:
        Frequency = freq
    if type(Frequency) is str:
        Frequency = float(Frequency)
    # 
    # If input velocity width by argument dv
    if Velowidth <= 0.0 and dv > 0.0:
        Velowidth = dv
    # 
    # If input band width by argument bw
    if Bandwidth <= 0.0 and bw > 0.0:
        Bandwidth = bw
    # 
    # If input velocity width instead of bandwidth, then convert to bandwidth
    if Velowidth > 0.0 and Bandwidth <= 0.0 and Frequency > 0.0:
        Bandwidth = (Velowidth/(speed_of_light/1e3)) * Frequency # GHz
    # 
    # calculate velocity width from bandwidth
    if Bandwidth > 0.0 and Frequency > 0.0:
        Velowidth = (Bandwidth/Frequency) * (speed_of_light/1e3) # km/s
    # 
    # If input Tint is not a list, make it a list
    if type(Tint) is not list:
        Tint = [Tint]
    #print(Tint, len(Tint))
    # 
    # If input Tsys is not a list, make it a list
    if type(Tsys) is not list:
        Tsys = [Tsys]
    #print(Tsys, len(Tsys))
    # 
    # If input Bandwidth is not given, print error
    if not Frequency > 0.0:
        print("Error! Frequency is not given (in GHz)!")
        return []
    # 
    # If input Bandwidth is not given, print error
    if not Bandwidth > 0.0:
        print("Error! Bandwidth is not given (in GHz)!")
        return []
    # 
    # If input Nantenna, Bandwidth, Frequency are valid, then do sensitivity calculation
    Output_2d = []
    if Bandwidth > 0.0 and Frequency > 0.0:
        Frequency = float(Frequency)
        Bandwidth = float(Bandwidth)
        # 
        Output_1d = []
        # 
        # Loop each Tint
        for i_Tint in range(len(Tint)):
            # 
            # prepare an array for each Tsys
            Output_1d = []
            # 
            # determine Tsys
            if len(Tsys) == 0:
                Tsys = [numpy.nan]
            # 
            # If input Tsys is a list, then loop each Tsys
            for i_Tsys in range(len(Tsys)):
                # 
                # determine \eta and t_JpK
                t_eta_q = numpy.nan # from ALMA tech handbook: 
                                    # quantization efficiency. A fundamental limit on the achievable sensitivity is set by the initial 3-bit
                                    # digitization of the baseband signals. This is equal to 0.96.
                t_eta_c = numpy.nan # from ALMA tech handbook: correlator efficiency. This depends on the correlator (64-input or ACA) and correlator mode, although
                                    # the efficiency of all 64-input Correlator modes is equal to 0.88. The ACA efficiencies do depend on the
                                    # mode, but this is only taken into account in the OT, not by the web application or OT GUI, which
                                    # therefore assume a value of 0.88
                t_shadow = numpy.nan # from ALMA tech handbook: shadowing fraction
                                     # For the more compact 12 m configurations and the ACA 7-m Array, antennas
                                     # can block the field-of-view of other antennas in the array and thus reduce the total collecting area. The
                                     # shadowing fraction is a function of source declination as shown in Fig. 7.5.
                t_robust = numpy.nan # from ALMA tech handbook: robust weighting factor
                                     # Pipeline imaging and subsequent QA2 assessment is performed assuming
                                     # that the visibilities are weighted using robust weighting, specifically a Briggs robustness factor of 0.5.
                                     # Simulations have shown that this factor is equal to 1.1.
                t_eta_qc = numpy.nan # = t_eta_q * t_eta_c, is the spectrometer efficiency (eta_spec) in NOEMA handbook "http://iram-institute.org/medias/uploads/astro-noema-time-estimator.pdf" 
                t_eta_ap = numpy.nan # aperture efficient to the antenna area, eta_ap * antenna_area =  effective area (Aeff_m2)
                t_JpK = numpy.nan
                t_Bandnumb = numpy.nan
                t_Telescop = ''
                t_Beamsize = 0.0
                t_Nant = 0         # temporary variable, will be overriden if it has been given by the user. 
                t_Dant = numpy.nan # temporary variable, will be overriden if it has been given by the user. 
                t_Aant = numpy.nan # temporary variable, will be overriden if it has been given by the user. 
                t_Tsys = numpy.nan # temporary variable, will be overriden if it has been given by the user. 
                t_Tint = numpy.nan # temporary variable, will be overriden if it has been given by the user. 
                rms = numpy.nan
                # 
                # determine Tsys for NOEMA 
                # 
                if Telescope.upper().find('NOEMA')>=0:
                    t_Telescop = 'NOEMA'
                    t_Beamsize = calc_BeamSize(Frequency, 15.0) # NOEMA 15m
                    # 
                    # determine Nant
                    t_Nant = 7 # ealier than 2017-09-14
                    t_Nant = 9 # later than 2017-09-14
                    t_Dant = 15.0
                    t_Aant = numpy.pi * (t_Dant/2.0)**2
                    # 
                    # determine Band
                    # Band 1 before 201703 was 80-116GHz
                    # Band 1 after 201703 was 70.9-121.6GHz
                    # Band 2 before 201703 was 130-177GHz
                    # Band 2 after 201703 was 124.4-183.6GHz
                    # Band 3 before 201703 was 202-267GHz
                    # Band 3 after 201703 was 196.4-279.6GHz
                    if Frequency >= 70.9 and Frequency <= 121.6:
                        t_Bandnumb = 1    # NOEMA Band 1
                        t_eta_qc = 0.9    # NOEMA Band 1, February 22, 2016
                        t_JpK = 22.0      # NOEMA Band 1, February 22, 2016
                        # t_JpK = calc_JanskyPerKelvin(numpy.pi*(15.0/2.0)**2 * 0.95, Frequency, 15.0) / eta      #<before><20170312><pms.iram.fr># 
                        # t_Tsys = 100.0 if(Frequency<110) else (Frequency-110)/(116-110)*(185.0-100.0)+100.0     #<before><20170312><pms.iram.fr># 
                        # t_Tsys = 85.0 if(Frequency<110) else (Frequency-110)/(121.6-110)*(185.0-100.0)+100.0
                        if(Weather.lower().find('winter')>=0):
                            database_Tsys = {'freq':[70., 80, 110, 122.],
                                             'Tsys':[140, 75, 85., 313.]} #<20170312># /Users/dzliu/Softwares/GILDAS/gildas-exe-10feb17/pro/noema-sensitivity-estimator.astro
                        else:
                            database_Tsys = {'freq':[70., 80, 110, 122.],
                                             'Tsys':[150, 85, 95., 323.]} #<20170312># /Users/dzliu/Softwares/GILDAS/gildas-exe-10feb17/pro/noema-sensitivity-estimator.astro
                        # 
                        t_Tsys = numpy.interp(Frequency, database_Tsys['freq'], database_Tsys['Tsys'])
                    elif Frequency >= 124.4 and Frequency <= 183.6:
                        t_Bandnumb = 2    # NOEMA Band 2
                        t_eta_qc = 0.8    # NOEMA Band 2, February 22, 2016
                        t_JpK = 29.0      # NOEMA Band 2, February 22, 2016
                        # t_JpK = calc_JanskyPerKelvin(numpy.pi*(15.0/2.0)**2 * 0.85, Frequency, 15.0) / eta #<TODO># dzliu
                        # t_Tsys = 150.0 if(Frequency<150) else (Frequency-150)/(177-150)*(200.0-150.0)+150.0
                        if(Weather.lower().find('winter')>=0):
                            database_Tsys = {'freq':[124, 126, 150, 184.],
                                             'Tsys':[110, 110, 110, 195.]} #<20170312># /Users/dzliu/Softwares/GILDAS/gildas-exe-10feb17/pro/noema-sensitivity-estimator.astro
                        else:
                            database_Tsys = {'freq':[124, 126, 150, 184.],
                                             'Tsys':[140, 140, 140, 242.]} #<20170312># /Users/dzliu/Softwares/GILDAS/gildas-exe-10feb17/pro/noema-sensitivity-estimator.astro
                        # 
                        t_Tsys = numpy.interp(Frequency, database_Tsys['freq'], database_Tsys['Tsys'])
                    elif Frequency >= 196.4 and Frequency <= 279.6:
                        t_Bandnumb = 3    # NOEMA Band 3
                        t_eta_qc = 0.6    # NOEMA Band 3, February 22, 2016
                        t_JpK = 35.0      # NOEMA Band 3, February 22, 2016
                        # t_JpK = calc_JanskyPerKelvin(numpy.pi*(15.0/2.0)**2 * 0.75, Frequency, 15.0) / eta #<TODO># dzliu
                        # t_Tsys = 250.0
                        if(Weather.lower().find('winter')>=0):
                            database_Tsys = {'freq':[195, 196, 230, 280.],
                                             'Tsys':[190, 190, 190, 190.]} #<20170312># /Users/dzliu/Softwares/GILDAS/gildas-exe-10feb17/pro/noema-sensitivity-estimator.astro
                        else:
                            database_Tsys = {'freq':[195, 196, 230, 280.],
                                             'Tsys':[250, 250, 250, 250.]} #<20170312># /Users/dzliu/Softwares/GILDAS/gildas-exe-10feb17/pro/noema-sensitivity-estimator.astro
                        # 
                        t_Tsys = numpy.interp(Frequency, database_Tsys['freq'], database_Tsys['Tsys'])
                # 
                # determine Tsys for ALMA
                # 
                elif Telescope.upper().find('ALMA')>=0:
                    # 
                    t_Bandnumb = convert_Frequency_GHz_to_ALMA_Band_Number(Frequency)
                    t_Telescop = 'ALMA'
                    if Telescope.find('7m')>=0:
                        t_Beamsize = calc_BeamSize(Frequency, 7.0)
                        t_Telescop = t_Telescop + ' 7m'
                        t_Aant = 38.5 # antenna collecting area
                        t_Dant = 7.0 # antenna diameter
                        t_Nant = 10
                        t_eta_ap_7m = {'3':0.71, '4':0.71, '5':0.00, '6':0.69, '7':0.66, '8':0.64, '9':0.52, '10':0.42} # ALMA_Cycle4_Technical_Handbook_08Sep2016.pdf -- PDF Page 130, Table 9.3
                        t_eta_ap = t_eta_ap_7m[str(t_Bandnumb)]
                    elif Telescope.find('12m')>=0:
                        t_Beamsize = calc_BeamSize(Frequency, 12.0)
                        t_Telescop = t_Telescop + ' 12m'
                        t_Aant = 113.1 # antenna collecting area
                        t_Dant = 12.0 # antenna diameter
                        t_Nant = 40
                        t_eta_ap_12m = {'3':0.71, '4':0.70, '5':0.00, '6':0.68, '7':0.63, '8':0.60, '9':0.43, '10':0.31} # ALMA_Cycle4_Technical_Handbook_08Sep2016.pdf -- PDF Page 130, Table 9.3
                        t_eta_ap = t_eta_ap_12m[str(t_Bandnumb)]
                    else:
                        t_Beamsize = calc_BeamSize(Frequency, 12.0)
                        t_Telescop = t_Telescop + ' 12m'
                        t_Aant = 113.1 # antenna collecting area
                        t_Dant = 12.0 # antenna diameter
                        t_Nant = 40
                        t_eta_ap_12m = {'3':0.71, '4':0.70, '5':0.00, '6':0.68, '7':0.63, '8':0.60, '9':0.43, '10':0.31} # ALMA_Cycle4_Technical_Handbook_08Sep2016.pdf -- PDF Page 130, Table 9.3
                        t_eta_ap = t_eta_ap_12m[str(t_Bandnumb)]
                    # 
                    t_eta_q = 0.96
                    t_eta_c = 0.88
                    t_robust = 1.1
                    t_shadow = 0.0
                    t_eta_qc = t_eta_q * t_eta_c / t_robust * (1.0 - t_shadow) 
                                # ALMA_Cycle4_Technical_Handbook_08Sep2016.pdf -- the last 0.0 is shadowing
                                # see also Section~9.2.1, Eq.~(9.8) on page 138 of \url{https://almascience.eso.org/proposing/documents-and-tools/latest/documents-and-tools/cycle6/alma-technical-handbook}
                    # 
                    # 
                    # determine Band
                    if t_Bandnumb == 3:
                        t_Tsys = 70.0 if(Frequency<110) else (Frequency-110)/(116-110)*(170.0-70.0)+70.0
                    elif t_Bandnumb == 4:
                        #t_Tsys = 80.0 if(Frequency>130) else (Frequency-130)/(125-130)*(100.0-80.0)+80.0
                        #if (Frequency>142 and Frequency<145): t_Tsys = 90.0
                        t_Tsys_spl = InterpolatedUnivariateSpline(
                                        numpy.array([125.0, 130.0, 135.0, 140.0, 140.15, 140.2, 140.25, 150.0, 155.0, 160.0, 165.0]), 
                                        numpy.array([95.0,  80.0,  78.0,  78.0,  78,     90,    78,     78,    80,    82,    84.  ]), 
                                        k = 1
                                    ) #<TODO># k is the degree of the smoothing spline. Must be 1 <= k <= 5. Here we spline x as a funtion of y.
                                      #<TODO># PWV = 1.262mm, Zenith, Figure~4.11 of \url{https://www.iram.fr/IRAMFR/ARC/documents/cycle5/ALMA_Cycle5_Technical_Handbook-Final.pdf}
                        t_Tsys = t_Tsys_spl(Frequency)
                    elif t_Bandnumb == 5:
                        t_Tsys_spl = InterpolatedUnivariateSpline(
                                        numpy.array([162.0, 170.0, 175.0, 180.0, 183.0, 185.0, 187.0, 190.0, 195.0, 200.0, 205.0, 210.0, 215.0]), 
                                        numpy.array([40,    40.0,  50.0,  80.0,  210,   130,   80,    60,    50,    50,    55,    65,    65.0]), 
                                        k = 1
                                    ) #<TODO># k is the degree of the smoothing spline. Must be 1 <= k <= 5. Here we spline x as a funtion of y.
                                      #<TODO># PWV = 0.5mm, Zenith, Figure~4.15 of \url{https://www.iram.fr/IRAMFR/ARC/documents/cycle5/ALMA_Cycle5_Technical_Handbook-Final.pdf}
                        t_Tsys = t_Tsys_spl(Frequency)
                    elif t_Bandnumb == 6:
                        t_Tsys = 95.0 if(Frequency<220) else 120.0 #<TODO># 
                    elif t_Bandnumb == 7:
                        t_Tsys = (Frequency-275)/(350-275)*(150.0-120.0)+120.0
                        if (Frequency>316 and Frequency<334): t_Tsys = 200.0
                        if (Frequency>320 and Frequency<330): t_Tsys = 999.0
                    elif t_Bandnumb == 8:
                        t_Tsys = 500.0
                        if (Frequency>390 and Frequency<420): t_Tsys = 350.0
                        if (Frequency>425-5 and Frequency<425+5): t_Tsys = 999.0
                        if (Frequency>447-5 and Frequency<447+5): t_Tsys = 999.0
                        if (Frequency>475-5 and Frequency<475+5): t_Tsys = 999.0
                        if (Frequency>487-5 and Frequency<487+5): t_Tsys = 999.0
                    elif t_Bandnumb == 9:
                        pass
                    elif t_Bandnumb == 10:
                        pass
                # 
                # determine Tsys for VLA
                # 
                elif Telescope.upper().find('VLA')>=0:
                    t_Telescop = 'VLA'
                    Diameter = 25.0 # https://www.nrao.edu/pr/2000/vla20/background/vlafacts/
                    t_Beamsize = calc_BeamSize(Frequency, Diameter) # VLA 25m
                    t_Nant = 27
                    t_Dant = Diameter
                    t_Aant = numpy.pi * (t_Dant/2.0)**2
                    t_Tsys = 100.0 #<TODO>#
                    t_eta_ap = 0.5 #<TODO># 
                    if Frequency>=1.0 and Frequency<2.0:
                        t_eta_ap = 0.45
                        t_Tsys = 26.0 # https://arxiv.org/pdf/0909.1585.pdf, Table 1
                    elif Frequency>=2.0 and Frequency<4.0:
                        t_eta_ap = 0.62
                        t_Tsys = 29.0 # https://arxiv.org/pdf/0909.1585.pdf, Table 1
                    elif Frequency>=4.0 and Frequency<8.0:
                        t_eta_ap = 0.60
                        t_Tsys = 31.0 # https://arxiv.org/pdf/0909.1585.pdf, Table 1
                    elif Frequency>=8.0 and Frequency<12.0:
                        t_eta_ap = 0.56
                        t_Tsys = 34.0 # https://arxiv.org/pdf/0909.1585.pdf, Table 1
                    elif Frequency>=12.0 and Frequency<18.0:
                        t_eta_ap = 0.54
                        t_Tsys = 39.0 # https://arxiv.org/pdf/0909.1585.pdf, Table 1
                    elif Frequency>=18.0 and Frequency<26.5:
                        t_eta_ap = 0.51
                        t_Tsys = 54.0 # https://arxiv.org/pdf/0909.1585.pdf, Table 1
                    elif Frequency>=26.5 and Frequency<40.0:
                        t_eta_ap = 0.39
                        #t_Tsys = 45.0 # https://arxiv.org/pdf/0909.1585.pdf, Table 1
                        #t_Tsys = 50.0 # http://www.phys.unm.edu/~gbtaylor/IAS/talks_pdf/Perley_Brisken_EVLAUpdate.pdf -- or -- http://www.phys.unm.edu/~gbtaylor/IAS/originals/Perley:Brisken-EVLAUpdate.ppt
                        t_Tsys = 50.5 # matched VLA ETC (https://obs.vla.nrao.edu/ect/) (high elevation, winter weather, 8-bit)
                    elif Frequency>=40.0 and Frequency<50.0:
                        t_eta_ap = 0.34
                        t_Tsys = 66.0 # https://arxiv.org/pdf/0909.1585.pdf, Table 1
                    # 
                    # VLA uses the term SEFD for sensitivity calculation, see -- https://science.nrao.edu/facilities/vla/docs/manuals/oss/performance/sensitivity
                    # which is just SEFD = t_JpK * t_Tsys
                    # VLA staff calibrated that SEFD = 5.62 * Tsys / eta_A (see the above website), where eta_A is the antenna aperture efficiency (i.e., eta_ap in this code) and changes with band (e.g., https://arxiv.org/pdf/0909.1585.pdf, Table 1)
                    # which just means t_JpK = 5.62 / eta_A. 
                    # Our equation in this code gives t_JpK = 14.4 at 33 GHz, fully agree with the VLA value 5.62/0.39=14.4 (eta_ap=0.39 at 33 GHz). 
                    # 
                    t_eta_qc = 0.93 # correlator efficiency (~0.93 with the use of the 8-bit samplers) -- https://science.nrao.edu/facilities/vla/docs/manuals/oss/performance/sensitivity
                # 
                # determine Tsys for any t_Telescope with user-defined Diameter
                # 
                elif Diameter>0:
                    t_Telescop = Telescope
                    t_Beamsize = calc_BeamSize(Frequency, Diameter)
                    t_Bandnumb = -1
                    t_Dant = Diameter
                    t_Aant = numpy.pi * numpy.power(Diameter/2.0,2)
                    t_eta_ap = 0.6 # 0.75 #<TODO># dish area aperture coefficient affecting Jy/K
                    t_eta_qc = 0.9 # assuming a correlator efficiency of 0.9
                # 
                # 
                # 
                # Overwriting according to user inputs
                # 
                if ~numpy.isnan(Nant):
                    if Nant>0:
                        t_Nant = Nant
                if ~numpy.isnan(Tsys[i_Tsys]):
                    if Tsys[i_Tsys]>0.0:
                        t_Tsys = float(Tsys[i_Tsys])
                if ~numpy.isnan(Tint[i_Tint]):
                    if Tint[i_Tint]>0.0:
                        t_Tint = float(Tint[i_Tint])
                if ~numpy.isnan(eta_ap):
                    if eta_ap>0.0:
                        t_eta_ap = eta_ap
                if ~numpy.isnan(eta_mb):
                    if eta_mb>0.0:
                        t_eta_qc = eta_mb
                # 
                # If t_JpK could not be determined but the user input eta_ap
                if numpy.isnan(t_JpK):
                    if Verbose:
                        print('Calculating Jy/K ...')
                    if not numpy.isnan(t_eta_ap):
                        if Verbose:
                            print('Calculating Jy/K with eta_ap = %s ...'%(t_eta_ap))
                        t_JpK = calc_JanskyPerKelvin(t_eta_ap * t_Aant, Frequency, t_Dant)
                # 
                if t_eta_qc is not numpy.nan and t_JpK is not numpy.nan and t_Tsys is not numpy.nan and t_Tint is not numpy.nan:
                    # rms = ( 2 * k_B * Tsys ) / ( Aeff * sqrt( N * (N-1) * BW * Tint * Npol) )
                    if t_Nant > 1:
                        rms = ( float(t_JpK) * float(t_Tsys) ) / ( float(t_eta_qc) * numpy.sqrt(float(t_Nant)*float(t_Nant-1)*float(t_Tint)*float(Bandwidth)*1e9*float(Npol)) ) * 1e3 # mJy
                    else:
                        rms = ( float(t_JpK) * float(t_Tsys) ) / ( float(t_eta_qc) * numpy.sqrt(float(t_Tint)*float(Bandwidth)*1e9*float(Npol)) ) * 1e3 # mJy -- single dish mode
                    if Verbose:
                        print("")
                        print("Telescope = %s"%(t_Telescop))
                        print("Weather = %s"%(Weather))
                        print("Bandnumber = %s"%(t_Bandnumb))
                        print("Frequency = %s GHz"%(Frequency))
                        print("Bandwidth = %s GHz"%(Bandwidth))
                        print("Velowidth = %s km/s"%(Velowidth))
                        print("Beamsize = %s arcsec"%(t_Beamsize))
                        print("Jy/K = %s"%(t_JpK))
                        print("Nant = %s"%(t_Nant))
                        print("Npol = %s"%(Npol))
                        print("Tsys = %s K"%(t_Tsys))
                        print("Tint = %s s"%(t_Tint))
                        print("rms = %s mJy"%(rms))
                else:
                    print("")
                    print("Sorry! Could not determine eta and Jy/K and Tsys for Telescope %s at Frequency %0.6f GHz at Band %s!"%(Telescope, Frequency, t_Bandnumb))
                # 
                # output item --> output 1d array --> output 2d array
                Output_item = {'Telescope':t_Telescop, 'Bandnumber':t_Bandnumb, 'Bandwidth':Bandwidth, 'Frequency':Frequency, 
                                'BeamSize':t_Beamsize, 
                                'JpK':t_JpK, 'Tsys':t_Tsys, 
                                'eta_qc':t_eta_qc, 'eta_ap':t_eta_ap, 'Nant':t_Nant, 'Npol':Npol, 'Tint':t_Tint, 
                                'rms':rms,
                              }
                #print(Output_item)
                # 
                # next
            Output_1d.append(Output_item)
        Output_2d.append(Output_1d)
    # 
    Output_data = Output_2d
    # 
    if len(Tsys) == 1:
        Output_data = [x[0] for x in Output_data]
    # 
    if len(Tint) == 1:
        Output_data = Output_data[0]
    # 
    return Output_data
            







def convert_flux2lprm(S_Jy_km_s, rest_freq_GHz, z = 0.0, dL = 0.0):
    # convert flux [Jy km/s] to lumin prime [K km s-1 pc2]
    if dL <= 0.0:
        lumdist_Mpc = cosmo.luminosity_distance(z).value # Mpc
    else:
        lumdist_Mpc = dL
    L_K_km_s__1_pc_2 = numpy.array(S_Jy_km_s) * 3.25e7 * lumdist_Mpc**2 / numpy.array(rest_freq_GHz)**2 / (1.0+z)
    return L_K_km_s__1_pc_2


def convert_lprm2flux(L_K_km_s__1_pc_2, rest_freq_GHz, z = 0.0, dL = 0.0):
    # convert lumin prime [K km s-1 pc2] to flux [Jy km/s]
    if dL <= 0.0:
        lumdist_Mpc = cosmo.luminosity_distance(z).value # Mpc
    else:
        lumdist_Mpc = dL
    S_Jy_km_s = numpy.array(L_K_km_s__1_pc_2) / 3.25e7 / lumdist_Mpc**2 * numpy.array(rest_freq_GHz)**2 * (1.0+z)
    return S_Jy_km_s


def convert_flux2lsun(S_Jy_km_s, rest_freq_GHz, z = 0.0, dL = 0.0):
    # convert flux [Jy km/s] to luminosity [L_sun]
    # https://1054.github.io/Wiki/radio_line_brightness_temperature/
    if dL <= 0.0:
        lumdist_Mpc = cosmo.luminosity_distance(z).value # Mpc
    else:
        lumdist_Mpc = dL
    L_L_sun = numpy.array(S_Jy_km_s) * 1.0339577e-3 * lumdist_Mpc**2 * numpy.array(rest_freq_GHz) / (1.0+z)
    return L_L_sun


def convert_lsun2flux(L_Lsun, rest_freq_GHz, z = 0.0, dL = 0.0):
    # convert flux [Jy km/s] to luminosity [L_sun]
    # https://1054.github.io/Wiki/radio_line_brightness_temperature/
    if dL <= 0.0:
        lumdist_Mpc = cosmo.luminosity_distance(z).value # Mpc
    else:
        lumdist_Mpc = dL
    S_Jy_km_s = numpy.array(L_Lsun) / 1.0339577e-3 / lumdist_Mpc**2 / numpy.array(rest_freq_GHz) * (1.0+z)
    return S_Jy_km_s


def convert_lprm2lsun(L_K_km_s__1_pc_2, rest_freq_GHz):
    # convert lumin prime [K km/s pc2] to luminosity [L_sun]
    L_L_sun = L_K_km_s__1_pc_2 * 3.1814084e-11 * numpy.array(rest_freq_GHz)**3 # https://1054.github.io/Wiki/radio_line_brightness_temperature/
    return L_L_sun


def convert_lsun2lprm(L_L_sun, rest_freq_GHz):
    # convert luminosity [L_sun] to lumin prime [K km/s pc2]
    L_K_km_s__1_pc_2 = L_L_sun / 3.1814084e-11 / numpy.array(rest_freq_GHz)**3 # https://1054.github.io/Wiki/radio_line_brightness_temperature/
    return L_K_km_s__1_pc_2


def get_CO_excitation_ladder_for_BzKs(Jansky_scale = True):
    # see Daddi2015 Fig.10 BzK-average
    ladder = []
    ladder.append(0.193)
    ladder.append(0.59)
    ladder.append(0.73)
    ladder.append(1.00)
    ladder.append(1.12)
    ladder.append(0.85)
    ladder.append(0.50)
    ladder.append(0.20)
    Jscale = numpy.array(ladder)
    if Jansky_scale is False:
        Jscale = numpy.arange(1,len(ladder)+1)
        Jscale = Jscale**2
        ladder = ladder / Jscale
    return ladder


def calc_CII_based_on_DeLooze2011(IR_luminosity, set_also_output_line_luminosity_in_solar_unit = False):
    # arXiv:1106.1643v1 
    # Table 4 and Figure 6 and Equation 8
    # Valid within -2 < logSFR(UV+24um) < 2.2
    # 
    # -- computing with IDL
    # SFR (Kroupa IMF) [Msun/yr] = ( L_CII [erg/s] )^0.983 / 1.028e40
    # SFR (Kroupa IMF) [Msun/yr] = SFR (Salpeter IMF) [Msun/yr] / 1.51
    # SFR (Salpeter IMF) [Msun/yr] = L_TIR [erg/s] / 2.2e43 = L_TIR [Lsun] / 5.8e9 -- Kennicutt 1998 ApJ
    # => L_TIR [Lsun] = ( L_CII [erg/s]                                                           )^0.983 / 1.028D40 * 1.51 * 5.8D9 ; computing with IDL
    #                 = ( L_CII [Lsun] * 2.2e43 / 5.8e9                                           )^0.983 / 1.028D40 * 1.51 * 5.8D9
    #                 = ( LPrm_CII [K km s-1 pc2] * 3.1814084D-11 * 1900.53690^3 * 2.2D43 / 5.8D9 )^0.983 / 1.028D40 * 1.51 * 5.8D9
    #                 = ( LPrm_CII [K km s-1 pc2] * 0.21839784                   * 2.2D43 / 5.8D9 )^0.983 / 1.028D40 * 1.51 * 5.8D9
    #                 = ( LPrm_CII [K km s-1 pc2] * 8.2840560D+32                                 )^0.983 * 8.5194552D-31
    #                 = ( LPrm_CII [K km s-1 pc2])^0.983 * 8.2840560D+32^0.983 * 8.5194552D-31
    #                 = ( LPrm_CII [K km s-1 pc2])^0.983 * 194.55575172665547
    # -- note that (3.1814084D-11 * 1900.53690^3) = 0.21839784
    # 
    # return line luminosity in units of [K km s-1 pc2]
    # 
    N = 0.983
    A = numpy.log10(194.55575172665547) # Slope is 0.983, Intercept see the above computing with IDL
    LineLPrm = 10**((numpy.log10(IR_luminosity)-A)/N)
    LineLsun = LineLPrm * 0.21839784
    if set_also_output_line_luminosity_in_solar_unit:
        return LineLPrm, LineLsun
    return LineLPrm


def calc_CII_based_on_dzliu_model_2017a(IR_luminosity, set_also_output_line_luminosity_in_solar_unit = False):
    # calculate the CII 158um line luminosities for a given total IR luminosity 
    # when L_TIR < 1e11, we use calc_DeLooze2011_CII(), 
    # otherwise we consider a redshift/luminosity-dependent decaying, which can fit WangRan2013 data (http://adsabs.harvard.edu/abs/2013ApJ...773...44W)
    # -- From WangRan 2013 Fig. 4, IR=1e11, log(LumiCII/LumiIR)=0.003; IR=1e13, log(LumiCII/LumiIR)=0.0004~0.0006, so slope in log is about ~0.335?
    N = 0.983
    A = numpy.log10(194.55575172665547) # Slope is 0.983, Intercept see the above computing with IDL
    LineLPrm = 10**((numpy.log10(IR_luminosity)-A)/N)
    LineLsun = LineLPrm * 0.21839784
    # Apply redshift/luminosity-dependent decaying <20160903> <TODO> assuming Bethermin 2015 Sec.4.3 http://arxiv.org/pdf/1409.5796.pdf
    #_dzliu_Decaying = numpy.array(IR_luminosity)*0.0 + 1.0
    #_dzliu_Mask = (numpy.array(IR_luminosity)>1e10)
    #_dzliu_Decaying[_dzliu_Mask] = (numpy.array(IR_luminosity)[_dzliu_Mask]/1e11)**0.335
    _dzliu_Decaying = (IR_luminosity/1e11)**0.335 if (IR_luminosity>1e10) else 1.0
    _dzliu_Decaying = 1.0 / _dzliu_Decaying
    LineLPrm = LineLPrm * _dzliu_Decaying
    LineLsun = LineLsun * _dzliu_Decaying
    if set_also_output_line_luminosity_in_solar_unit:
        return LineLPrm, LineLsun
    return LineLPrm


def calc_OIII_based_on_DeLooze2014(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = False):
    # arXiv:1402.4075v2
    # Table 3 and Fig. 10
    # Valid within -3 < logSFR(UV+24um) < 3
    # 
    # -- computing with IDL
    # SFR (Kroupa IMF) [Msun/yr] = ( L_OIII [L_sun] )^1.12 * 10**(-7.48)
    # SFR (Kroupa IMF) [Msun/yr] = SFR (Salpeter IMF) [Msun/yr] / 1.51
    # SFR (Salpeter IMF) [Msun/yr] = L_TIR [erg/s] / 2.2e43 = L_TIR [Lsun] / 5.8e9 -- Kennicutt 1998 ApJ
    # => L_TIR [Lsun] = ( SFR (Kroupa IMF) [Msun/yr]                         ) * 5.8e9 * 1.51
    #                 = ( L_OIII [Lsun]                                      )^1.12 * 10^(-7.48) * 5.8e9 * 1.51
    #                 = ( LPrm_OIII [K km s-1 pc2] * 3.1814084D-11 * 3393.^3 )^1.12 * 290.00464
    #                 = ( LPrm_OIII [K km s-1 pc2] * 1.2427134               )^1.12 * 290.00464
    #                 = ( LPrm_OIII [K km s-1 pc2]                           )^1.12 * 1.2427134^1.12 * 290.00464
    #                 = ( LPrm_OIII [K km s-1 pc2]                           )^1.12 * 369.91373
    # 
    # return line luminosity in units of [K km s-1 pc2]
    # 
    if line_J_up == 1:
        # for OIII 88um 3P1-3P0
        N = 1.12
        A = numpy.log10(369.91373) # Slope is 1.12, Intercept see the above computing with IDL
        LineLPrm = 10**((numpy.log10(IR_luminosity)-A)/N)
        LineLsun = LineLPrm * 1.2427134
        if set_also_output_line_luminosity_in_solar_unit:
            return LineLPrm, LineLsun
        return LineLPrm
    else:
        raise ValueError('Error! calc_OIII_based_on_DeLooze2014() can only compute OIII 88um. Please input line_index = 0.')
    return []


def calc_OIII_based_on_dzliu_model_2017a(IR_luminosity, line_J_up = 1, starburstiness = 0.0, set_also_output_line_luminosity_in_solar_unit = False):
    # calculate the OIII 88um or 52um line luminosities for a given total IR luminosity 
    # 
    if line_J_up == 1:
        # OIII 88um (3P1-3P0)
        LineLPrm, LineLsun = calc_OIII_based_on_DeLooze2014(IR_luminosity, 1, True)
    elif line_J_up == 2:
        # OIII 52um (3P2-3P1)
        LineLPrm, LineLsun = calc_OIII_based_on_DeLooze2014(IR_luminosity, 1, True)
        LineLsun = LineLPrm * 3.1814084e-11 * 5786.**3
        print('*** CrabPdBI.py ***')
        print('Warning! calc_OIII_based_on_dzliu_model_2017a() can only compute OIII 88um for now. Here we assume OIII 63um has the same line brightness temperature (TODO)!')
        print('***')
    else:
        raise ValueError('Error! calc_OIII_based_on_dzliu_model_2017a() can only compute OIII 88um (3P1-3P0). Please input line_J_up = 1.')
    # 
    # Apply luminosity-dependent decaying <20160903> <TODO> 
    _dzliu_Decaying = (IR_luminosity/1e11)**(0.335*starburstiness) if (IR_luminosity>1e10) else 1.0 # 1.0 at LIR 1e10 to 0.1**0.335=0.46 at LIR 1e11. <TODO><20181005>
    LineLPrm = LineLPrm / (_dzliu_Decaying) #<20181012>$ it is only significant when it is starburst
    LineLsun = LineLsun / (_dzliu_Decaying) #<20181012>$ it is only significant when it is starburst
    if set_also_output_line_luminosity_in_solar_unit:
        return LineLPrm, LineLsun
    return LineLPrm


def calc_NII_based_on_Zhao2016(IR_luminosity, line_J_up, IR_color, set_also_output_line_luminosity_in_solar_unit = False):
    # calculate the NII 205um line luminosities for a given total IR luminosity 
    # calc_Zhao2016_NII LTIR NII_J_up z R70160 # all input are in linear form
    # 
    line_J_up_max = 2
    if line_J_up > line_J_up_max: 
        print('Error! calc_NII_based_on_Zhao2016() does not support line_J_up>=%d!' % (line_J_up_max) )
        sys.exit()
    N = numpy.zeros(line_J_up_max+1) # leave N[0] unused
    A = numpy.zeros(line_J_up_max+1) # leave N[0] unused
    N[1] = 1.00; A[1] = 3.83+1.26*numpy.log10(IR_color)+1.86*numpy.log10(IR_color)**2+0.90*numpy.log10(IR_color)**3 # see Zhao Yinghe, Lu Nanyao et al. 2016 Eq(1)
    N[2] = 1.00; A[2] = 99.9+1.26*numpy.log10(IR_color)+1.86*numpy.log10(IR_color)**2+0.90*numpy.log10(IR_color)**3 # TODO: No correlation for [NII]122um???
    # 
    LineLPrm = 10**((numpy.log10(IR_luminosity/1.3)-A[line_J_up])/N[line_J_up]) # IR_luminosity/1.3 converts 8-1000um to 40-500um IR luminosity.
    # 
    if set_also_output_line_luminosity_in_solar_unit:
        LineRestFreq = numpy.zeros(line_J_up_max+1)
        LineRestFreq[1] = 1461.13141
        LineRestFreq[2] = 2459.38010
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq[line_J_up])**3
        return LineLPrm, LineLsun
    return LineLPrm


def calc_OI_based_on_dzliu_model_2017a(IR_luminosity, starburst, line_J_up = 2, set_also_output_line_luminosity_in_solar_unit = False):
    # calculate the OI 63um (63.18um) (3P1-3P2) line luminosities for a given total IR luminosity 
    # In Horsehead Nebula, LineLumin_OI63 / IR_Lumin = 4e-3, Goicoechea et al. 2009, https://arxiv.org/pdf/0906.0691.pdf
    # In 77 YSOs, Riviere-Marichalar et al. 2016, https://arxiv.org/pdf/1607.07991.pdf
    # In six unlensed z~1 LESS SMGs, Coppin et al. 2012, MNRAS, 427, 520–532 (2012), doi:10.1111/j.1365-2966.2012.21977.x
    #     LineLumin_OI63 / IR_Lumin ~ 6e-3 to 3e-2 for z~1 LESS SMGs, 
    #     LineLumin_OI63 / IR_Lumin ~ 8e-4 to 4e-3 for local HII galaxies, 
    #     LineLumin_OI63 / IR_Lumin ~ 2e-2 to 4e-3 for local Seyfert/QSOs/LINERs, see their Figure 3. 
    #     LineLumin_OI63 / IR_Lumin = 2e-4 in Mrk231 and Arp220, almost representing the lowest values. 
    # So here I set this ratio to 2e-4 for most extreme starbursts (low mass?) -- starburst = 1.0
    #     and to 2e-3 for local SFGs (not so massive) -- starburst = 0.2
    #     and to 1e-2 for really massive MS at high-z -- starburst = 0.0
    if line_J_up == 1:
        # OI 145um (3P0-3P1)
        f4spl = numpy.log10([2e-4,2e-4,2e-3,1e-2,1e-2])
        sb4spl = numpy.array([10.0,1.0,0.2,0.0,-10.0])
        f = interp1d(sb4spl,f4spl)(starburst)
        f = 10**f # this is LineLumin_OI63 / IR_Lumin
        LineLPrm = f * IR_luminosity
        LineRestFreq = calc_radio_line_frequencies('[OI](3P%d-3P%d)'%(line_J_up-1,line_J_up))
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq)**3
        print('*** CrabPdBI.py ***')
        print('Warning! calc_OIII_based_on_dzliu_model_2017a() can only compute OI 63um (3P1-3P2) for now. Here we assume OI 145um (3P0-3P1) has the same line brightness temperature, though this is not true (TODO)!')
        print('***')
        if set_also_output_line_luminosity_in_solar_unit:
            return LineLPrm, LineLsun
        return LineLPrm
    elif line_J_up == 2:
        # OI 63um (3P1-3P2)
        f4spl = numpy.log10([2e-4,2e-4,2e-3,1e-2,1e-2])
        sb4spl = numpy.array([10.0,1.0,0.2,0.0,-10.0])
        f = interp1d(sb4spl,f4spl)(starburst)
        f = 10**f # this is LineLumin_OI63 / IR_Lumin
        LineLPrm = f * IR_luminosity
        LineRestFreq = calc_radio_line_frequencies('[OI](3P%d-3P%d)'%(line_J_up-1,line_J_up))
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq)**3
        if set_also_output_line_luminosity_in_solar_unit:
            return LineLPrm, LineLsun
        return LineLPrm
    else:
        raise ValueError('Error! calc_OI_based_on_dzliu_model_2017a() can only compute OI 63um (3P1-3P2). Please input line_J_up = 2.')
    return []


def calc_HCN_based_on_Gao2004(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False):
    # Gao & Solomon 2004
    # LIR = LHCN(1-0) ⁄ 900 L[􏰤sun(Kkms-1pc2)-1]
    N=1.0; A = 2.9
    LineLPrm = 10**((numpy.log10(IR_luminosity-A))/N) # total 8-1000um IR_luminosity
    if set_also_output_line_luminosity_in_solar_unit:
        LineRestFreq = 88.6316023
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq)**3
        return LineLPrm, LineLsun
    return LineLPrm


def calc_HCN_based_on_Zhang2014(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False):
    # Zhang 2014 ApJL 784:L31
    # log(LIR) = 1.00(±0.04)×log(L′HCN43) + 3.67(±0.28); r = 0.97
    N=1.0; A = 3.67
    LineLPrm = 10**((numpy.log10(IR_luminosity-A))/N) # total 8-1000um IR_luminosity
    if set_also_output_line_luminosity_in_solar_unit:
        LineRestFreq = 354.5054779
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq)**3
        return LineLPrm, LineLsun
    return LineLPrm


def calc_CS_based_on_Zhang2014(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False):
    # Zhang 2014 ApJL 784:L31
    # log(LIR) = 0.95(±0.04)×log(L′CS76) + 4.33(±0.28); r = 0.99
    N=0.95; A = 4.33
    LineLPrm = 10**((numpy.log10(IR_luminosity-A))/N) # total 8-1000um IR_luminosity
    if set_also_output_line_luminosity_in_solar_unit:
        LineRestFreq = 342.8828503 # http://home.strw.leidenuniv.nl/~moldata/datafiles/cs@lique.dat
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq)**3
        return LineLPrm, LineLsun
    return LineLPrm


def calc_CO_based_on_Daddi2010(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False):
    # 
    # calculate the CO luminosity for a given total IR luminosity
    # CO luminosity is in unit of K km s-1 pc2, IR luminosity is in unit of solar luminosity. 
    # input $1 is LTIR (in linear not in log)
    # input $2 is J_upper
    # input $3 is z
    # input $4 is starburst-ness: 1.0 for strong SB, 0.0 for MS. Default is 0.0.
    # #<Modified><20160314># input $5 is excitation: if unset then same as starburst-ness: 1.0 for thermalized excitation, 0.0 for HERACLES/z2BzK exc. 
    # input $5 is excitation: if unset then use BzK: 1.0 for BzK excitation. 
    # 
    # see paper http://arxiv.org/pdf/1003.3889
    #     equation (1) disk sequence: lg_LTIR = 1.31 * lg_MH2 - 2.09
    #                  starburst seq: lg_LTIR = 1.31 * lg_MH2 - 2.09 + 1.1  (1.1 dex see caption of figure 1)
    #                  and they are using alpha_CO = 3.6 for BzK, 4.6 for local spirals, 0.8 for local LRG/SMG
    # 
    line_J_up_max = 1
    line_J_up = 1
    #if line_J_up > line_J_up_max: 
    #    print('Error! calc_CO_based_on_Daddi2010() only supports CO(1-0)!' )
    #    sys.exit()
    N = numpy.zeros(line_J_up_max+1) # leave N[0] unused
    A = numpy.zeros(line_J_up_max+1) # leave N[0] unused
    N[0] = 1.31; A[0] = -2.09
    N[1] = 1.31; A[1] = -2.09 + 1.1
    # 
    MH2_0 = 10**((numpy.log10(IR_luminosity)-A[0])/N[0]) # IR_luminosity/1.3 converts 8-1000um to 40-500um IR luminosity.
    MH2_1 = 10**((numpy.log10(IR_luminosity)-A[1])/N[1]) # IR_luminosity/1.3 converts 8-1000um to 40-500um IR luminosity.
    # 
    #alphaCO = starburstiness * (4.6 - 0.8) + 0.8
    LineLPrm = starburstiness * (MH2_0/4.6 - MH2_1/0.8) + MH2_0/4.6 # weighted-average
    # 
    if set_also_output_line_luminosity_in_solar_unit:
        LineRestFreq = 115.2712018
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq)**3
        return LineLPrm, LineLsun
    return LineLPrm


def calc_CO_based_on_Sargent2014(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = False):
    # calculate the CO luminosity for a given total IR luminosity
    # CO luminosity is in unit of K km s-1 pc2, IR luminosity is in unit of solar luminosity. 
    # see paper doi:10.1088/0004-637X/793/1/19
    #     equation (1) disk sequence: lg LPrmCO10 = 0.54 + 0.81 * lg_LTIR
    #                  starburst seq: lg LPrmCO10 = 0.08 + 0.81 * lg_LTIR
    line_J_up_max = 1
    line_J_up = 1
    #if line_J_up > line_J_up_max: 
    #    print('Error! calc_CO_based_on_Daddi2010() only supports CO(1-0)!' )
    #    sys.exit()
    N = numpy.zeros(line_J_up_max+1) # leave N[0] unused
    A = numpy.zeros(line_J_up_max+1) # leave N[0] unused
    N[0] = 0.81; A[0] = 0.54 # MS
    N[1] = 0.81; A[1] = 0.08 # SB
    # 
    LineLPrm_0 = 10**(A[0] + numpy.log10(IR_luminosity) * N[0])
    LineLPrm_1 = 10**(A[1] + numpy.log10(IR_luminosity) * N[1])
    # 
    LineLPrm = starburstiness * (LineLPrm_1 - LineLPrm_0) + LineLPrm_0 # weighted-average
    # 
    if set_also_output_line_luminosity_in_solar_unit:
        LineRestFreq = 115.2712018
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq)**3
        return LineLPrm, LineLsun
    return LineLPrm


def calc_CO_based_on_Liudz2015(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = False):
    # arXiv:1504.05897
    # 
    line_J_up_max = 15
    if line_J_up > line_J_up_max: 
        print('Error! calc_CO_based_on_Liudz2015() does not support line_J_up>=%d!' % (line_J_up_max) )
        sys.exit()
    N = numpy.zeros(line_J_up_max+1) # leave N[0] unused
    A = numpy.zeros(line_J_up_max+1) # leave N[0] unused
    N[1] = 1.06; A[1] = 1.49+numpy.log10(0.8) #<TODO># using non-linear slope #<TODO># using CO(4-3) as a lower limit for now
    N[2] = 1.06; A[2] = 1.49+numpy.log10(0.8) #<TODO># using non-linear slope #<TODO># using CO(4-3) as a lower limit for now
    N[3] = 1.06; A[3] = 1.49+numpy.log10(0.8) #<TODO># using non-linear slope #<TODO># using CO(4-3) as a lower limit for now
    N[4] = 1.06; A[4] = 1.49 #<TODO># using non-linear slope
    N[5] = 1.07; A[5] = 1.71 #<TODO># using non-linear slope
    N[6] = 1.10; A[6] = 1.79 #<TODO># using non-linear slope
    N[7] = 1.03; A[7] = 2.62 #<TODO># using non-linear slope
    #N[1] = 1.00; A[1] = 1.96 #<TODO># using linear slope #<TODO># using CO(4-3) as a lower limit for now
    #N[2] = 1.00; A[2] = 1.96 #<TODO># using linear slope #<TODO># using CO(4-3) as a lower limit for now
    #N[3] = 1.00; A[3] = 1.96 #<TODO># using linear slope #<TODO># using CO(4-3) as a lower limit for now
    #N[4] = 1.00; A[4] = 1.96 #<TODO># using linear slope
    #N[5] = 1.00; A[5] = 2.27 #<TODO># using linear slope
    #N[6] = 1.00; A[6] = 2.56 #<TODO># using linear slope
    #N[7] = 1.00; A[7] = 2.86 #<TODO># using linear slope
    N[8]  = 1.00; A[8]  = 3.04 #<TODO># using linear slope
    N[9]  = 1.00; A[9]  = 3.20 #<TODO># using linear slope
    N[10] = 1.00; A[10] = 3.38 #<TODO># using linear slope
    N[11] = 1.00; A[11] = 3.56 #<TODO># using linear slope
    N[12] = 1.00; A[12] = 3.77 #<TODO># using linear slope
    N[13] = 1.00; A[13] = 3.98 #<TODO># extrapolation!!!
    N[14] = 1.00; A[14] = 4.19 #<TODO># extrapolation!!!
    N[15] = 1.00; A[15] = 4.40 #<TODO># extrapolation!!!
    # 
    LineLPrm = 10**((numpy.log10(IR_luminosity/1.3)-A[line_J_up])/N[line_J_up]) # IR_luminosity/1.3 converts 8-1000um to 40-500um IR luminosity.
    # 
    if set_also_output_line_luminosity_in_solar_unit:
        LineRestFreq = numpy.zeros(line_J_up_max+1)
        LineRestFreq[1] = 115.2712018
        LineRestFreq[2] = 230.5380000
        LineRestFreq[3] = 345.7959899
        LineRestFreq[4] = 461.0407682
        LineRestFreq[5] = 576.2679305
        LineRestFreq[6] = 691.4730763
        LineRestFreq[7] = 806.6518060
        LineRestFreq[8] = 921.7997000
        LineRestFreq[9] = 1036.9123930
        LineRestFreq[10] = 1151.9854520
        LineRestFreq[11] = 1267.0144860
        LineRestFreq[12] = 1381.9951050
        LineRestFreq[13] = 1496.9229090
        LineRestFreq[14] = 1611.7935180
        LineRestFreq[15] = 1726.6025057
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq[line_J_up])**3
        return LineLPrm, LineLsun
    return LineLPrm


def calc_CI_based_on_Liudz2015(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = False):
    # dzliu own fitting
    #   y: log_L_FIR_50_500um
    #   x: log_LPrime_3P1_3P0
    #   y = 0.065 * x**3 - 1.921 * x**2 + 19.866 * x - 59.322
    # see -- '/Volumes/GoogleDrive/Team Drives/SpireLines/Plot/Plot_Correlation_CI_LIR/Plot_FIR_CI_3P1_3P0_v1.pdf'
    # see -- '/Volumes/GoogleDrive/Team Drives/SpireLines/Plot/Plot_Correlation_CI_LIR/Plot_FIR_CI_3P2_3P1_v1.pdf'
    #  
    line_J_up_max = 2
    if line_J_up > line_J_up_max: 
        print('Error! calc_CI_based_on_Liudz2015() does not support line_J_up>=%d!' % (line_J_up_max) )
        sys.exit()
    # 
    x = [None]*(line_J_up_max+1) # x is log10(LineLPrm)
    y = [None]*(line_J_up_max+1) # y is log10(IR_luminosity)
    f = [None]*(line_J_up_max+1) # f is log10(IR_luminosity/LineLPrm)
    x[1] = numpy.arange(6.8, 10.55, 0.01)
    x[2] = numpy.arange(6.0, 9.55, 0.01)
    y[1] = 0.0653741952625 * x[1]**3 - 1.92089044289 * x[1]**2 + 19.8655338987 * x[1] - 59.3221991296 # '/Volumes/GoogleDrive/Team Drives/SpireLines/Plot/Plot_Correlation_CI_LIR/datatable_for_CI_3P1_3P0_NumpyFit_fitted_order_3_params.txt'
    y[2] = -0.0458894875722 * x[2]**3 + 0.945193645758 * x[2]**2 - 4.85912193717 * x[2] + 12.6100503599 # '/Volumes/GoogleDrive/Team Drives/SpireLines/Plot/Plot_Correlation_CI_LIR/datatable_for_CI_3P2_3P1_NumpyFit_fitted_order_3_params.txt'
    f[1] = y[1]-x[1] # log10(IR_luminosity) - log10(LineLPrm) = log10(IR_luminosity/LineLPrm)
    f[2] = y[2]-x[2] # log10(IR_luminosity) - log10(LineLPrm) = log10(IR_luminosity/LineLPrm)
    spl = [None]*(line_J_up_max+1)
    y4spl = y[line_J_up].tolist()
    f4spl = f[line_J_up].tolist()
    y4spl.insert(0, 5.0)
    f4spl.insert(0, f4spl[0])
    y4spl.append(15.0)
    f4spl.append(f4spl[-1]) # for values out of valid range, we just copy the edge values for the ratio 'log10(IR_luminosity/LineLPrm)' for now <20181005>.
    spl = InterpolatedUnivariateSpline(y4spl, f4spl, k = 1) #<TODO># k is the degree of the smoothing spline. Must be 1 <= k <= 5. Here we spline x as a funtion of y.
    yy = numpy.log10(IR_luminosity/1.3) # IR_luminosity/1.3 converts 8-1000um to 40-500um IR luminosity.
    LineLPrm = (10**(yy - spl(yy))) # we spline 'log10(IR_luminosity) - log10(LineLPrm)' = 'log10(IR_luminosity/LineLPrm)', so LineLPrm = 10**(yy - ratio). 
    #print('DEBUG: calc_CI_based_on_Liudz2015: spl(yy)=', spl(yy), 'y4spl=', y4spl, 'f4spl=', f4spl)
    # 
    if set_also_output_line_luminosity_in_solar_unit:
        LineRestFreq = calc_radio_line_frequencies('[CI](%d-%d)'%(line_J_up, line_J_up-1))
        LineLsun = LineLPrm * 3.1814084e-11 * (LineRestFreq)**3
        return LineLPrm, LineLsun
    return LineLPrm



def calc_radio_line_flux_from_IR_luminosity(line_name, IR_luminosity, z, starburstiness = 0.0, IR_color = 0.0, verbose = True, return_lprm = False):
    if type(line_name) is not str:
        print('Errro! calc_radio_line_flux_from_IR_luminosity() requires the input line_name to be a string!')
        sys.exit()
    # 
    rest_freq, output_line_name = calc_radio_line_frequencies(line_name, set_output_line_names = True)
    obs_freq = numpy.array(rest_freq) / (1.0+z)
    #print('DEBUG: CrabPdBI::calc_radio_line_flux_from_IR_luminosity(): line_name', line_name)
    #print('DEBUG: CrabPdBI::calc_radio_line_flux_from_IR_luminosity(): output_line_name', output_line_name)
    # 
    if output_line_name.startswith('CO'):
        line_J_up = int(re.sub(r'CO\(([0-9]+)\-([0-9]+)\)', r'\1', output_line_name))
        if line_J_up >= 4:
            line_lprm, line_lsun = calc_CO_based_on_Liudz2015(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = True)
            line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
        elif line_J_up == 1:
            line_lprm, line_lsun = calc_CO_based_on_Sargent2014(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = True)
            line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
        else:
            line_J_up2 = 4
            line_lprm2, line_lsun2 = calc_CO_based_on_Liudz2015(IR_luminosity, 4, set_also_output_line_luminosity_in_solar_unit = True)
            line_flux2 = convert_lprm2flux(line_lprm2, 461.0407682, z)
            #line_J_up2 = 5
            #line_lprm2, line_lsun2 = calc_CO_based_on_Liudz2015(IR_luminosity, 5, set_also_output_line_luminosity_in_solar_unit = True)
            #line_flux2 = convert_lprm2flux(line_lprm2, 576.2679305, z)
            line_lprm1, line_lsun1 = calc_CO_based_on_Sargent2014(IR_luminosity, starburstiness, set_also_output_line_luminosity_in_solar_unit = True)
            line_flux1 = convert_lprm2flux(line_lprm1, 115.2712018, z)
            line_lprm = (line_lprm2-line_lprm1)*float(line_J_up-1)/float(line_J_up2-1) + line_lprm1
            line_lsun = (line_lsun2-line_lsun1)*float(line_J_up-1)/float(line_J_up2-1) + line_lsun1
            line_flux = (line_flux2-line_flux1)*float(line_J_up-1)/float(line_J_up2-1) + line_flux1
            print('DEBUG: CO(4-3) %0.4f CO(1-0) %0.4f [Jy km s-1]' % (line_flux2, line_flux1))
            print('DEBUG: CO(2-1) / CO(1-0) %0.4f [K/K]' % (
                ((line_lprm2-line_lprm1)*float(2-1)/float(line_J_up2-1) + line_lprm1) / 
                ((line_lprm2-line_lprm1)*float(1-1)/float(line_J_up2-1) + line_lprm1)
                ))
            #<TODO># if line is 1<J<4, use an average -- although this may underestimates CO because CO SLED is up-curved.
    elif output_line_name.startswith('[OIII]'):
        line_J_up = int(re.sub(r'\[OIII\]\(([0-9]+)\-([0-9]+)\)', r'\1', output_line_name))
        line_lprm, line_lsun = calc_OIII_based_on_dzliu_model_2017a(IR_luminosity, line_J_up, starburstiness = starburstiness, set_also_output_line_luminosity_in_solar_unit = True)
        line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
    elif output_line_name.startswith('[OI]'):
        line_J_up = int(re.sub(r'\[OI\]\(3P([0-9]+)\-3P([0-9]+)\)', r'\2', output_line_name)) # note the naming: 3P0-3P1, 3P1-3P2
        line_lprm, line_lsun = calc_OI_based_on_dzliu_model_2017a(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = True)
        line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
    elif output_line_name == '[CII](1-0)':
        #line_lprm, line_lsun = calc_CII_based_on_DeLooze2011(IR_luminosity, set_also_output_line_luminosity_in_solar_unit = True)
        line_lprm, line_lsun = calc_CII_based_on_dzliu_model_2017a(IR_luminosity, set_also_output_line_luminosity_in_solar_unit = True)
        line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
    elif output_line_name.startswith('[CI]'):
        line_J_up = int(re.sub(r'\[CI\]\(([0-9]+)\-([0-9]+)\)', r'\1', output_line_name))
        line_lprm, line_lsun = calc_CI_based_on_Liudz2015(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = True)
        line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
    elif output_line_name.startswith('[NII]'):
        line_J_up = int(re.sub(r'\[NII\]\(([0-9]+)\-([0-9]+)\)', r'\1', output_line_name))
        IR_color = IR_color if (IR_color>0.0) else 0.6
        line_lprm, line_lsun = calc_NII_based_on_Zhao2016(IR_luminosity, line_J_up, IR_color, set_also_output_line_luminosity_in_solar_unit = True) # IR_color is S_70um/S_160um[Jy/Jy].
        line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
    elif output_line_name.startswith('HCN'):
        line_J_up = int(re.sub(r'HCN\(([0-9]+)\-([0-9]+)\)', r'\1', output_line_name))
        if line_J_up == 1:
            line_lprm, line_lsun = calc_HCN_based_on_Gao2004(IR_luminosity, line_J_up, set_also_output_line_luminosity_in_solar_unit = True)
            line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
    
    elif output_line_name.startswith('H2O'):
        if output_line_name == 'H2O(3_{1,2}-2_{2,1})':
            line_lprm, line_lsun = calc_CO_based_on_Liudz2015(IR_luminosity, 10, set_also_output_line_luminosity_in_solar_unit = True)
            line_lprm = line_lprm / 3.0
            line_flux = convert_lprm2flux(line_lprm, rest_freq, z)
            print('*** CrabPdBI.py ***')
            print('Warning! calc_radio_line_flux_from_IR_luminosity() we assume '+output_line_name+' has 1/3 the line brightness temperature of CO(10-9) (TODO)!')
            print('***')
    
    else:
        print('Error! calc_radio_line_flux_from_IR_luminosity() could not recognize line_name "%s"' % (line_name) )
        sys.exit()
    # 
    if verbose:
        print('line_name         = %-12s' % ('"'+output_line_name+'"') )
        print('line_redshift     = %-12.4f' % (z) )
        print('line_obsfreq      = %-12.4f  [GHz]' % (obs_freq) )
        print('line_restfreq     = %-12.4f  [GHz]' % (rest_freq) )
        print('IR_luminosity     = %-12.6e  [L_solar]' % (IR_luminosity) )
        print('IR_SFR            = %-12.2f  [M_solar yr-1]' % (IR_luminosity/1e10) )
        print('IR_SFR_log10      = %-12.2f  [M_solar yr-1]' % (numpy.log10(IR_luminosity/1e10)) )
        print('line_luminosity   = %-12.6e  [K km s-1 pc2]' % (line_lprm) )
        print('line_luminosity   = %-12.6e  [L_solar]' % (line_lsun) )
        print('line_flux_density = %-12.8f  [Jy km s-1]' % (line_flux) )
    # 
    if return_lprm:
        return line_flux, line_lprm
    return line_flux

































