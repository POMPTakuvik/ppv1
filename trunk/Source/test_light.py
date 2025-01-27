#!/usr/bin/env python2

"""Test light.c: get_array4d_itaucld_io3_ithetas_iwl_ed0minus(...)

Usage:
python2 test_light.py
"""

# author: Maxime Benoit-Gagne - Takuvik - Canada.
# date of creation: October 23, 2015.
#
# Python from Anaconda.
#
# Interpreter:
# $ python
# Python 2.7.10 |Anaconda 2.4.0 (x86_64)| (default, Oct 19 2015, 18:31:17) 
# [GCC 4.2.1 (Apple Inc. build 5577)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# Anaconda is brought to you by Continuum Analytics.
# Please check out: http://continuum.io/thanks and https://anaconda.org

########### Importing modules ###########
import numpy as np
import light

########### Constants ###########
LUT = "/Volumes/taku-njall/LUTS/Ed0moins_LUT.dat"

########### Future output ###########
ed0minus_ref = 0.003896

########### Compute lut ###########

# Array of 4 dimensions : 						     
# NTAUCLD=8 * NO3=8 * NTHETAS=19 * NBWL=83.				     
# The first dimension is the mean cloud optical thickness.		     
# The second dimension is the total ozone column.			     
# The third dimension is the solar zenith angle.			     
# The fourth dimension is the wavelengths from 290 to 700 by step 5 nm.    
# The values are the downward irradiance just below the water surface      
# from the lookup table.						     
# The units are umol photons*m^-2*s^-1*nm^-1.
array4d_itaucld_io3_ithetas_iwl_ed0minus \
    = np.zeros(shape = (light.NTAUCLD, light.NO3, light.NTHETAS, light.NBWL),
               dtype = np.float32)

light.get_array4d_itaucld_io3_ithetas_iwl_ed0minus(LUT,
                                    array4d_itaucld_io3_ithetas_iwl_ed0minus)

########### Test ###########

ed0minus = array4d_itaucld_io3_ithetas_iwl_ed0minus[1, 1, 1, 1]

if np.allclose(a = ed0minus,
               b = ed0minus_ref,
               rtol = 1e-03):
    print("PASS\n")
else:
    print("FAIL\n")
