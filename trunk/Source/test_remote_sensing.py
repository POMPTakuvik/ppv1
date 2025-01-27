#!/usr/bin/env python2

"""Test remote_sensing.py.

Usage:
python2 test_remote_sensing.py
"""

# author: Maxime Benoit-Gagne - Takuvik - Canada.
# date of creation: November 6, 2015.
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

import Netcdf_tools
from domain.image import image_with_primary_production_pixel

########### constants ###########
NTIMES = 9

########### functions ###########

def fail(nfail):
    """
    Print 'FAIL' and increment nfail.

    Args:
        nfail(int): Number of failed tests until now.
    """
    print("FAIL\n")
    nfail += 1
    return nfail
#############################################################################

def pass_test(npass):
    """
    Print 'PASS' and increment npass.

    Args:
        npass(int): Number of passed tests until now.
    """
    print("PASS\n")
    npass += 1
    return npass
#############################################################################

########### main ###########

nfail = 0
npass = 0

########### test Pixel.__init__(lat, lon, year, month, day) ###########

print("test Pixel.__init__(lat, lon, year, month, day)")

# Latitude.			 
# The units are degrees North.
lat = 68.83912
lat_ref = np.float32(68.83912)
# Longitude.			
# From -180 to 180.		
# The units are degrees East.
lon = -104.9695
lon_ref = np.float32(-104.9695)
year = 2009
year_ref = np.int32(2009)
month = 8
month_ref = np.int32(8)
# Day of month.
day = 21
day_ref = np.int32(21)
# Day of year.
doy_ref = np.int32(233)
# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N_ref = 0

p = image_with_primary_production_pixel.Pixel(lat,
                                              lon,
                                              year,
                                              month,
                                              day)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy_ref \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Pixel.__init__(lat, lon, year, doy) ###########

print("test Pixel.__init__(lat, lon, year, doy)")
# Day of year.
doy = 233
# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N_ref = 0

p = image_with_primary_production_pixel.Pixel(lat,
                                              lon,
                                              year,
                                              doy = doy)

print(p)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month_ref \
   and p.day == day_ref \
   and p.doy == doy_ref \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Pixel.__init__(lat, lon, year, month, day, doy) ###########

print("test Pixel.__init__(lat, lon, year, month, day, doy)")

p = image_with_primary_production_pixel.Pixel(lat,
                                              lon,
                                              year,
                                              month,
                                              day,
                                              doy)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month_ref \
   and p.day == day_ref \
   and p.doy == doy_ref \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Pixel.__init__(lat, lon, year, month, day, ibin45N)
###########

print("test Pixel.__init__(lat, lon, year, month, day, ibin45N)")
# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N = 1
ibin45N_ref = 1

p = image_with_primary_production_pixel.Pixel(lat,
                                              lon,
                                              year,
                                              month,
                                              day,
                                              ibin45N = ibin45N
                                              )

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month_ref \
   and p.day == day_ref \
   and p.doy == doy_ref \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Pixel.__init__(lat, lon, year, doy, ibin45N)
###########

print("test Pixel.__init__(lat, lon, year, doy ibin45N)")
# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N = 1
ibin45N_ref = 1

p = image_with_primary_production_pixel.Pixel(lat,
                                              lon,
                                              year,
                                              doy = doy,
                                              ibin45N = ibin45N
                                              )

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month_ref \
   and p.day == day_ref \
   and p.doy == doy_ref \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Pixel.__init__(lat, lon, year, month, day, doy, ibin45N)
###########

print("test Pixel.__init__(lat, lon, year, month, day, doy, ibin45N)")
# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N = 1
ibin45N_ref = 1

p = image_with_primary_production_pixel.Pixel(lat,
                                              lon,
                                              year,
                                              month,
                                              day,
                                              doy,
                                              ibin45N
                                              )

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month_ref \
   and p.day == day_ref \
   and p.doy == doy_ref \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)
 
########### test Pixel.__repr__ ###########

print("test Pixel.__repr__")

str_ref = \
"""Pixel(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1)"""
str = repr(p)
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Pixel.__str__ ###########

print("test Pixel.__str__")

str_ref = \
"""(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1)"""
str = p.__str__()
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWater.__init__(lat, lon, year, month, day, doy, rrs_type \
########### array1d_iband_Rrs, array1d_idepth_chl) ###########

print("test PixelWater.__init__(lat, lon, year, month, day, doy, rrs_type, array1d_iband_Rrs, array1d_idepth_chl)")

# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N_ref = 0

rrs_type = 'A'

# Array of dimension NBANDS = 6.					       
# The first dimension are the wavelengths of the bands of the satellite.    
# The values are the remote-sensing reflectances.			       
# The units are sr^-1.
array1d_iband_Rrs = [0.000064, 0.0008, 0.001718, 0.003318, 0.00399, 0.001152]
array1d_iband_Rrs_ref = np.array(
    [0.000064, 0.0008, 0.001718, 0.003318, 0.00399, 0.001152],
    dtype = np.float32)

# Array of dimension NBDEPTHS = 101.				  
# The first dimension is the index of the geometric depths.	  
# The geometric depths are from 0 to 100 by step 1. Units: m.  
# The values are the chlorophyll-a concentration.		  
# The units are mg Chl-a m^-3.
array1d_idepth_chl = [51.346355, 54.653086, 59.353554, 64.846223, 69.99886, 73.420727, 73.950885, 71.134465, 65.421479, 57.970096, 50.17125, 43.159635, 37.539974, 33.39117, 30.45346, 28.350487, 26.744011, 25.396499, 24.168568, 22.98983, 21.829195, 20.674541, 19.521663, 18.369261, 17.216974, 16.064711, 14.912454, 13.760198, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
array1d_idepth_chl_ref = np.array(
    [51.346355, 54.653086, 59.353554, 64.846223, 69.99886, 73.420727, 73.950885, 71.134465, 65.421479, 57.970096, 50.17125, 43.159635, 37.539974, 33.39117, 30.45346, 28.350487, 26.744011, 25.396499, 24.168568, 22.98983, 21.829195, 20.674541, 19.521663, 18.369261, 17.216974, 16.064711, 14.912454, 13.760198, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    dtype = np.float32)

p = image_with_primary_production_pixel.PixelWater(lat,
                                                   lon,
                                                   year,
                                                   month,
                                                   day,
                                                   doy,
                                                   rrs_type,
                                                   array1d_iband_Rrs,
                                                   array1d_idepth_chl)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.ibin45N == ibin45N_ref \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWater.__init__(lat, lon, year, month, day, doy,
########### ibin45N,rrs_type, array1d_iband_Rrs, array1d_idepth_chl) ###########

print("test PixelWater.__init__(lat, lon, year, month, day, doy, rrs_type, array1d_iband_Rrs, array1d_idepth_chl, ibin45N)")

# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N = 1
ibin45N_ref = 1

p = image_with_primary_production_pixel.PixelWater(lat,
                                                   lon,
                                                   year,
                                                   month,
                                                   day,
                                                   doy,
                                                   rrs_type,
                                                   array1d_iband_Rrs,
                                                   array1d_idepth_chl,
                                                   ibin45N)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)



########### test PixelWater.__repr__ ###########

print("test PixelWater.__repr__")

str_ref = \
"""PixelWater(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1, rrs_type = 'A', array1d_iband_Rrs = [6.399999983841553e-05, 0.0007999999797903001, 0.0017180000431835651, 0.0033179998863488436, 0.0039900001138448715, 0.0011520000407472253], array1d_idepth_chl = [51.34635543823242, 54.6530876159668, 59.353553771972656, 64.84622192382812, 69.99886322021484, 73.42073059082031, 73.95088195800781, 71.13446807861328, 65.42147827148438, 57.970096588134766, 50.17124938964844, 43.15963363647461, 37.539974212646484, 33.391170501708984, 30.453460693359375, 28.350486755371094, 26.74401092529297, 25.396499633789062, 24.168567657470703, 22.989830017089844, 21.829195022583008, 20.674541473388672, 19.521663665771484, 18.369260787963867, 17.21697425842285, 16.06471061706543, 14.912453651428223, 13.760197639465332, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])"""
str = repr(p)
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWater.__str__ ###########

print("test PixelWater.__str__")

str_ref = \
"""(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1, rrs_type = 'A', array1d_iband_Rrs = [6.399999983841553e-05, 0.0007999999797903001, 0.0017180000431835651, 0.0033179998863488436, 0.0039900001138448715, 0.0011520000407472253], array1d_idepth_chl = [51.34635543823242, 54.6530876159668, 59.353553771972656, 64.84622192382812, 69.99886322021484, 73.42073059082031, 73.95088195800781, 71.13446807861328, 65.42147827148438, 57.970096588134766, 50.17124938964844, 43.15963363647461, 37.539974212646484, 33.391170501708984, 30.453460693359375, 28.350486755371094, 26.74401092529297, 25.396499633789062, 24.168567657470703, 22.989830017089844, 21.829195022583008, 20.674541473388672, 19.521663665771484, 18.369260787963867, 17.21697425842285, 16.06471061706543, 14.912453651428223, 13.760197639465332, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])"""
str = p.__str__()
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelGeo.__init__(lat, lon, year, month, day, doy, depth, province)
###########

print("test PixelGeo.__init__(lat, lon, year, month, day, doy, depth, province)")

# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N_ref = 0

# Depth.
# The units are m.
depth = 28.
depth_ref = np.float32(28.)
province = 5
province_ref = np.uint8(province)

p = image_with_primary_production_pixel.PixelGeo(lat,
                                                 lon,
                                                 year,
                                                 month,
                                                 day,
                                                 doy,
                                                 depth,
                                                 province)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.depth == depth_ref \
   and p.province == province_ref \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelGeo.__init__(lat, lon, year, month, day, doy, depth, province, ibin45N)
###########

print("test PixelGeo.__init__(lat, lon, year, month, day, doy, depth, province, ibin45N)")

# Depth.
# The units are m.
depth = 28.
depth_ref = np.float32(28.)
province = 5
province_ref = np.uint8(province)
# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N = 1
ibin45N_ref = 1

p = image_with_primary_production_pixel.PixelGeo(lat,
                                                 lon,
                                                 year,
                                                 month,
                                                 day,
                                                 doy,
                                                 depth,
                                                 province,
                                                 ibin45N)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.depth == depth_ref \
   and p.province == province_ref \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelGeo.__repr__() ###########

print("test PixelGeo.__repr__")

str_ref = \
"""PixelGeo(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1, depth = 28.0, province = 5)"""
str = repr(p)
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelGeo.__str__ ###########

print("test PixelGeo.__str__")

str_ref = \
"""(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1, depth = 28.0, province = 5)"""
str = p.__str__()
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelLight.__init__(lat, lon, year, month, day, doy, array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld) ###########

print("PixelLight.__init__(lat, lon, year, month, day, doy, array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld)")

array1d_itime_cf \
    = [0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822]
array1d_itime_cf_ref = np.zeros(NTIMES, dtype = np.float32)
array1d_itime_cf_ref.fill(0.5822)
array1d_itime_o3 \
    = [276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8]
array1d_itime_o3_ref = np.zeros(NTIMES, dtype = np.float32)
array1d_itime_o3_ref.fill(276.8)
array1d_itime_taucld \
    = [5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52]
array1d_itime_taucld_ref = np.zeros(NTIMES, dtype = np.float32)
array1d_itime_taucld_ref.fill(5.52)
# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N_ref = 0

p = image_with_primary_production_pixel.PixelLight(lat,
                                                   lon,
                                                   year,
                                                   month,
                                                   day,
                                                   doy,
                                                   array1d_itime_cf,
                                                   array1d_itime_o3,
                                                   array1d_itime_taucld)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)
    
########### test PixelLight.__init__(lat, lon, year, month, day, doy, array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, ibin45N) ###########

print("PixelLight.__init__(lat, lon, year, month, day, doy, array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, ibin45N)")

array1d_itime_cf \
    = [0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822]
array1d_itime_cf_ref = np.zeros(NTIMES, dtype = np.float32)
array1d_itime_cf_ref.fill(0.5822)
array1d_itime_o3 \
    = [276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8]
array1d_itime_o3_ref = np.zeros(NTIMES, dtype = np.float32)
array1d_itime_o3_ref.fill(276.8)
array1d_itime_taucld \
    = [5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52]
array1d_itime_taucld_ref = np.zeros(NTIMES, dtype = np.float32)
array1d_itime_taucld_ref.fill(5.52)
# Index (0-based) in the ISIN grid above 45 degrees North.
# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N = 1
ibin45N_ref = 1

p = image_with_primary_production_pixel.PixelLight(lat,
                                                   lon,
                                                   year,
                                                   month,
                                                   day,
                                                   doy,
                                                   array1d_itime_cf,
                                                   array1d_itime_o3,
                                                   array1d_itime_taucld,
                                                   ibin45N)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelLight.__repr__ ###########

print("test PixelLight.__repr__")

str_ref = \
"""PixelLight(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1, array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514])"""

str = repr(p)
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelLight.__str__() ###########

print("test PixelLight.__str__()")

str_ref = \
"""(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1, array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514])"""

str = p.__str__()
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWaterLight.__init__(lat, lon, year, month, day, doy, \
########### rrs_type, array1d_iband_Rrs, array1d_idepth_chl, 
########### array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld)

print("test PixelWaterLight.__init__(lat, lon, year, month, day, doy, rrs_type, array1d_iband_Rrs, array1d_idepth_chl, array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld")

# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N_ref = 0

p = image_with_primary_production_pixel.PixelWaterLight(lat,
                                                        lon,
                                                        year,
                                                        month,
                                                        day,
                                                        doy,
                                                        rrs_type,
                                                        array1d_iband_Rrs,
                                                        array1d_idepth_chl,
                                                        array1d_itime_cf,
                                                        array1d_itime_o3,
                                                        array1d_itime_taucld)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWaterLight.__init__(lat, lon, year, month, day, doy, \
########### rrs_type, array1d_iband_Rrs, array1d_idepth_chl, 
########### array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld)

print("test PixelWaterLight.__init__(lat, lon, year, month, day, doy, rrs_type, array1d_iband_Rrs, array1d_idepth_chl, array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld")

# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N_ref = 0

p = image_with_primary_production_pixel.PixelWaterLight(lat,
                                                        lon,
                                                        year,
                                                        month,
                                                        day,
                                                        doy,
                                                        rrs_type,
                                                        array1d_iband_Rrs,
                                                        array1d_idepth_chl,
                                                        array1d_itime_cf,
                                                        array1d_itime_o3,
                                                        array1d_itime_taucld)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWaterLight.__init__(lat, lon, year, month, day, doy, \
########### rrs_type, array1d_iband_Rrs, array1d_idepth_chl, 
########### array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, ibin45N)

print("test PixelWaterLight.__init__(lat, lon, year, month, day, doy, rrs_type, array1d_iband_Rrs, array1d_idepth_chl, array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, ibin45N")

# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N = 1
ibin45N_ref = 1

p = image_with_primary_production_pixel.PixelWaterLight(lat,
                                                        lon,
                                                        year,
                                                        month,
                                                        day,
                                                        doy,
                                                        rrs_type,
                                                        array1d_iband_Rrs,
                                                        array1d_idepth_chl,
                                                        array1d_itime_cf,
                                                        array1d_itime_o3,
                                                        array1d_itime_taucld,
                                                        ibin45N)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWaterLight.__repr__ ###########

print("test PixelWaterLight.__repr__")

str_ref = \
"""PixelWaterLight(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1, rrs_type = 'A', array1d_iband_Rrs = [6.399999983841553e-05, 0.0007999999797903001, 0.0017180000431835651, 0.0033179998863488436, 0.0039900001138448715, 0.0011520000407472253], array1d_idepth_chl = [51.34635543823242, 54.6530876159668, 59.353553771972656, 64.84622192382812, 69.99886322021484, 73.42073059082031, 73.95088195800781, 71.13446807861328, 65.42147827148438, 57.970096588134766, 50.17124938964844, 43.15963363647461, 37.539974212646484, 33.391170501708984, 30.453460693359375, 28.350486755371094, 26.74401092529297, 25.396499633789062, 24.168567657470703, 22.989830017089844, 21.829195022583008, 20.674541473388672, 19.521663665771484, 18.369260787963867, 17.21697425842285, 16.06471061706543, 14.912453651428223, 13.760197639465332, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514])"""
str = repr(p)
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWaterLight.__str__ ###########

print("test PixelWaterLight.__str__")

str_ref = \
"""(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 1, rrs_type = 'A', array1d_iband_Rrs = [6.399999983841553e-05, 0.0007999999797903001, 0.0017180000431835651, 0.0033179998863488436, 0.0039900001138448715, 0.0011520000407472253], array1d_idepth_chl = [51.34635543823242, 54.6530876159668, 59.353553771972656, 64.84622192382812, 69.99886322021484, 73.42073059082031, 73.95088195800781, 71.13446807861328, 65.42147827148438, 57.970096588134766, 50.17124938964844, 43.15963363647461, 37.539974212646484, 33.391170501708984, 30.453460693359375, 28.350486755371094, 26.74401092529297, 25.396499633789062, 24.168567657470703, 22.989830017089844, 21.829195022583008, 20.674541473388672, 19.521663665771484, 18.369260787963867, 17.21697425842285, 16.06471061706543, 14.912453651428223, 13.760197639465332, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514])"""
str = p.__str__()
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWaterLightGeo.__init__(lat, lon, year, month, day, doy, \
########### rrs_type, array1d_iband_Rrs, array1d_idepth_chl, \
########### array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, \
########### depth, province, array4d_itaucld_io3_ithetas_iwl_ed0minus)

print("test PixelWaterLightGeo.__init__(lat, lon, year, month, day, doy, \
rrs_type, array1d_iband_Rrs, array1d_idepth_chl, \
array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, \
depth, province, array4d_itaucld_io3_ithetas_iwl_ed0minus)")

lut_ed0minus = "../Inputs/Ed0moins_LUT.dat"
array4d_itaucld_io3_ithetas_iwl_ed0minus \
    = image_with_primary_production_pixel.ImageLight.get_array4d_itaucld_io3_ithetas_iwl_ed0minus(lut_ed0minus)

# Array of dimension NBDEPTHS - 1 = 100.                           
# The first dimension is the index of the geometric depths.        
# The geometric depths are from 0 to 100 by step 1. Units: m.      
# The values are the primary productivities.                       
# Units: mgC.m^-3.d^-1.
array1d_idepth_pp_ref_l_matsuoka2011 = [1186.482421875, 844.26025390625, 606.4862060546875, 402.34600830078125, 228.46109008789062, 115.42898559570312, 54.418548583984375, 24.84198760986328, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
array1d_idepth_pp_ref_matsuoka2011 = np.array(
    object = array1d_idepth_pp_ref_l_matsuoka2011,
    dtype = np.float32
)

pp_ref_matsuoka2011 = np.float32(3462.7255020141602)

# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N_ref = 0

p = image_with_primary_production_pixel.PixelWaterLightGeo(lat,
                                                           lon,
                                                           year,
                                                           month,
                                                           day,
                                                           doy,
                                                           rrs_type,
                                                           array1d_iband_Rrs,
                                                           array1d_idepth_chl,
                                                           array1d_itime_cf,
                                                           array1d_itime_o3,
                                                           array1d_itime_taucld,
                                                           depth,
                                                           province,
                                                           array4d_itaucld_io3_ithetas_iwl_ed0minus)

#print(p)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.depth == depth_ref \
   and p.province == province_ref \
   and np.allclose(p.array1d_idepth_pp,
                   array1d_idepth_pp_ref_matsuoka2011) \
   and np.isclose(p.pp,
                  pp_ref_matsuoka2011) \
    and p.ibin45N == ibin45N_ref:
      npass = pass_test(npass)
else:
      nfail = fail(nfail)

########### test PixelWaterLightGeo.__init__(lat, lon, year, month, day, doy, \
########### rrs_type, array1d_iband_Rrs, array1d_idepth_chl, \
########### array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, \
########### depth, province, array4d_itaucld_io3_ithetas_iwl_ed0minus,
########### ibin45N, chl = CHL_SURFACE)

print("test PixelWaterLightGeo.__init__(lat, lon, year, month, day, doy, \
rrs_type, array1d_iband_Rrs, array1d_idepth_chl, \
array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, \
depth, province, array4d_itaucld_io3_ithetas_iwl_ed0minus, ibin45N, \
chl = CHL_SURFACE)")

# The value of the option chl to use the chlorophyll-a concentration.        
# 0 for the chlorophyll-a concentration vertical profile in the water column.
# 1 for the surface chlorophyll-a concentration.                             
chl = image_with_primary_production_pixel.get_array1d_idepth_pp.CHL_SURFACE

# Index (0-based) in the ISIN grid above 45 degrees North.
ibin45N = 1
ibin45N_ref = 1

# Array of dimension NBDEPTHS - 1 = 100.                           
# The first dimension is the index of the geometric depths.        
# The geometric depths are from 0 to 100 by step 1. Units: m.      
# The values are the primary productivities.                       
# Units: mgC.m^-3.d^-1.
array1d_idepth_pp_ref_surface_matsuoka2011=[1162.2470703125, 781.9638671875, 535.7859497070312, 356.07159423828125, 215.67868041992188, 122.90534210205078, 68.05543518066406, 37.29963684082031, 20.417219161987305, 11.022384643554688, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

array1d_idepth_pp_ref_surface_matsuoka2011 = np.array(
    object = array1d_idepth_pp_ref_surface_matsuoka2011,
    dtype = np.float32
)

pp_ref_surface_matsuoka2011 = np.float32(3311.4471797943115)

p = image_with_primary_production_pixel.PixelWaterLightGeo(lat,
                                                           lon,
                                                           year,
                                                           month,
                                                           day,
                                                           doy,
                                                           rrs_type,
                                                           array1d_iband_Rrs,
                                                           array1d_idepth_chl,
                                                           array1d_itime_cf,
                                                           array1d_itime_o3,
                                                           array1d_itime_taucld,
                                                           depth,
                                                           province,
                                                           array4d_itaucld_io3_ithetas_iwl_ed0minus,
                                                           ibin45N,
                                                           chl = chl
                                                           )

#print(p)

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
                   and p.depth == depth_ref \
                   and p.province == province_ref \
   and np.allclose(p.array1d_idepth_pp,
                   array1d_idepth_pp_ref_surface_matsuoka2011) \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test PixelWaterLightGeo.__init__(lat, lon, year, month, day, doy, \
########### rrs_type, array1d_iband_Rrs, array1d_idepth_chl, \
########### array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, \
########### depth, province, array4d_itaucld_io3_ithetas_iwl_ed0minus,
########### ibin45N)

print("test PixelWaterLightGeo.__init__(lat, lon, year, month, day, doy, \
rrs_type, array1d_iband_Rrs, array1d_idepth_chl, \
array1d_itime_cf, array1d_itime_o3, array1d_itime_taucld, \
depth, province, array4d_itaucld_io3_ithetas_iwl_ed0minus, ibin45N)")

p = image_with_primary_production_pixel.PixelWaterLightGeo(lat,
                                                           lon,
                                                           year,
                                                           month,
                                                           day,
                                                           doy,
                                                           rrs_type,
                                                           array1d_iband_Rrs,
                                                           array1d_idepth_chl,
                                                           array1d_itime_cf,
                                                           array1d_itime_o3,
                                                           array1d_itime_taucld,
                                                           depth,
                                                           province,
                                                           array4d_itaucld_io3_ithetas_iwl_ed0minus,
                                                           ibin45N
                                                           )

if p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
                   and p.depth == depth_ref \
                   and p.province == province_ref \
   and np.allclose(p.array1d_idepth_pp,
                   array1d_idepth_pp_ref_matsuoka2011) \
   and p.ibin45N == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Image.__init__(year, month, day, doy, grid_file)
###########

print("test Image.__init__(year, month, day, doy, grid_file)")

ipix_ref = 2
npix_ref = 3479813
# TEST
npix_ref = 3

year = 2009
month = 8
# Day of month.
day = 21
# Day of year.
doy = 233
# Name of the NetCDF file containing the variables lat and lon.
grid_file = "../Inputs/grid.nc"

image = image_with_primary_production_pixel.Image(year,
                                                  month,
                                                  day,
                                                  doy,
                                                  grid_file)

#print("image: {}",format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))
lat_read = p.lat
lon_read = p.lon
year_read = p.year
month_read = p.month
day_read = p.day
doy_read = p.doy

if npix == npix_ref \
   and np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and np.isclose(year_read, year) \
   and np.isclose(month_read, month) \
   and np.isclose(day_read, day) \
   and np.isclose(doy_read, doy):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)
    

########### test Image.__init__(year, month, day, doy, grid_file,
########### array1d_ipix_ibin45N)

print("test Image.__init__(year, month, day, doy, grid_file, array1d_ipix_ibin45N)")

ipix_ref = 1
npix_ref = 3479813
# TEST
npix_ref = 2

year = 2009
month = 8
# Day of month.
day = 21
# Day of year.
doy = 233
# Name of the NetCDF file containing the variables lat and lon.
grid_file = "../Inputs/grid.nc"
# Array of dimension npix. The number of pixels in the resulting image.
# The first dimension is the indices of the pixel in the resulting image.
# The values are the indices (0-based) of the pixels in the ISIN grid above 45
# degrees North.
# Units: Unitless.                                                             
array1d_ipix_ibin45N = np.array([0, 2], dtype = np.int32)

image = image_with_primary_production_pixel.Image(year,
                                                  month,
                                                  day,
                                                  doy,
                                                  grid_file,
                                                  array1d_ipix_ibin45N)

#print("image: {}",format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))
lat_read = p.lat
lon_read = p.lon
year_read = p.year
month_read = p.month
day_read = p.day
doy_read = p.doy

if npix == npix_ref \
   and np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and np.isclose(year_read, year) \
   and np.isclose(month_read, month) \
   and np.isclose(day_read, day) \
   and np.isclose(doy_read, doy):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Image.__repr__ ###########

print("test Image.__repr__")

str_ref = \
"""Image(array1d_ipix_pixel = array([ Pixel(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0),
       Pixel(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2)], dtype=object))"""
str = repr(image)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Image.__str__ ###########

print("test Image.__str__")

str_ref = \
"""(array1d_ipix_pixel = array([ Pixel(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0),
       Pixel(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2)], dtype=object))"""
str = image.__str__()
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Image.export(filename) ###########

print("test Image.export(filename)")

filename = "../Outputs/foo_Image.nc"

ipix_ref = 1
ibin45N_ref = 2

image.export_primary_production(filename)

array1d_ipix_lat = \
Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon = \
Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Image.export(filename) ###########

print("test Image.export(filename)")

filename = "../Outputs/Dir/foo_Image.nc"

image.export_primary_production(filename)

array1d_ipix_lat = \
Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon = \
Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test Image.export(filename, grid_file) ###########

print("test Image.export(filename, grid_file)")

filename = "../Outputs/foo_Image.nc"
grid_file = "../Inputs/grid.nc"

ipix_ref = 2
ibin45N_ref = 2

image.export_primary_production(filename, grid_file)

array1d_ipix_lat = \
Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon = \
Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWater.__init__(year, month, day, doy, grid_file, rrs_type, rrs_file, chl_file )
###########

print("test ImageWater.__init__(year, month, day, doy, grid_file, rrs_type, rrs_file, chl_file )")

ipix_ref = 2
npix_ref = 3479813
# TEST
npix_ref = 3

year = 2009
month = 8
# Day of month.
day = 21
# Day of year.
doy = 233
# Name of the NetCDF file containing the variables lat and lon.
grid_file = "../Inputs/grid.nc"
rrs_type = 'A'
rrs_file = "../Inputs/Rrs.nc"
chl_file = "../Inputs/chl.nc"

image = image_with_primary_production_pixel.ImageWater(year,
                                                       month,
                                                       day,
                                                       doy,
                                                       grid_file,
                                                       rrs_type,
                                                       rrs_file,
                                                       chl_file)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWater.__init__(year, month, day, doy, grid_file, rrs_type, rrs_file, chl_file, array1d_ipix_ibin45N)
###########

print("test ImageWater.__init__(year, month, day, doy, grid_file, rrs_type, rrs_file, chl_file, array1d_ipix_ibin45N)")

ipix_ref = 1
npix_ref = 3479813
# TEST
npix_ref = 2

year = 2009
month = 8
# Day of month.
day = 21
# Day of year.
doy = 233
# Name of the NetCDF file containing the variables lat and lon.
grid_file = "../Inputs/grid.nc"
rrs_type = 'A'
rrs_file = "../Inputs/Rrs.nc"
chl_file = "../Inputs/chl.nc"
# Array of dimension npix. The number of pixels in the resulting image.
# The first dimension is the indices of the pixel in the resulting image.
# The values are the indices (0-based) of the pixels in the ISIN grid above 45
# degrees North.
# Units: Unitless.                                                             
array1d_ipix_ibin45N = np.array([0, 2], dtype = np.int32)

image = image_with_primary_production_pixel.ImageWater(year,
                                                       month,
                                                       day,
                                                       doy,
                                                       grid_file,
                                                       rrs_type,
                                                       rrs_file,
                                                       chl_file,
                                                       array1d_ipix_ibin45N)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWater.export(filename) ###########

print('test ImageWater.export(filename)')
ipix_ref = 1
ibin45N_ref = 2
filename = "../Outputs/foo_ImageWater.nc"
image.export_primary_production(filename)
array1d_ipix_lat \
= Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon \
= Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
array2d_ipix_iband_Rrs \
    = Netcdf_tools.get_array2d_i_j_val(filename, "Rrs")
array2d_ipix_idepth_chl \
    = Netcdf_tools.get_array2d_i_j_val(filename, "chlz")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
array1d_iband_Rrs_read = array2d_ipix_iband_Rrs[ipix_ref,]
array1d_idepth_chlz_read = array2d_ipix_idepth_chl[ipix_ref,]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref \
   and np.allclose(array1d_iband_Rrs_read, array1d_iband_Rrs_ref) \
   and np.allclose(array1d_idepth_chlz_read, array1d_idepth_chl_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWater.export(filename, grid_file) ###########

print('test ImageWater.export(filename, grid_file)')
filename = "../Outputs/foo_ImageWater.nc"
grid_file = "../Inputs/grid.nc"
ipix_ref = 2
ibin45N_ref = 2
image.export_primary_production(filename, grid_file)
array1d_ipix_lat \
= Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon \
= Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
array2d_ipix_iband_Rrs \
    = Netcdf_tools.get_array2d_i_j_val(filename, "Rrs")
array2d_ipix_idepth_chl \
    = Netcdf_tools.get_array2d_i_j_val(filename, "chlz")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
array1d_iband_Rrs_read = array2d_ipix_iband_Rrs[ipix_ref,]
array1d_idepth_chlz_read = array2d_ipix_idepth_chl[ipix_ref,]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref \
   and np.allclose(array1d_iband_Rrs_read, array1d_iband_Rrs_ref) \
   and np.allclose(array1d_idepth_chlz_read, array1d_idepth_chl_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWater.get_array1d_ipix_documented(chl_file)###########

print('test ImageWater.get_array1d_ipix_documented(chl_file)')

array1d_ipix_ibin45N \
    = image_with_primary_production_pixel.ImageWater.get_pixel_with_chlorophyl_information(chl_file)

array1d_ipix_ibin45N_ref = [0, 2]

if np.allclose(array1d_ipix_ibin45N, array1d_ipix_ibin45N_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWater.get_array2d_ipix_iband_Rrs(rrs_type, rrs_file)
###########

print("test ImageWater.get_array2d_ipix_iband_Rrs(rrs_type, rrs_file)")

ipix_ref = 2

array2d_ipix_iband_Rrs_read \
    = image_with_primary_production_pixel.ImageWater.get_array2d_ipix_iband_Rrs(rrs_type,
                                                                                rrs_file)
array1d_iband_Rrs_read = array2d_ipix_iband_Rrs_read[ipix_ref]

if np.allclose(array1d_iband_Rrs_read, array1d_iband_Rrs_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWater.get_array2d_ipix_iband_chl(chl_file)
###########

print("test ImageWater.get_array2d_ipix_idepth_chl(chl_file)")

ipix_ref = 2

array2d_ipix_idepth_chl_read \
    = image_with_primary_production_pixel.ImageWater.get_array2d_ipix_idepth_chl(chl_file)
array1d_idepth_chl_read = array2d_ipix_idepth_chl_read[ipix_ref]

if np.allclose(array1d_idepth_chl_read, array1d_idepth_chl_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

############ test ImageWater.__repr__() ###########

print("test ImageWater.__repr__()")

str_ref = \
"""ImageWater(array1d_ipix_pixel = array([ PixelWater(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0, rrs_type = 'A', array1d_iband_Rrs = [0.008642000146210194, 0.008084000088274479, 0.006331999786198139, 0.00469799991697073, 0.003625999903306365, 0.0020359999034553766], array1d_idepth_chl = [0.2825790047645569, 0.28540900349617004, 0.28870299458503723, 0.2924950122833252, 0.29681700468063354, 0.30170199275016785, 0.3071799874305725, 0.313277006149292, 0.3200179934501648, 0.32742199301719666, 0.33550500869750977, 0.3442760109901428, 0.353738009929657, 0.3638859987258911, 0.37470901012420654, 0.3861849904060364, 0.39828601479530334, 0.410971999168396, 0.42419400811195374, 0.43789398670196533, 0.45200398564338684, 0.4664449989795685, 0.481128990650177, 0.4959630072116852, 0.5108399987220764, 0.5256519913673401, 0.5402809977531433, 0.5546069741249084, 0.5685070157051086, 0.581853985786438, 0.5945240259170532, 0.6063950061798096, 0.6173480153083801, 0.627269983291626, 0.6360549926757812, 0.6436060070991516, 0.6498379707336426, 0.6546769738197327, 0.6580619812011719, 0.6599469780921936, 0.6603019833564758, 0.6591100096702576, 0.6563720107078552, 0.6521040201187134, 0.6463389992713928, 0.6391239762306213, 0.6305199861526489, 0.6206009984016418, 0.6094539761543274, 0.5971760153770447, 0.583873987197876, 0.5696600079536438, 0.5546550154685974, 0.5389800071716309, 0.5227599740028381, 0.5061209797859192, 0.48918700218200684, 0.47207701206207275, 0.45490700006484985, 0.4377889931201935, 0.4208250045776367, 0.40411099791526794, 0.38773301243782043, 0.3717679977416992, 0.3562859892845154, 0.3413420021533966, 0.32698699831962585, 0.31325799226760864, 0.3001840114593506, 0.28778600692749023, 0.27607399225234985, 0.26505300402641296, 0.254720002412796, 0.24506500363349915, 0.23607300221920013, 0.22772200405597687, 0.21999000012874603, 0.21284900605678558, 0.20626799762248993, 0.20021599531173706, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),\n       PixelWater(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2, rrs_type = 'A', array1d_iband_Rrs = [6.399999983841553e-05, 0.0007999999797903001, 0.0017180000431835651, 0.0033179998863488436, 0.0039900001138448715, 0.0011520000407472253], array1d_idepth_chl = [51.34635543823242, 54.6530876159668, 59.353553771972656, 64.84622192382812, 69.99886322021484, 73.42073059082031, 73.95088195800781, 71.13446807861328, 65.42147827148438, 57.970096588134766, 50.17124938964844, 43.15963363647461, 37.539974212646484, 33.391170501708984, 30.453460693359375, 28.350486755371094, 26.74401092529297, 25.396499633789062, 24.168567657470703, 22.989830017089844, 21.829195022583008, 20.674541473388672, 19.521663665771484, 18.369260787963867, 17.21697425842285, 16.06471061706543, 14.912453651428223, 13.760197639465332, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])], dtype=object))"""
str = repr(image)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWater.__str__() ###########

print("test ImageWater.__str__()")

str_ref = \
"""(array1d_ipix_pixel = array([ PixelWater(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0, rrs_type = 'A', array1d_iband_Rrs = [0.008642000146210194, 0.008084000088274479, 0.006331999786198139, 0.00469799991697073, 0.003625999903306365, 0.0020359999034553766], array1d_idepth_chl = [0.2825790047645569, 0.28540900349617004, 0.28870299458503723, 0.2924950122833252, 0.29681700468063354, 0.30170199275016785, 0.3071799874305725, 0.313277006149292, 0.3200179934501648, 0.32742199301719666, 0.33550500869750977, 0.3442760109901428, 0.353738009929657, 0.3638859987258911, 0.37470901012420654, 0.3861849904060364, 0.39828601479530334, 0.410971999168396, 0.42419400811195374, 0.43789398670196533, 0.45200398564338684, 0.4664449989795685, 0.481128990650177, 0.4959630072116852, 0.5108399987220764, 0.5256519913673401, 0.5402809977531433, 0.5546069741249084, 0.5685070157051086, 0.581853985786438, 0.5945240259170532, 0.6063950061798096, 0.6173480153083801, 0.627269983291626, 0.6360549926757812, 0.6436060070991516, 0.6498379707336426, 0.6546769738197327, 0.6580619812011719, 0.6599469780921936, 0.6603019833564758, 0.6591100096702576, 0.6563720107078552, 0.6521040201187134, 0.6463389992713928, 0.6391239762306213, 0.6305199861526489, 0.6206009984016418, 0.6094539761543274, 0.5971760153770447, 0.583873987197876, 0.5696600079536438, 0.5546550154685974, 0.5389800071716309, 0.5227599740028381, 0.5061209797859192, 0.48918700218200684, 0.47207701206207275, 0.45490700006484985, 0.4377889931201935, 0.4208250045776367, 0.40411099791526794, 0.38773301243782043, 0.3717679977416992, 0.3562859892845154, 0.3413420021533966, 0.32698699831962585, 0.31325799226760864, 0.3001840114593506, 0.28778600692749023, 0.27607399225234985, 0.26505300402641296, 0.254720002412796, 0.24506500363349915, 0.23607300221920013, 0.22772200405597687, 0.21999000012874603, 0.21284900605678558, 0.20626799762248993, 0.20021599531173706, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
       PixelWater(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2, rrs_type = 'A', array1d_iband_Rrs = [6.399999983841553e-05, 0.0007999999797903001, 0.0017180000431835651, 0.0033179998863488436, 0.0039900001138448715, 0.0011520000407472253], array1d_idepth_chl = [51.34635543823242, 54.6530876159668, 59.353553771972656, 64.84622192382812, 69.99886322021484, 73.42073059082031, 73.95088195800781, 71.13446807861328, 65.42147827148438, 57.970096588134766, 50.17124938964844, 43.15963363647461, 37.539974212646484, 33.391170501708984, 30.453460693359375, 28.350486755371094, 26.74401092529297, 25.396499633789062, 24.168567657470703, 22.989830017089844, 21.829195022583008, 20.674541473388672, 19.521663665771484, 18.369260787963867, 17.21697425842285, 16.06471061706543, 14.912453651428223, 13.760197639465332, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])], dtype=object))"""
str = image.__str__()
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)


########### test ImageGeo.__init__(year, month, day, doy, grid_file,
########### geospatial_file)

print("test ImageGeo.__init__(year, month, day, doy, grid_file, geospatial_file)")

ipix_ref = 2
npix_ref = 3479813
# TEST
npix_ref = 3

# Name of the NetCDF containing the variable Zbot.
geospatial_file = "../Inputs/bathymetry.nc"

image = image_with_primary_production_pixel.ImageGeo(year,
                                                     month,
                                                     day,
                                                     doy,
                                                     grid_file,
                                                     geospatial_file)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.depth == depth_ref \
   and p.province == province_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageGeo.__init__(year, month, day, doy, grid_file,
########### geospatial_file, array1d_ipix_ibin45N)

print("test ImageGeo.__init__(year, month, day, doy, grid_file, geospatial_file, array1d_ipix_ibin45N)")

ipix_ref = 1
npix_ref = 3479813
# TEST
npix_ref = 2

# Name of the NetCDF containing the variable Zbot.
geospatial_file = "../Inputs/bathymetry.nc"
# Array of dimension npix. The number of pixels in the resulting image.
# The first dimension is the indices of the pixel in the resulting image.
# The values are the indices (0-based) of the pixels in the ISIN grid above 45
# degrees North.
# Units: Unitless.                                                             
array1d_ipix_ibin45N = np.array([0, 2], dtype = np.int32)

image = image_with_primary_production_pixel.ImageGeo(year,
                                                     month,
                                                     day,
                                                     doy,
                                                     grid_file,
                                                     geospatial_file,
                                                     array1d_ipix_ibin45N)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.depth == depth_ref \
   and p.province == province_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########## test ImageGeo.export(filename) ###########

print('test ImageGeo.export(filename)')
ipix_ref = 1
ibin45N_ref = 2
filename = "../Outputs/foo_ImageGeo.nc"
image.export_primary_production(filename)
array1d_ipix_lat \
= Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon \
= Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
array1d_ipix_depth \
    = Netcdf_tools.get_array1d_i_val(filename, "depth")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
depth_read = array1d_ipix_depth[ipix_ref]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref \
   and np.isclose(depth_read, depth_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageGeo.__repr__ ###########

print("test ImageGeo.__repr__")

str_ref = \
"""ImageGeo(array1d_ipix_pixel = array([ PixelGeo(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0, depth = 79.900002, province = 5),
       PixelGeo(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2, depth = 28.0, province = 5)], dtype=object))"""
str = repr(image)
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageGeo.__str__ ###########

# UNCOMMENT
# TODO by Eric Rehm

print("test ImageGeo.__str__")

str_ref = \
"""(array1d_ipix_pixel = array([ PixelGeo(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0, depth = 79.900002, province = 5),
       PixelGeo(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2, depth = 28.0, province = 5)], dtype=object))"""
str = image.__str__()
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageLight.__init__(year, month, day, doy, grid_file, atm_file, lut_ed0minus) ###########

print("test ImageLight.__init__(year, month, day, doy, grid_file, atm_file, lut_ed0minus)")

ipix_ref = 2
npix_ref = 3479813
# TEST
npix_ref = 3

atm_file = "../Inputs/atm.nc"
lut_ed0minus = "../Inputs/Ed0moins_LUT.dat"
#lut_ed0minus = "bug"
ed0minus_ref = 1.509924

image = image_with_primary_production_pixel.ImageLight(year,
                                                       month,
                                                       day,
                                                       doy,
                                                       grid_file,
                                                       atm_file,
                                                       lut_ed0minus)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and np.allclose(image.array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10],
                   ed0minus_ref,
                   rtol = 1e-03) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)
########### test ImageLight.__init__(year, month, day, doy, grid_file, atm_file, lut_ed0minus, array1d_ipix_ibin45N) ###########

print("test ImageLight.__init__(year, month, day, doy, grid_file, atm_file, lut_ed0minus, array1d_ipix_ibin45N)")

ipix_ref = 1
npix_ref = 3479813
# TEST
npix_ref = 2

atm_file = "../Inputs/atm.nc"
lut_ed0minus = "../Inputs/Ed0moins_LUT.dat"
#lut_ed0minus = "bug"
ed0minus_ref = 1.509924
# Array of dimension npix. The number of pixels in the resulting image.
# The first dimension is the indices of the pixel in the resulting image.
# The values are the indices (0-based) of the pixels in the ISIN grid above 45
# degrees North.
# Units: Unitless.                                                             
array1d_ipix_ibin45N = np.array([0, 2], dtype = np.int32)

image = image_with_primary_production_pixel.ImageLight(year,
                                                       month,
                                                       day,
                                                       doy,
                                                       grid_file,
                                                       atm_file,
                                                       lut_ed0minus,
                                                       array1d_ipix_ibin45N)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and np.allclose(image.array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10],
                   ed0minus_ref,
                   rtol = 1e-03) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageLight.get_array4d_itaucld_io3_ithetas_iwl_ed0minus(filename) ###########

print("test ImageLight.get_array4d_itaucld_io3_ithetas_iwl_ed0minus(filename)")

array4d_itaucld_io3_ithetas_iwl_ed0minus \
    = image_with_primary_production_pixel.ImageLight.get_array4d_itaucld_io3_ithetas_iwl_ed0minus(lut_ed0minus)
ed0minus = array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10]
#print("ed0minus: {}".format(ed0minus))
if np.allclose(ed0minus,
               ed0minus_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageLight.get_array2d_ipix_itime_cf(filename) ###########

print("test ImageLight.get_array2d_ipix_itime_cf(filename)")

ipix_ref = 2

array2d_ipix_itime_cf \
    = image_with_primary_production_pixel.ImageLight.get_array2d_ipix_itime_cf(atm_file)
array1d_itime_cf = array2d_ipix_itime_cf[ipix_ref]
#print("array1d_itime_cf: {0}".format(array1d_itime_cf))
if np.allclose(array1d_itime_cf,
               array1d_itime_cf_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageLight.get_array2d_ipix_itime_o3(filename) ###########

print("test ImageLight.get_array2d_ipix_itime_o3(filename)")

ipix_ref = 2

array2d_ipix_itime_o3 \
    = image_with_primary_production_pixel.ImageLight.get_array2d_ipix_itime_o3(atm_file)
array1d_itime_o3 = array2d_ipix_itime_o3[ipix_ref]
#print("array1d_itime_o3: {0}".format(array1d_itime_o3))
if np.allclose(array1d_itime_o3,
               array1d_itime_o3_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageLight.get_array2d_ipix_itime_taucld(filename) ###########

print("test ImageLight.get_array2d_ipix_itime_taucld(filename)")

ipix_ref = 2

array2d_ipix_itime_taucld \
    = image_with_primary_production_pixel.ImageLight.get_array2d_ipix_itime_taucld(atm_file)
array1d_itime_taucld = array2d_ipix_itime_taucld[ipix_ref]
#print("array1d_itime_taucld: {0}".format(array1d_itime_taucld))
if np.allclose(array1d_itime_taucld,
               array1d_itime_taucld_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

############ test ImageLight.__repr__() ###########

print("test ImageLight.__repr__()")

str_ref = \
"""ImageLight(array1d_ipix_pixel = array([ PixelLight(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0, array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514]),
       PixelLight(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2, array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514])], dtype=object), array4d_itaucld_io3_ithetas_iwl_ed0minus = array([[[[  2.46599986e-04,   1.15595004e-02,   1.02635399e-01, ...,
            7.21043253e+00,   7.33221912e+00,   7.30728006e+00],
         [  2.38399996e-04,   1.13199996e-02,   1.01288103e-01, ...,
            7.18108988e+00,   7.30266428e+00,   7.27753830e+00],
         [  2.14900007e-04,   1.06236003e-02,   9.73128974e-02, ...,
            7.09181023e+00,   7.21219444e+00,   7.18813705e+00],
         ..., 
         [  0.00000000e+00,   5.50000004e-06,   1.57799994e-04, ...,
            6.59078896e-01,   6.84351087e-01,   6.95586503e-01],
         [  0.00000000e+00,   2.70000010e-06,   6.73000031e-05, ...,
            2.10019693e-01,   2.19942600e-01,   2.25101799e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.90999994e-05,   4.27869987e-03,   6.22630008e-02, ...,
            7.20080853e+00,   7.32366276e+00,   7.29871464e+00],
         [  3.75999989e-05,   4.17440012e-03,   6.13318011e-02, ...,
            7.17095280e+00,   7.29359102e+00,   7.26951933e+00],
         [  3.31000010e-05,   3.87299992e-03,   5.85886016e-02, ...,
            7.08167362e+00,   7.20366430e+00,   7.18011808e+00],
         ..., 
         [  0.00000000e+00,   1.30000001e-06,   6.55999975e-05, ...,
            6.53923213e-01,   6.79589927e-01,   6.91259086e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.95000009e-05, ...,
            2.06878603e-01,   2.17028797e-01,   2.22394004e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.58960000e-03,   3.78668010e-02, ...,
            7.19067144e+00,   7.31458950e+00,   7.29069567e+00],
         [  0.00000000e+00,   1.54500001e-03,   3.72284018e-02, ...,
            7.16135454e+00,   7.28449202e+00,   7.26152658e+00],
         [  0.00000000e+00,   1.41729997e-03,   3.53609994e-02, ...,
            7.07207537e+00,   7.19459105e+00,   7.17209911e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.90000007e-05, ...,
            6.48858905e-01,   6.74920619e-01,   6.86969817e-01],
         [  0.00000000e+00,   2.00000002e-07,   1.35000000e-05, ...,
            2.03784794e-01,   2.14146897e-01,   2.19713494e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   8.26999967e-05,   8.60089995e-03, ...,
            7.16133785e+00,   7.28788710e+00,   7.26666498e+00],
         [  0.00000000e+00,   7.95000014e-05,   8.40890035e-03, ...,
            7.13145638e+00,   7.25778913e+00,   7.23746967e+00],
         [  0.00000000e+00,   7.04999984e-05,   7.85250030e-03, ...,
            7.04220343e+00,   7.16788864e+00,   7.14806843e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-06, ...,
            6.33799374e-01,   6.61026120e-01,   6.74144387e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.50000005e-06, ...,
            1.94786206e-01,   2.05736294e-01,   2.11883903e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   3.09999996e-05,   5.25970012e-03, ...,
            7.15120125e+00,   7.27935648e+00,   7.25921869e+00],
         [  0.00000000e+00,   2.97000006e-05,   5.13269985e-03, ...,
            7.12185812e+00,   7.24925900e+00,   7.22947693e+00],
         [  0.00000000e+00,   2.59999997e-05,   4.76620020e-03, ...,
            7.03260517e+00,   7.15935850e+00,   7.14007568e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.50000005e-06, ...,
            6.28884971e-01,   6.56486571e-01,   6.69931114e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.91874802e-01,   2.03007996e-01,   2.09335804e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   3.21920007e-03, ...,
            7.14160299e+00,   7.27028370e+00,   7.25119972e+00],
         [  0.00000000e+00,   0.00000000e+00,   3.13579990e-03, ...,
            7.11172104e+00,   7.24018574e+00,   7.22145796e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.89530004e-03, ...,
            7.02246809e+00,   7.15025949e+00,   7.13205671e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            6.23970628e-01,   6.51930571e-01,   6.65755808e-01],
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            1.89008296e-01,   2.00320795e-01,   2.06820399e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  2.29800004e-04,   1.08067002e-02,   9.62229967e-02, ...,
            6.75160360e+00,   6.85922956e+00,   6.83517504e+00],
         [  2.22000002e-04,   1.05796000e-02,   9.49361995e-02, ...,
            6.72050095e+00,   6.82789373e+00,   6.80362940e+00],
         [  1.99999995e-04,   9.92020033e-03,   9.11398008e-02, ...,
            6.62713575e+00,   6.73329639e+00,   6.71003056e+00],
         ..., 
         [  0.00000000e+00,   5.10000018e-06,   1.47900006e-04, ...,
            5.48654497e-01,   5.72791815e-01,   5.80892026e-01],
         [  0.00000000e+00,   2.49999994e-06,   6.31000003e-05, ...,
            2.03703105e-01,   2.17257798e-01,   2.22078100e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.64000007e-05,   3.99489980e-03,   5.83126992e-02, ...,
            6.74228239e+00,   6.85094452e+00,   6.82739258e+00],
         [  3.49000002e-05,   3.89640010e-03,   5.74234016e-02, ...,
            6.71117973e+00,   6.81961107e+00,   6.79639339e+00],
         [  3.08000017e-05,   3.61169991e-03,   5.48100993e-02, ...,
            6.61781979e+00,   6.72501373e+00,   6.70279741e+00],
         ..., 
         [  0.00000000e+00,   1.20000004e-06,   6.14000019e-05, ...,
            5.44404387e-01,   5.68835974e-01,   5.77289820e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.75999992e-05, ...,
            2.00637802e-01,   2.14354798e-01,   2.19389200e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.48260000e-03,   3.54324989e-02, ...,
            6.73296356e+00,   6.84265900e+00,   6.82015610e+00],
         [  0.00000000e+00,   1.44060003e-03,   3.48262005e-02, ...,
            6.70186090e+00,   6.81132603e+00,   6.78861046e+00],
         [  0.00000000e+00,   1.32020004e-03,   3.30503993e-02, ...,
            6.60850143e+00,   6.71673107e+00,   6.69501734e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.71000008e-05, ...,
            5.40154219e-01,   5.64880073e-01,   5.73687613e-01],
         [  0.00000000e+00,   1.00000001e-07,   1.26000004e-05, ...,
            1.97615594e-01,   2.11489797e-01,   2.16733098e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   7.69000035e-05,   8.03130027e-03, ...,
            6.70554399e+00,   6.81780577e+00,   6.79735470e+00],
         [  0.00000000e+00,   7.39000025e-05,   7.84969982e-03, ...,
            6.67444372e+00,   6.78647232e+00,   6.76635838e+00],
         [  0.00000000e+00,   6.54000032e-05,   7.32359989e-03, ...,
            6.58109188e+00,   6.69188547e+00,   6.67276764e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.79999995e-06, ...,
            5.27613521e-01,   5.53283513e-01,   5.62990129e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            1.88834593e-01,   2.03133598e-01,   2.08956093e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.87999992e-05,   4.90880013e-03, ...,
            6.69622517e+00,   6.80952024e+00,   6.79012156e+00],
         [  0.00000000e+00,   2.75999992e-05,   4.78880014e-03, ...,
            6.66512489e+00,   6.77818966e+00,   6.75857830e+00],
         [  0.00000000e+00,   2.40999998e-05,   4.44239983e-03, ...,
            6.57177591e+00,   6.68360281e+00,   6.66553402e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            5.23497820e-01,   5.49435973e-01,   5.59442282e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.85995594e-01,   2.00420499e-01,   2.06431195e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   3.00280005e-03, ...,
            6.68690634e+00,   6.80123520e+00,   6.78233862e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.92390003e-03, ...,
            6.65580606e+00,   6.76990700e+00,   6.75134230e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.69729993e-03, ...,
            6.56245947e+00,   6.67532301e+00,   6.65775442e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            5.19419730e-01,   5.45642674e-01,   5.55949271e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.83199704e-01,   1.97745398e-01,   2.03933597e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  2.16100001e-04,   1.02049001e-02,   9.11696032e-02, ...,
            6.36338997e+00,   6.45821190e+00,   6.43479300e+00],
         [  2.08800004e-04,   9.98819992e-03,   8.99311975e-02, ...,
            6.33109903e+00,   6.42568445e+00,   6.40258265e+00],
         [  1.87900005e-04,   9.35900025e-03,   8.62796977e-02, ...,
            6.23368359e+00,   6.32755280e+00,   6.30540562e+00],
         ..., 
         [  0.00000000e+00,   4.80000017e-06,   1.39199998e-04, ...,
            4.59726900e-01,   4.81187105e-01,   4.86550689e-01],
         [  0.00000000e+00,   2.30000001e-06,   5.93000004e-05, ...,
            1.75960705e-01,   1.88354000e-01,   1.92037299e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.41999985e-05,   3.76689993e-03,   5.51913008e-02, ...,
            6.35471106e+00,   6.45056057e+00,   6.42764091e+00],
         [  3.27999987e-05,   3.67300003e-03,   5.43375015e-02, ...,
            6.32188129e+00,   6.41749001e+00,   6.39543056e+00],
         [  2.89000000e-05,   3.40240006e-03,   5.18306009e-02, ...,
            6.22500753e+00,   6.31990385e+00,   6.29825354e+00],
         ..., 
         [  0.00000000e+00,   1.09999996e-06,   5.75999984e-05, ...,
            4.56144512e-01,   4.77866292e-01,   4.83506590e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.59000008e-05, ...,
            1.73315600e-01,   1.85841694e-01,   1.89714506e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.39620004e-03,   3.35027017e-02, ...,
            6.34603214e+00,   6.44236898e+00,   6.42048597e+00],
         [  0.00000000e+00,   1.35629997e-03,   3.29227000e-02, ...,
            6.31320477e+00,   6.40984154e+00,   6.38827848e+00],
         [  0.00000000e+00,   1.24200003e-03,   3.12226005e-02, ...,
            6.21633101e+00,   6.31171227e+00,   6.29110432e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.54000006e-05, ...,
            4.52588886e-01,   4.74567086e-01,   4.80489790e-01],
         [  0.00000000e+00,   1.00000001e-07,   1.17999998e-05, ...,
            1.70713603e-01,   1.83361903e-01,   1.87424600e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   7.21999968e-05,   7.57599995e-03, ...,
            6.31945896e+00,   6.41887760e+00,   6.39957619e+00],
         [  0.00000000e+00,   6.92999965e-05,   7.40269991e-03, ...,
            6.28717041e+00,   6.38635206e+00,   6.36682224e+00],
         [  0.00000000e+00,   6.14000019e-05,   6.90140016e-03, ...,
            6.19030190e+00,   6.28876877e+00,   6.27019739e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.60000002e-06, ...,
            4.42094803e-01,   4.64805514e-01,   4.71537799e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.30000001e-06, ...,
            1.63139194e-01,   1.76128805e-01,   1.80707797e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.70000000e-05,   4.62719984e-03, ...,
            6.31078005e+00,   6.41122866e+00,   6.39242411e+00],
         [  0.00000000e+00,   2.58000000e-05,   4.51290002e-03, ...,
            6.27849150e+00,   6.37870359e+00,   6.36021662e+00],
         [  0.00000000e+00,   2.25999993e-05,   4.18339996e-03, ...,
            6.18216419e+00,   6.28057957e+00,   6.26304531e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.30000001e-06, ...,
            4.38652396e-01,   4.61598605e-01,   4.68592107e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.60688102e-01,   1.73779204e-01,   1.78527206e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   2.82890000e-03, ...,
            6.30210114e+00,   6.40357733e+00,   6.38526964e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.75389990e-03, ...,
            6.26981497e+00,   6.37050962e+00,   6.35306454e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.53829989e-03, ...,
            6.17348766e+00,   6.27293110e+00,   6.25589561e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.00000021e-07, ...,
            4.35236990e-01,   4.58407998e-01,   4.65662688e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.58280000e-01,   1.71462297e-01,   1.76368400e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       ..., 
       [[[  1.10300003e-04,   5.45680011e-03,   5.05620018e-02, ...,
            3.12169504e+00,   3.13715339e+00,   3.12665820e+00],
         [  1.06500003e-04,   5.33809979e-03,   4.98499013e-02, ...,
            3.10240889e+00,   3.11789036e+00,   3.10752988e+00],
         [  9.57000011e-05,   4.99449996e-03,   4.77560014e-02, ...,
            3.04498196e+00,   3.06064415e+00,   3.05063677e+00],
         ..., 
         [  0.00000000e+00,   2.49999994e-06,   7.56000009e-05, ...,
            2.08547607e-01,   2.18382597e-01,   2.20232397e-01],
         [  0.00000000e+00,   1.20000004e-06,   3.22999986e-05, ...,
            8.06510970e-02,   8.63090008e-02,   8.77989009e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  1.70000003e-05,   1.98030006e-03,   3.02383006e-02, ...,
            3.11738515e+00,   3.13324642e+00,   3.12316036e+00],
         [  1.63000004e-05,   1.92990003e-03,   2.97535006e-02, ...,
            3.09809923e+00,   3.11403775e+00,   3.10408688e+00],
         [  1.43999996e-05,   1.78499997e-03,   2.83387993e-02, ...,
            3.04067206e+00,   3.05679154e+00,   3.04713917e+00],
         ..., 
         [  0.00000000e+00,   6.00000021e-07,   3.08999988e-05, ...,
            2.06920594e-01,   2.16874093e-01,   2.18855098e-01],
         [  0.00000000e+00,   3.00000011e-07,   1.39000003e-05, ...,
            7.94389993e-02,   8.51586983e-02,   8.67331997e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   7.22899975e-04,   1.81559008e-02, ...,
            3.11302161e+00,   3.12939382e+00,   3.11971736e+00],
         [  0.00000000e+00,   7.01799989e-04,   1.78316999e-02, ...,
            3.09373569e+00,   3.11018515e+00,   3.10058904e+00],
         [  0.00000000e+00,   6.41699997e-04,   1.68855004e-02, ...,
            3.03636241e+00,   3.05293894e+00,   3.04369593e+00],
         ..., 
         [  0.00000000e+00,   1.00000001e-07,   1.35000000e-05, ...,
            2.05309898e-01,   2.15376407e-01,   2.17488796e-01],
         [  0.00000000e+00,   1.00000001e-07,   6.30000022e-06, ...,
            7.82483965e-02,   8.40191990e-02,   8.56892988e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   3.59000005e-05,   3.99329979e-03, ...,
            3.10003853e+00,   3.11783624e+00,   3.10927868e+00],
         [  0.00000000e+00,   3.45000008e-05,   3.89979989e-03, ...,
            3.08080649e+00,   3.09868169e+00,   3.09020519e+00],
         [  0.00000000e+00,   3.04999994e-05,   3.62979993e-03, ...,
            3.02354097e+00,   3.04148960e+00,   3.03336668e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            2.00547606e-01,   2.10948706e-01,   2.13433594e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            7.47736990e-02,   8.07038024e-02,   8.26179013e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.33000003e-05,   2.41929991e-03, ...,
            3.09572887e+00,   3.11398363e+00,   3.10578108e+00],
         [  0.00000000e+00,   1.27000003e-05,   2.35820003e-03, ...,
            3.07649684e+00,   3.09482908e+00,   3.08676195e+00],
         [  0.00000000e+00,   1.10999999e-05,   2.18249997e-03, ...,
            3.01923132e+00,   3.03769135e+00,   3.02997828e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.98985398e-01,   2.09489003e-01,   2.12100103e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            7.36531988e-02,   7.96239972e-02,   8.16176981e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   1.46770000e-03, ...,
            3.09141922e+00,   3.11018515e+00,   3.10233784e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.42800005e-03, ...,
            3.07218695e+00,   3.09097648e+00,   3.08326435e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.31409999e-03, ...,
            3.01497531e+00,   3.03389287e+00,   3.02653503e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.97433904e-01,   2.08045706e-01,   2.10777506e-01],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            7.25487992e-02,   7.85657987e-02,   8.06339979e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  6.76999989e-05,   3.46309994e-03,   3.28803994e-02, ...,
            1.91745019e+00,   1.91365540e+00,   1.90873158e+00],
         [  6.54000032e-05,   3.38799995e-03,   3.24189998e-02, ...,
            1.90565240e+00,   1.90198910e+00,   1.89714527e+00],
         [  5.88000003e-05,   3.17010004e-03,   3.10558006e-02, ...,
            1.87052810e+00,   1.86720717e+00,   1.86255038e+00],
         ..., 
         [  0.00000000e+00,   1.60000002e-06,   4.91999999e-05, ...,
            1.29054695e-01,   1.34390503e-01,   1.35515794e-01],
         [  0.00000000e+00,   8.00000009e-07,   2.09999998e-05, ...,
            4.99616005e-02,   5.31668998e-02,   5.40850013e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  1.03000002e-05,   1.24230003e-03,   1.95126999e-02, ...,
            1.91475666e+00,   1.91126788e+00,   1.90660012e+00],
         [  9.89999990e-06,   1.21070002e-03,   1.92015003e-02, ...,
            1.90295875e+00,   1.89960158e+00,   1.89501393e+00],
         [  8.69999985e-06,   1.12000003e-03,   1.82886999e-02, ...,
            1.86783457e+00,   1.86487389e+00,   1.86041903e+00],
         ..., 
         [  0.00000000e+00,   4.00000005e-07,   1.99999995e-05, ...,
            1.28047302e-01,   1.33462593e-01,   1.34668693e-01],
         [  0.00000000e+00,   2.00000002e-07,   9.00000032e-06, ...,
            4.92100008e-02,   5.24565987e-02,   5.34303002e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   4.48600011e-04,   1.16341002e-02, ...,
            1.91206312e+00,   1.90888035e+00,   1.90446877e+00],
         [  0.00000000e+00,   4.35599999e-04,   1.14268996e-02, ...,
            1.90026522e+00,   1.89721406e+00,   1.89288247e+00],
         [  0.00000000e+00,   3.98400007e-04,   1.08212000e-02, ...,
            1.86519480e+00,   1.86254060e+00,   1.85828757e+00],
         ..., 
         [  0.00000000e+00,   1.00000001e-07,   8.69999985e-06, ...,
            1.27050698e-01,   1.32540196e-01,   1.33827105e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.99999999e-06, ...,
            4.84704003e-02,   5.17560989e-02,   5.27831987e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   2.16999997e-05,   2.51160003e-03, ...,
            1.90403616e+00,   1.90177202e+00,   1.89801979e+00],
         [  0.00000000e+00,   2.08000001e-05,   2.45300005e-03, ...,
            1.89223838e+00,   1.89015996e+00,   1.88643348e+00],
         [  0.00000000e+00,   1.84000000e-05,   2.28350004e-03, ...,
            1.85722184e+00,   1.85548663e+00,   1.85194790e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   8.99999975e-07, ...,
            1.24098502e-01,   1.29805401e-01,   1.31329507e-01],
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            4.63171005e-02,   4.97104004e-02,   5.08899987e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   7.90000013e-06,   1.51320000e-03, ...,
            1.90134263e+00,   1.89938450e+00,   1.89588833e+00],
         [  0.00000000e+00,   7.60000012e-06,   1.47510006e-03, ...,
            1.88959861e+00,   1.88777244e+00,   1.88430202e+00],
         [  0.00000000e+00,   6.59999978e-06,   1.36540004e-03, ...,
            1.85458207e+00,   1.85309911e+00,   1.84981644e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            1.23128802e-01,   1.28910094e-01,   1.30504206e-01],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            4.56217006e-02,   4.90473993e-02,   5.02746999e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   9.13100026e-04, ...,
            1.89870286e+00,   1.89705122e+00,   1.89375687e+00],
         [  0.00000000e+00,   0.00000000e+00,   8.88400013e-04, ...,
            1.88690507e+00,   1.88543916e+00,   1.88217056e+00],
         [  0.00000000e+00,   0.00000000e+00,   8.17699998e-04, ...,
            1.85188854e+00,   1.85076582e+00,   1.84768498e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            1.22169897e-01,   1.28020197e-01,   1.29689902e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            4.49359007e-02,   4.83924001e-02,   4.96664010e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  3.57999998e-05,   1.92870002e-03,   1.89859997e-02, ...,
            1.06622577e+00,   1.05327833e+00,   1.05216610e+00],
         [  3.46000015e-05,   1.88690005e-03,   1.87187009e-02, ...,
            1.05970728e+00,   1.04687536e+00,   1.04582644e+00],
         [  3.11000003e-05,   1.76570006e-03,   1.79334003e-02, ...,
            1.04025972e+00,   1.02782941e+00,   1.02680743e+00],
         ..., 
         [  0.00000000e+00,   8.99999975e-07,   2.83999998e-05, ...,
            7.25433975e-02,   7.47457966e-02,   7.54147023e-02],
         [  0.00000000e+00,   4.00000005e-07,   1.21000003e-05, ...,
            2.81419996e-02,   2.96302997e-02,   3.01632006e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  5.29999988e-06,   6.79999997e-04,   1.11498004e-02, ...,
            1.06471741e+00,   1.05192173e+00,   1.05096376e+00],
         [  5.10000018e-06,   6.62799983e-04,   1.09719997e-02, ...,
            1.05819893e+00,   1.04557312e+00,   1.04462409e+00],
         [  4.50000016e-06,   6.13100012e-04,   1.04507999e-02, ...,
            1.03875124e+00,   1.02652717e+00,   1.02560508e+00],
         ..., 
         [  0.00000000e+00,   2.00000002e-07,   1.14000004e-05, ...,
            7.19724000e-02,   7.42248967e-02,   7.49391988e-02],
         [  0.00000000e+00,   1.00000001e-07,   5.10000018e-06, ...,
            2.77180001e-02,   2.92342007e-02,   2.97975000e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.41600006e-04,   6.58260006e-03, ...,
            1.06320894e+00,   1.05061948e+00,   1.04976141e+00],
         [  0.00000000e+00,   2.34599996e-04,   6.46529999e-03, ...,
            1.05669057e+00,   1.04421651e+00,   1.04342175e+00],
         [  0.00000000e+00,   2.14600004e-04,   6.12290017e-03, ...,
            1.03724289e+00,   1.02517056e+00,   1.02445734e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.90000002e-06, ...,
            7.14121014e-02,   7.37093985e-02,   7.44692013e-02],
         [  0.00000000e+00,   0.00000000e+00,   2.30000001e-06, ...,
            2.73004994e-02,   2.88428999e-02,   2.94362996e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   1.11999998e-05,   1.38300005e-03, ...,
            1.05862987e+00,   1.04660404e+00,   1.04615438e+00],
         [  0.00000000e+00,   1.06999996e-05,   1.35070004e-03, ...,
            1.05211151e+00,   1.04025543e+00,   1.03981471e+00],
         [  0.00000000e+00,   9.49999958e-06,   1.25750003e-03, ...,
            1.03271770e+00,   1.02126372e+00,   1.02085030e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.99999999e-07, ...,
            6.97475001e-02,   7.21845999e-02,   7.30756000e-02],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            2.60857008e-02,   2.77006999e-02,   2.83787996e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   3.99999999e-06,   8.26200005e-04, ...,
            1.05712152e+00,   1.04530180e+00,   1.04500663e+00],
         [  0.00000000e+00,   3.90000014e-06,   8.05400021e-04, ...,
            1.05060303e+00,   1.03895307e+00,   1.03861237e+00],
         [  0.00000000e+00,   3.39999997e-06,   7.45499972e-04, ...,
            1.03120923e+00,   1.01996148e+00,   1.01970267e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            6.92033991e-02,   7.16854036e-02,   7.26165026e-02],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            2.56929994e-02,   2.73305997e-02,   2.80344002e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   4.94399981e-04, ...,
            1.05561304e+00,   1.04399943e+00,   1.04380429e+00],
         [  0.00000000e+00,   0.00000000e+00,   4.81099996e-04, ...,
            1.04909468e+00,   1.03759658e+00,   1.03741002e+00],
         [  0.00000000e+00,   0.00000000e+00,   4.42799996e-04, ...,
            1.02975476e+00,   1.01865911e+00,   1.01850033e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            6.86592981e-02,   7.11916015e-02,   7.21628964e-02],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            2.53062006e-02,   2.69648992e-02,   2.76951008e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]]], dtype=float32))"""
str = repr(image)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageLight.__str__() ###########

print("test ImageLight.__str__()")

str_ref = \
"""(array1d_ipix_pixel = array([ PixelLight(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0, array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514]),
       PixelLight(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2, array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514])], dtype=object), array4d_itaucld_io3_ithetas_iwl_ed0minus = array([[[[  2.46599986e-04,   1.15595004e-02,   1.02635399e-01, ...,
            7.21043253e+00,   7.33221912e+00,   7.30728006e+00],
         [  2.38399996e-04,   1.13199996e-02,   1.01288103e-01, ...,
            7.18108988e+00,   7.30266428e+00,   7.27753830e+00],
         [  2.14900007e-04,   1.06236003e-02,   9.73128974e-02, ...,
            7.09181023e+00,   7.21219444e+00,   7.18813705e+00],
         ..., 
         [  0.00000000e+00,   5.50000004e-06,   1.57799994e-04, ...,
            6.59078896e-01,   6.84351087e-01,   6.95586503e-01],
         [  0.00000000e+00,   2.70000010e-06,   6.73000031e-05, ...,
            2.10019693e-01,   2.19942600e-01,   2.25101799e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.90999994e-05,   4.27869987e-03,   6.22630008e-02, ...,
            7.20080853e+00,   7.32366276e+00,   7.29871464e+00],
         [  3.75999989e-05,   4.17440012e-03,   6.13318011e-02, ...,
            7.17095280e+00,   7.29359102e+00,   7.26951933e+00],
         [  3.31000010e-05,   3.87299992e-03,   5.85886016e-02, ...,
            7.08167362e+00,   7.20366430e+00,   7.18011808e+00],
         ..., 
         [  0.00000000e+00,   1.30000001e-06,   6.55999975e-05, ...,
            6.53923213e-01,   6.79589927e-01,   6.91259086e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.95000009e-05, ...,
            2.06878603e-01,   2.17028797e-01,   2.22394004e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.58960000e-03,   3.78668010e-02, ...,
            7.19067144e+00,   7.31458950e+00,   7.29069567e+00],
         [  0.00000000e+00,   1.54500001e-03,   3.72284018e-02, ...,
            7.16135454e+00,   7.28449202e+00,   7.26152658e+00],
         [  0.00000000e+00,   1.41729997e-03,   3.53609994e-02, ...,
            7.07207537e+00,   7.19459105e+00,   7.17209911e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.90000007e-05, ...,
            6.48858905e-01,   6.74920619e-01,   6.86969817e-01],
         [  0.00000000e+00,   2.00000002e-07,   1.35000000e-05, ...,
            2.03784794e-01,   2.14146897e-01,   2.19713494e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   8.26999967e-05,   8.60089995e-03, ...,
            7.16133785e+00,   7.28788710e+00,   7.26666498e+00],
         [  0.00000000e+00,   7.95000014e-05,   8.40890035e-03, ...,
            7.13145638e+00,   7.25778913e+00,   7.23746967e+00],
         [  0.00000000e+00,   7.04999984e-05,   7.85250030e-03, ...,
            7.04220343e+00,   7.16788864e+00,   7.14806843e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-06, ...,
            6.33799374e-01,   6.61026120e-01,   6.74144387e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.50000005e-06, ...,
            1.94786206e-01,   2.05736294e-01,   2.11883903e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   3.09999996e-05,   5.25970012e-03, ...,
            7.15120125e+00,   7.27935648e+00,   7.25921869e+00],
         [  0.00000000e+00,   2.97000006e-05,   5.13269985e-03, ...,
            7.12185812e+00,   7.24925900e+00,   7.22947693e+00],
         [  0.00000000e+00,   2.59999997e-05,   4.76620020e-03, ...,
            7.03260517e+00,   7.15935850e+00,   7.14007568e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.50000005e-06, ...,
            6.28884971e-01,   6.56486571e-01,   6.69931114e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.91874802e-01,   2.03007996e-01,   2.09335804e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   3.21920007e-03, ...,
            7.14160299e+00,   7.27028370e+00,   7.25119972e+00],
         [  0.00000000e+00,   0.00000000e+00,   3.13579990e-03, ...,
            7.11172104e+00,   7.24018574e+00,   7.22145796e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.89530004e-03, ...,
            7.02246809e+00,   7.15025949e+00,   7.13205671e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            6.23970628e-01,   6.51930571e-01,   6.65755808e-01],
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            1.89008296e-01,   2.00320795e-01,   2.06820399e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  2.29800004e-04,   1.08067002e-02,   9.62229967e-02, ...,
            6.75160360e+00,   6.85922956e+00,   6.83517504e+00],
         [  2.22000002e-04,   1.05796000e-02,   9.49361995e-02, ...,
            6.72050095e+00,   6.82789373e+00,   6.80362940e+00],
         [  1.99999995e-04,   9.92020033e-03,   9.11398008e-02, ...,
            6.62713575e+00,   6.73329639e+00,   6.71003056e+00],
         ..., 
         [  0.00000000e+00,   5.10000018e-06,   1.47900006e-04, ...,
            5.48654497e-01,   5.72791815e-01,   5.80892026e-01],
         [  0.00000000e+00,   2.49999994e-06,   6.31000003e-05, ...,
            2.03703105e-01,   2.17257798e-01,   2.22078100e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.64000007e-05,   3.99489980e-03,   5.83126992e-02, ...,
            6.74228239e+00,   6.85094452e+00,   6.82739258e+00],
         [  3.49000002e-05,   3.89640010e-03,   5.74234016e-02, ...,
            6.71117973e+00,   6.81961107e+00,   6.79639339e+00],
         [  3.08000017e-05,   3.61169991e-03,   5.48100993e-02, ...,
            6.61781979e+00,   6.72501373e+00,   6.70279741e+00],
         ..., 
         [  0.00000000e+00,   1.20000004e-06,   6.14000019e-05, ...,
            5.44404387e-01,   5.68835974e-01,   5.77289820e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.75999992e-05, ...,
            2.00637802e-01,   2.14354798e-01,   2.19389200e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.48260000e-03,   3.54324989e-02, ...,
            6.73296356e+00,   6.84265900e+00,   6.82015610e+00],
         [  0.00000000e+00,   1.44060003e-03,   3.48262005e-02, ...,
            6.70186090e+00,   6.81132603e+00,   6.78861046e+00],
         [  0.00000000e+00,   1.32020004e-03,   3.30503993e-02, ...,
            6.60850143e+00,   6.71673107e+00,   6.69501734e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.71000008e-05, ...,
            5.40154219e-01,   5.64880073e-01,   5.73687613e-01],
         [  0.00000000e+00,   1.00000001e-07,   1.26000004e-05, ...,
            1.97615594e-01,   2.11489797e-01,   2.16733098e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   7.69000035e-05,   8.03130027e-03, ...,
            6.70554399e+00,   6.81780577e+00,   6.79735470e+00],
         [  0.00000000e+00,   7.39000025e-05,   7.84969982e-03, ...,
            6.67444372e+00,   6.78647232e+00,   6.76635838e+00],
         [  0.00000000e+00,   6.54000032e-05,   7.32359989e-03, ...,
            6.58109188e+00,   6.69188547e+00,   6.67276764e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.79999995e-06, ...,
            5.27613521e-01,   5.53283513e-01,   5.62990129e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            1.88834593e-01,   2.03133598e-01,   2.08956093e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.87999992e-05,   4.90880013e-03, ...,
            6.69622517e+00,   6.80952024e+00,   6.79012156e+00],
         [  0.00000000e+00,   2.75999992e-05,   4.78880014e-03, ...,
            6.66512489e+00,   6.77818966e+00,   6.75857830e+00],
         [  0.00000000e+00,   2.40999998e-05,   4.44239983e-03, ...,
            6.57177591e+00,   6.68360281e+00,   6.66553402e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            5.23497820e-01,   5.49435973e-01,   5.59442282e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.85995594e-01,   2.00420499e-01,   2.06431195e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   3.00280005e-03, ...,
            6.68690634e+00,   6.80123520e+00,   6.78233862e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.92390003e-03, ...,
            6.65580606e+00,   6.76990700e+00,   6.75134230e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.69729993e-03, ...,
            6.56245947e+00,   6.67532301e+00,   6.65775442e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            5.19419730e-01,   5.45642674e-01,   5.55949271e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.83199704e-01,   1.97745398e-01,   2.03933597e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  2.16100001e-04,   1.02049001e-02,   9.11696032e-02, ...,
            6.36338997e+00,   6.45821190e+00,   6.43479300e+00],
         [  2.08800004e-04,   9.98819992e-03,   8.99311975e-02, ...,
            6.33109903e+00,   6.42568445e+00,   6.40258265e+00],
         [  1.87900005e-04,   9.35900025e-03,   8.62796977e-02, ...,
            6.23368359e+00,   6.32755280e+00,   6.30540562e+00],
         ..., 
         [  0.00000000e+00,   4.80000017e-06,   1.39199998e-04, ...,
            4.59726900e-01,   4.81187105e-01,   4.86550689e-01],
         [  0.00000000e+00,   2.30000001e-06,   5.93000004e-05, ...,
            1.75960705e-01,   1.88354000e-01,   1.92037299e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.41999985e-05,   3.76689993e-03,   5.51913008e-02, ...,
            6.35471106e+00,   6.45056057e+00,   6.42764091e+00],
         [  3.27999987e-05,   3.67300003e-03,   5.43375015e-02, ...,
            6.32188129e+00,   6.41749001e+00,   6.39543056e+00],
         [  2.89000000e-05,   3.40240006e-03,   5.18306009e-02, ...,
            6.22500753e+00,   6.31990385e+00,   6.29825354e+00],
         ..., 
         [  0.00000000e+00,   1.09999996e-06,   5.75999984e-05, ...,
            4.56144512e-01,   4.77866292e-01,   4.83506590e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.59000008e-05, ...,
            1.73315600e-01,   1.85841694e-01,   1.89714506e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.39620004e-03,   3.35027017e-02, ...,
            6.34603214e+00,   6.44236898e+00,   6.42048597e+00],
         [  0.00000000e+00,   1.35629997e-03,   3.29227000e-02, ...,
            6.31320477e+00,   6.40984154e+00,   6.38827848e+00],
         [  0.00000000e+00,   1.24200003e-03,   3.12226005e-02, ...,
            6.21633101e+00,   6.31171227e+00,   6.29110432e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.54000006e-05, ...,
            4.52588886e-01,   4.74567086e-01,   4.80489790e-01],
         [  0.00000000e+00,   1.00000001e-07,   1.17999998e-05, ...,
            1.70713603e-01,   1.83361903e-01,   1.87424600e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   7.21999968e-05,   7.57599995e-03, ...,
            6.31945896e+00,   6.41887760e+00,   6.39957619e+00],
         [  0.00000000e+00,   6.92999965e-05,   7.40269991e-03, ...,
            6.28717041e+00,   6.38635206e+00,   6.36682224e+00],
         [  0.00000000e+00,   6.14000019e-05,   6.90140016e-03, ...,
            6.19030190e+00,   6.28876877e+00,   6.27019739e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.60000002e-06, ...,
            4.42094803e-01,   4.64805514e-01,   4.71537799e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.30000001e-06, ...,
            1.63139194e-01,   1.76128805e-01,   1.80707797e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.70000000e-05,   4.62719984e-03, ...,
            6.31078005e+00,   6.41122866e+00,   6.39242411e+00],
         [  0.00000000e+00,   2.58000000e-05,   4.51290002e-03, ...,
            6.27849150e+00,   6.37870359e+00,   6.36021662e+00],
         [  0.00000000e+00,   2.25999993e-05,   4.18339996e-03, ...,
            6.18216419e+00,   6.28057957e+00,   6.26304531e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.30000001e-06, ...,
            4.38652396e-01,   4.61598605e-01,   4.68592107e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.60688102e-01,   1.73779204e-01,   1.78527206e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   2.82890000e-03, ...,
            6.30210114e+00,   6.40357733e+00,   6.38526964e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.75389990e-03, ...,
            6.26981497e+00,   6.37050962e+00,   6.35306454e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.53829989e-03, ...,
            6.17348766e+00,   6.27293110e+00,   6.25589561e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.00000021e-07, ...,
            4.35236990e-01,   4.58407998e-01,   4.65662688e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.58280000e-01,   1.71462297e-01,   1.76368400e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       ..., 
       [[[  1.10300003e-04,   5.45680011e-03,   5.05620018e-02, ...,
            3.12169504e+00,   3.13715339e+00,   3.12665820e+00],
         [  1.06500003e-04,   5.33809979e-03,   4.98499013e-02, ...,
            3.10240889e+00,   3.11789036e+00,   3.10752988e+00],
         [  9.57000011e-05,   4.99449996e-03,   4.77560014e-02, ...,
            3.04498196e+00,   3.06064415e+00,   3.05063677e+00],
         ..., 
         [  0.00000000e+00,   2.49999994e-06,   7.56000009e-05, ...,
            2.08547607e-01,   2.18382597e-01,   2.20232397e-01],
         [  0.00000000e+00,   1.20000004e-06,   3.22999986e-05, ...,
            8.06510970e-02,   8.63090008e-02,   8.77989009e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  1.70000003e-05,   1.98030006e-03,   3.02383006e-02, ...,
            3.11738515e+00,   3.13324642e+00,   3.12316036e+00],
         [  1.63000004e-05,   1.92990003e-03,   2.97535006e-02, ...,
            3.09809923e+00,   3.11403775e+00,   3.10408688e+00],
         [  1.43999996e-05,   1.78499997e-03,   2.83387993e-02, ...,
            3.04067206e+00,   3.05679154e+00,   3.04713917e+00],
         ..., 
         [  0.00000000e+00,   6.00000021e-07,   3.08999988e-05, ...,
            2.06920594e-01,   2.16874093e-01,   2.18855098e-01],
         [  0.00000000e+00,   3.00000011e-07,   1.39000003e-05, ...,
            7.94389993e-02,   8.51586983e-02,   8.67331997e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   7.22899975e-04,   1.81559008e-02, ...,
            3.11302161e+00,   3.12939382e+00,   3.11971736e+00],
         [  0.00000000e+00,   7.01799989e-04,   1.78316999e-02, ...,
            3.09373569e+00,   3.11018515e+00,   3.10058904e+00],
         [  0.00000000e+00,   6.41699997e-04,   1.68855004e-02, ...,
            3.03636241e+00,   3.05293894e+00,   3.04369593e+00],
         ..., 
         [  0.00000000e+00,   1.00000001e-07,   1.35000000e-05, ...,
            2.05309898e-01,   2.15376407e-01,   2.17488796e-01],
         [  0.00000000e+00,   1.00000001e-07,   6.30000022e-06, ...,
            7.82483965e-02,   8.40191990e-02,   8.56892988e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   3.59000005e-05,   3.99329979e-03, ...,
            3.10003853e+00,   3.11783624e+00,   3.10927868e+00],
         [  0.00000000e+00,   3.45000008e-05,   3.89979989e-03, ...,
            3.08080649e+00,   3.09868169e+00,   3.09020519e+00],
         [  0.00000000e+00,   3.04999994e-05,   3.62979993e-03, ...,
            3.02354097e+00,   3.04148960e+00,   3.03336668e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            2.00547606e-01,   2.10948706e-01,   2.13433594e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            7.47736990e-02,   8.07038024e-02,   8.26179013e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.33000003e-05,   2.41929991e-03, ...,
            3.09572887e+00,   3.11398363e+00,   3.10578108e+00],
         [  0.00000000e+00,   1.27000003e-05,   2.35820003e-03, ...,
            3.07649684e+00,   3.09482908e+00,   3.08676195e+00],
         [  0.00000000e+00,   1.10999999e-05,   2.18249997e-03, ...,
            3.01923132e+00,   3.03769135e+00,   3.02997828e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.98985398e-01,   2.09489003e-01,   2.12100103e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            7.36531988e-02,   7.96239972e-02,   8.16176981e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   1.46770000e-03, ...,
            3.09141922e+00,   3.11018515e+00,   3.10233784e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.42800005e-03, ...,
            3.07218695e+00,   3.09097648e+00,   3.08326435e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.31409999e-03, ...,
            3.01497531e+00,   3.03389287e+00,   3.02653503e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.97433904e-01,   2.08045706e-01,   2.10777506e-01],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            7.25487992e-02,   7.85657987e-02,   8.06339979e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  6.76999989e-05,   3.46309994e-03,   3.28803994e-02, ...,
            1.91745019e+00,   1.91365540e+00,   1.90873158e+00],
         [  6.54000032e-05,   3.38799995e-03,   3.24189998e-02, ...,
            1.90565240e+00,   1.90198910e+00,   1.89714527e+00],
         [  5.88000003e-05,   3.17010004e-03,   3.10558006e-02, ...,
            1.87052810e+00,   1.86720717e+00,   1.86255038e+00],
         ..., 
         [  0.00000000e+00,   1.60000002e-06,   4.91999999e-05, ...,
            1.29054695e-01,   1.34390503e-01,   1.35515794e-01],
         [  0.00000000e+00,   8.00000009e-07,   2.09999998e-05, ...,
            4.99616005e-02,   5.31668998e-02,   5.40850013e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  1.03000002e-05,   1.24230003e-03,   1.95126999e-02, ...,
            1.91475666e+00,   1.91126788e+00,   1.90660012e+00],
         [  9.89999990e-06,   1.21070002e-03,   1.92015003e-02, ...,
            1.90295875e+00,   1.89960158e+00,   1.89501393e+00],
         [  8.69999985e-06,   1.12000003e-03,   1.82886999e-02, ...,
            1.86783457e+00,   1.86487389e+00,   1.86041903e+00],
         ..., 
         [  0.00000000e+00,   4.00000005e-07,   1.99999995e-05, ...,
            1.28047302e-01,   1.33462593e-01,   1.34668693e-01],
         [  0.00000000e+00,   2.00000002e-07,   9.00000032e-06, ...,
            4.92100008e-02,   5.24565987e-02,   5.34303002e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   4.48600011e-04,   1.16341002e-02, ...,
            1.91206312e+00,   1.90888035e+00,   1.90446877e+00],
         [  0.00000000e+00,   4.35599999e-04,   1.14268996e-02, ...,
            1.90026522e+00,   1.89721406e+00,   1.89288247e+00],
         [  0.00000000e+00,   3.98400007e-04,   1.08212000e-02, ...,
            1.86519480e+00,   1.86254060e+00,   1.85828757e+00],
         ..., 
         [  0.00000000e+00,   1.00000001e-07,   8.69999985e-06, ...,
            1.27050698e-01,   1.32540196e-01,   1.33827105e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.99999999e-06, ...,
            4.84704003e-02,   5.17560989e-02,   5.27831987e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   2.16999997e-05,   2.51160003e-03, ...,
            1.90403616e+00,   1.90177202e+00,   1.89801979e+00],
         [  0.00000000e+00,   2.08000001e-05,   2.45300005e-03, ...,
            1.89223838e+00,   1.89015996e+00,   1.88643348e+00],
         [  0.00000000e+00,   1.84000000e-05,   2.28350004e-03, ...,
            1.85722184e+00,   1.85548663e+00,   1.85194790e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   8.99999975e-07, ...,
            1.24098502e-01,   1.29805401e-01,   1.31329507e-01],
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            4.63171005e-02,   4.97104004e-02,   5.08899987e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   7.90000013e-06,   1.51320000e-03, ...,
            1.90134263e+00,   1.89938450e+00,   1.89588833e+00],
         [  0.00000000e+00,   7.60000012e-06,   1.47510006e-03, ...,
            1.88959861e+00,   1.88777244e+00,   1.88430202e+00],
         [  0.00000000e+00,   6.59999978e-06,   1.36540004e-03, ...,
            1.85458207e+00,   1.85309911e+00,   1.84981644e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            1.23128802e-01,   1.28910094e-01,   1.30504206e-01],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            4.56217006e-02,   4.90473993e-02,   5.02746999e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   9.13100026e-04, ...,
            1.89870286e+00,   1.89705122e+00,   1.89375687e+00],
         [  0.00000000e+00,   0.00000000e+00,   8.88400013e-04, ...,
            1.88690507e+00,   1.88543916e+00,   1.88217056e+00],
         [  0.00000000e+00,   0.00000000e+00,   8.17699998e-04, ...,
            1.85188854e+00,   1.85076582e+00,   1.84768498e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            1.22169897e-01,   1.28020197e-01,   1.29689902e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            4.49359007e-02,   4.83924001e-02,   4.96664010e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  3.57999998e-05,   1.92870002e-03,   1.89859997e-02, ...,
            1.06622577e+00,   1.05327833e+00,   1.05216610e+00],
         [  3.46000015e-05,   1.88690005e-03,   1.87187009e-02, ...,
            1.05970728e+00,   1.04687536e+00,   1.04582644e+00],
         [  3.11000003e-05,   1.76570006e-03,   1.79334003e-02, ...,
            1.04025972e+00,   1.02782941e+00,   1.02680743e+00],
         ..., 
         [  0.00000000e+00,   8.99999975e-07,   2.83999998e-05, ...,
            7.25433975e-02,   7.47457966e-02,   7.54147023e-02],
         [  0.00000000e+00,   4.00000005e-07,   1.21000003e-05, ...,
            2.81419996e-02,   2.96302997e-02,   3.01632006e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  5.29999988e-06,   6.79999997e-04,   1.11498004e-02, ...,
            1.06471741e+00,   1.05192173e+00,   1.05096376e+00],
         [  5.10000018e-06,   6.62799983e-04,   1.09719997e-02, ...,
            1.05819893e+00,   1.04557312e+00,   1.04462409e+00],
         [  4.50000016e-06,   6.13100012e-04,   1.04507999e-02, ...,
            1.03875124e+00,   1.02652717e+00,   1.02560508e+00],
         ..., 
         [  0.00000000e+00,   2.00000002e-07,   1.14000004e-05, ...,
            7.19724000e-02,   7.42248967e-02,   7.49391988e-02],
         [  0.00000000e+00,   1.00000001e-07,   5.10000018e-06, ...,
            2.77180001e-02,   2.92342007e-02,   2.97975000e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.41600006e-04,   6.58260006e-03, ...,
            1.06320894e+00,   1.05061948e+00,   1.04976141e+00],
         [  0.00000000e+00,   2.34599996e-04,   6.46529999e-03, ...,
            1.05669057e+00,   1.04421651e+00,   1.04342175e+00],
         [  0.00000000e+00,   2.14600004e-04,   6.12290017e-03, ...,
            1.03724289e+00,   1.02517056e+00,   1.02445734e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.90000002e-06, ...,
            7.14121014e-02,   7.37093985e-02,   7.44692013e-02],
         [  0.00000000e+00,   0.00000000e+00,   2.30000001e-06, ...,
            2.73004994e-02,   2.88428999e-02,   2.94362996e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   1.11999998e-05,   1.38300005e-03, ...,
            1.05862987e+00,   1.04660404e+00,   1.04615438e+00],
         [  0.00000000e+00,   1.06999996e-05,   1.35070004e-03, ...,
            1.05211151e+00,   1.04025543e+00,   1.03981471e+00],
         [  0.00000000e+00,   9.49999958e-06,   1.25750003e-03, ...,
            1.03271770e+00,   1.02126372e+00,   1.02085030e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.99999999e-07, ...,
            6.97475001e-02,   7.21845999e-02,   7.30756000e-02],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            2.60857008e-02,   2.77006999e-02,   2.83787996e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   3.99999999e-06,   8.26200005e-04, ...,
            1.05712152e+00,   1.04530180e+00,   1.04500663e+00],
         [  0.00000000e+00,   3.90000014e-06,   8.05400021e-04, ...,
            1.05060303e+00,   1.03895307e+00,   1.03861237e+00],
         [  0.00000000e+00,   3.39999997e-06,   7.45499972e-04, ...,
            1.03120923e+00,   1.01996148e+00,   1.01970267e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            6.92033991e-02,   7.16854036e-02,   7.26165026e-02],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            2.56929994e-02,   2.73305997e-02,   2.80344002e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   4.94399981e-04, ...,
            1.05561304e+00,   1.04399943e+00,   1.04380429e+00],
         [  0.00000000e+00,   0.00000000e+00,   4.81099996e-04, ...,
            1.04909468e+00,   1.03759658e+00,   1.03741002e+00],
         [  0.00000000e+00,   0.00000000e+00,   4.42799996e-04, ...,
            1.02975476e+00,   1.01865911e+00,   1.01850033e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            6.86592981e-02,   7.11916015e-02,   7.21628964e-02],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            2.53062006e-02,   2.69648992e-02,   2.76951008e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]]], dtype=float32))"""
str = image.__str__()
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########## test ImageLight.export(filename) ###########

print("test ImageLight.export(filename)")
ipix_ref = 1
ibin45N_ref = 2
filename = "../Outputs/foo_ImageLight.nc"
image.export_primary_production(filename)
array1d_ipix_lat \
= Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon \
= Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
array2d_ipix_itime_cf \
    = Netcdf_tools.get_array2d_i_j_val(filename, "CF")
array2d_ipix_itime_o3 \
    = Netcdf_tools.get_array2d_i_j_val(filename, "O3")
array2d_ipix_itime_taucld \
    = Netcdf_tools.get_array2d_i_j_val(filename, "TauCld")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
array1d_itime_cf_read = array2d_ipix_itime_cf[ipix_ref,]
array1d_itime_o3_read = array2d_ipix_itime_o3[ipix_ref,]
array1d_itime_taucld_read = array2d_ipix_itime_taucld[ipix_ref,]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref \
   and np.allclose(array1d_itime_cf_read, array1d_itime_cf_ref) \
   and np.allclose(array1d_itime_o3_read, array1d_itime_o3_ref) \
   and np.allclose(array1d_itime_taucld_read, array1d_itime_taucld_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWaterLight.__init__(year, month, day, doy, grid_file,
########### rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus)

print("test ImageWaterLight.__init__(year, month, day, doy, grid_file, rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus)")

ipix_ref = 2
npix_ref = 3479813
# TEST
npix_ref = 3

image = image_with_primary_production_pixel.ImageWaterLight(year,
                                                            month,
                                                            day,
                                                            doy,
                                                            grid_file,
                                                            rrs_type,
                                                            rrs_file,
                                                            chl_file,
                                                            atm_file,
                                                            lut_ed0minus)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(image.array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10],
                   ed0minus_ref,
                   rtol = 1e-03) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)
########### test ImageWaterLight.__init__(year, month, day, doy, grid_file,
########### rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus, 
########### array1d_ipix_ibin45N)

print("test ImageWaterLight.__init__(year, month, day, doy, grid_file, rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus, array1d_ipix_ibin45N)")

ipix_ref = 1
npix_ref = 3479813
# TEST
npix_ref = 2

# Array of dimension npix. The number of pixels in the resulting image.
# The first dimension is the indices of the pixel in the resulting image.
# The values are the indices (0-based) of the pixels in the ISIN grid above 45
# degrees North.
# Units: Unitless.                                                             
array1d_ipix_ibin45N = np.array([0, 2], dtype = np.int32)

image = image_with_primary_production_pixel.ImageWaterLight(year,
                                                            month,
                                                            day,
                                                            doy,
                                                            grid_file,
                                                            rrs_type,
                                                            rrs_file,
                                                            chl_file,
                                                            atm_file,
                                                            lut_ed0minus,
                                                            array1d_ipix_ibin45N)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(image.array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10],
                   ed0minus_ref,
                   rtol = 1e-03) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWaterLight.export(filename) ###########

print('test ImageWaterLight.export(filename)')
ipix_ref = 1
ibin45N_ref = 2
filename = "../Outputs/foo_ImageWaterLight.nc"
image.export_primary_production(filename)
array1d_ipix_lat \
= Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon \
= Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
array2d_ipix_iband_Rrs \
    = Netcdf_tools.get_array2d_i_j_val(filename, "Rrs")
array2d_ipix_idepth_chl \
    = Netcdf_tools.get_array2d_i_j_val(filename, "chlz")
array2d_ipix_itime_cf \
    = Netcdf_tools.get_array2d_i_j_val(filename, "CF")
array2d_ipix_itime_o3 \
    = Netcdf_tools.get_array2d_i_j_val(filename, "O3")
array2d_ipix_itime_taucld \
    = Netcdf_tools.get_array2d_i_j_val(filename, "TauCld")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
array1d_iband_Rrs_read = array2d_ipix_iband_Rrs[ipix_ref,]
array1d_idepth_chlz_read = array2d_ipix_idepth_chl[ipix_ref,]
array1d_itime_cf_read = array2d_ipix_itime_cf[ipix_ref,]
array1d_itime_o3_read = array2d_ipix_itime_o3[ipix_ref,]
array1d_itime_taucld_read = array2d_ipix_itime_taucld[ipix_ref,]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref \
   and np.allclose(array1d_iband_Rrs_read, array1d_iband_Rrs_ref) \
   and np.allclose(array1d_idepth_chlz_read, array1d_idepth_chl_ref) \
   and np.allclose(array1d_itime_cf_read, array1d_itime_cf_ref) \
   and np.allclose(array1d_itime_o3_read, array1d_itime_o3_ref) \
   and np.allclose(array1d_itime_taucld_read, array1d_itime_taucld_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWaterLight.export(filename, grid_file) ###########

print('test ImageWaterLight.export(filename, grid_file)')
filename = "../Outputs/foo_ImageWaterLight.nc"
ipix_ref = 2
ibin45N_ref = 2
image.export_primary_production(filename, grid_file)
array1d_ipix_lat \
= Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon \
= Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
array2d_ipix_iband_Rrs \
    = Netcdf_tools.get_array2d_i_j_val(filename, "Rrs")
array2d_ipix_idepth_chl \
    = Netcdf_tools.get_array2d_i_j_val(filename, "chlz")
array2d_ipix_itime_cf \
    = Netcdf_tools.get_array2d_i_j_val(filename, "CF")
array2d_ipix_itime_o3 \
    = Netcdf_tools.get_array2d_i_j_val(filename, "O3")
array2d_ipix_itime_taucld \
    = Netcdf_tools.get_array2d_i_j_val(filename, "TauCld")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
array1d_iband_Rrs_read = array2d_ipix_iband_Rrs[ipix_ref,]
array1d_idepth_chlz_read = array2d_ipix_idepth_chl[ipix_ref,]
array1d_itime_cf_read = array2d_ipix_itime_cf[ipix_ref,]
array1d_itime_o3_read = array2d_ipix_itime_o3[ipix_ref,]
array1d_itime_taucld_read = array2d_ipix_itime_taucld[ipix_ref,]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref \
   and np.allclose(array1d_iband_Rrs_read, array1d_iband_Rrs_ref) \
   and np.allclose(array1d_idepth_chlz_read, array1d_idepth_chl_ref) \
   and np.allclose(array1d_itime_cf_read, array1d_itime_cf_ref) \
   and np.allclose(array1d_itime_o3_read, array1d_itime_o3_ref) \
   and np.allclose(array1d_itime_taucld_read, array1d_itime_taucld_ref):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

############ test ImageWaterLight.__repr__() ###########

print("test ImageWaterLight.__repr__()")

str_ref = \
"""ImageWaterLight(array1d_ipix_pixel = array([ PixelWaterLight(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0, rrs_type = 'A', array1d_iband_Rrs = [0.008642000146210194, 0.008084000088274479, 0.006331999786198139, 0.00469799991697073, 0.003625999903306365, 0.0020359999034553766], array1d_idepth_chl = [0.2825790047645569, 0.28540900349617004, 0.28870299458503723, 0.2924950122833252, 0.29681700468063354, 0.30170199275016785, 0.3071799874305725, 0.313277006149292, 0.3200179934501648, 0.32742199301719666, 0.33550500869750977, 0.3442760109901428, 0.353738009929657, 0.3638859987258911, 0.37470901012420654, 0.3861849904060364, 0.39828601479530334, 0.410971999168396, 0.42419400811195374, 0.43789398670196533, 0.45200398564338684, 0.4664449989795685, 0.481128990650177, 0.4959630072116852, 0.5108399987220764, 0.5256519913673401, 0.5402809977531433, 0.5546069741249084, 0.5685070157051086, 0.581853985786438, 0.5945240259170532, 0.6063950061798096, 0.6173480153083801, 0.627269983291626, 0.6360549926757812, 0.6436060070991516, 0.6498379707336426, 0.6546769738197327, 0.6580619812011719, 0.6599469780921936, 0.6603019833564758, 0.6591100096702576, 0.6563720107078552, 0.6521040201187134, 0.6463389992713928, 0.6391239762306213, 0.6305199861526489, 0.6206009984016418, 0.6094539761543274, 0.5971760153770447, 0.583873987197876, 0.5696600079536438, 0.5546550154685974, 0.5389800071716309, 0.5227599740028381, 0.5061209797859192, 0.48918700218200684, 0.47207701206207275, 0.45490700006484985, 0.4377889931201935, 0.4208250045776367, 0.40411099791526794, 0.38773301243782043, 0.3717679977416992, 0.3562859892845154, 0.3413420021533966, 0.32698699831962585, 0.31325799226760864, 0.3001840114593506, 0.28778600692749023, 0.27607399225234985, 0.26505300402641296, 0.254720002412796, 0.24506500363349915, 0.23607300221920013, 0.22772200405597687, 0.21999000012874603, 0.21284900605678558, 0.20626799762248993, 0.20021599531173706, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514]),
       PixelWaterLight(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2, rrs_type = 'A', array1d_iband_Rrs = [6.399999983841553e-05, 0.0007999999797903001, 0.0017180000431835651, 0.0033179998863488436, 0.0039900001138448715, 0.0011520000407472253], array1d_idepth_chl = [51.34635543823242, 54.6530876159668, 59.353553771972656, 64.84622192382812, 69.99886322021484, 73.42073059082031, 73.95088195800781, 71.13446807861328, 65.42147827148438, 57.970096588134766, 50.17124938964844, 43.15963363647461, 37.539974212646484, 33.391170501708984, 30.453460693359375, 28.350486755371094, 26.74401092529297, 25.396499633789062, 24.168567657470703, 22.989830017089844, 21.829195022583008, 20.674541473388672, 19.521663665771484, 18.369260787963867, 17.21697425842285, 16.06471061706543, 14.912453651428223, 13.760197639465332, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514])], dtype=object), array4d_itaucld_io3_ithetas_iwl_ed0minus = array([[[[  2.46599986e-04,   1.15595004e-02,   1.02635399e-01, ...,
            7.21043253e+00,   7.33221912e+00,   7.30728006e+00],
         [  2.38399996e-04,   1.13199996e-02,   1.01288103e-01, ...,
            7.18108988e+00,   7.30266428e+00,   7.27753830e+00],
         [  2.14900007e-04,   1.06236003e-02,   9.73128974e-02, ...,
            7.09181023e+00,   7.21219444e+00,   7.18813705e+00],
         ..., 
         [  0.00000000e+00,   5.50000004e-06,   1.57799994e-04, ...,
            6.59078896e-01,   6.84351087e-01,   6.95586503e-01],
         [  0.00000000e+00,   2.70000010e-06,   6.73000031e-05, ...,
            2.10019693e-01,   2.19942600e-01,   2.25101799e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.90999994e-05,   4.27869987e-03,   6.22630008e-02, ...,
            7.20080853e+00,   7.32366276e+00,   7.29871464e+00],
         [  3.75999989e-05,   4.17440012e-03,   6.13318011e-02, ...,
            7.17095280e+00,   7.29359102e+00,   7.26951933e+00],
         [  3.31000010e-05,   3.87299992e-03,   5.85886016e-02, ...,
            7.08167362e+00,   7.20366430e+00,   7.18011808e+00],
         ..., 
         [  0.00000000e+00,   1.30000001e-06,   6.55999975e-05, ...,
            6.53923213e-01,   6.79589927e-01,   6.91259086e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.95000009e-05, ...,
            2.06878603e-01,   2.17028797e-01,   2.22394004e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.58960000e-03,   3.78668010e-02, ...,
            7.19067144e+00,   7.31458950e+00,   7.29069567e+00],
         [  0.00000000e+00,   1.54500001e-03,   3.72284018e-02, ...,
            7.16135454e+00,   7.28449202e+00,   7.26152658e+00],
         [  0.00000000e+00,   1.41729997e-03,   3.53609994e-02, ...,
            7.07207537e+00,   7.19459105e+00,   7.17209911e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.90000007e-05, ...,
            6.48858905e-01,   6.74920619e-01,   6.86969817e-01],
         [  0.00000000e+00,   2.00000002e-07,   1.35000000e-05, ...,
            2.03784794e-01,   2.14146897e-01,   2.19713494e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   8.26999967e-05,   8.60089995e-03, ...,
            7.16133785e+00,   7.28788710e+00,   7.26666498e+00],
         [  0.00000000e+00,   7.95000014e-05,   8.40890035e-03, ...,
            7.13145638e+00,   7.25778913e+00,   7.23746967e+00],
         [  0.00000000e+00,   7.04999984e-05,   7.85250030e-03, ...,
            7.04220343e+00,   7.16788864e+00,   7.14806843e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-06, ...,
            6.33799374e-01,   6.61026120e-01,   6.74144387e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.50000005e-06, ...,
            1.94786206e-01,   2.05736294e-01,   2.11883903e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   3.09999996e-05,   5.25970012e-03, ...,
            7.15120125e+00,   7.27935648e+00,   7.25921869e+00],
         [  0.00000000e+00,   2.97000006e-05,   5.13269985e-03, ...,
            7.12185812e+00,   7.24925900e+00,   7.22947693e+00],
         [  0.00000000e+00,   2.59999997e-05,   4.76620020e-03, ...,
            7.03260517e+00,   7.15935850e+00,   7.14007568e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.50000005e-06, ...,
            6.28884971e-01,   6.56486571e-01,   6.69931114e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.91874802e-01,   2.03007996e-01,   2.09335804e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   3.21920007e-03, ...,
            7.14160299e+00,   7.27028370e+00,   7.25119972e+00],
         [  0.00000000e+00,   0.00000000e+00,   3.13579990e-03, ...,
            7.11172104e+00,   7.24018574e+00,   7.22145796e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.89530004e-03, ...,
            7.02246809e+00,   7.15025949e+00,   7.13205671e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            6.23970628e-01,   6.51930571e-01,   6.65755808e-01],
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            1.89008296e-01,   2.00320795e-01,   2.06820399e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  2.29800004e-04,   1.08067002e-02,   9.62229967e-02, ...,
            6.75160360e+00,   6.85922956e+00,   6.83517504e+00],
         [  2.22000002e-04,   1.05796000e-02,   9.49361995e-02, ...,
            6.72050095e+00,   6.82789373e+00,   6.80362940e+00],
         [  1.99999995e-04,   9.92020033e-03,   9.11398008e-02, ...,
            6.62713575e+00,   6.73329639e+00,   6.71003056e+00],
         ..., 
         [  0.00000000e+00,   5.10000018e-06,   1.47900006e-04, ...,
            5.48654497e-01,   5.72791815e-01,   5.80892026e-01],
         [  0.00000000e+00,   2.49999994e-06,   6.31000003e-05, ...,
            2.03703105e-01,   2.17257798e-01,   2.22078100e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.64000007e-05,   3.99489980e-03,   5.83126992e-02, ...,
            6.74228239e+00,   6.85094452e+00,   6.82739258e+00],
         [  3.49000002e-05,   3.89640010e-03,   5.74234016e-02, ...,
            6.71117973e+00,   6.81961107e+00,   6.79639339e+00],
         [  3.08000017e-05,   3.61169991e-03,   5.48100993e-02, ...,
            6.61781979e+00,   6.72501373e+00,   6.70279741e+00],
         ..., 
         [  0.00000000e+00,   1.20000004e-06,   6.14000019e-05, ...,
            5.44404387e-01,   5.68835974e-01,   5.77289820e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.75999992e-05, ...,
            2.00637802e-01,   2.14354798e-01,   2.19389200e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.48260000e-03,   3.54324989e-02, ...,
            6.73296356e+00,   6.84265900e+00,   6.82015610e+00],
         [  0.00000000e+00,   1.44060003e-03,   3.48262005e-02, ...,
            6.70186090e+00,   6.81132603e+00,   6.78861046e+00],
         [  0.00000000e+00,   1.32020004e-03,   3.30503993e-02, ...,
            6.60850143e+00,   6.71673107e+00,   6.69501734e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.71000008e-05, ...,
            5.40154219e-01,   5.64880073e-01,   5.73687613e-01],
         [  0.00000000e+00,   1.00000001e-07,   1.26000004e-05, ...,
            1.97615594e-01,   2.11489797e-01,   2.16733098e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   7.69000035e-05,   8.03130027e-03, ...,
            6.70554399e+00,   6.81780577e+00,   6.79735470e+00],
         [  0.00000000e+00,   7.39000025e-05,   7.84969982e-03, ...,
            6.67444372e+00,   6.78647232e+00,   6.76635838e+00],
         [  0.00000000e+00,   6.54000032e-05,   7.32359989e-03, ...,
            6.58109188e+00,   6.69188547e+00,   6.67276764e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.79999995e-06, ...,
            5.27613521e-01,   5.53283513e-01,   5.62990129e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            1.88834593e-01,   2.03133598e-01,   2.08956093e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.87999992e-05,   4.90880013e-03, ...,
            6.69622517e+00,   6.80952024e+00,   6.79012156e+00],
         [  0.00000000e+00,   2.75999992e-05,   4.78880014e-03, ...,
            6.66512489e+00,   6.77818966e+00,   6.75857830e+00],
         [  0.00000000e+00,   2.40999998e-05,   4.44239983e-03, ...,
            6.57177591e+00,   6.68360281e+00,   6.66553402e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            5.23497820e-01,   5.49435973e-01,   5.59442282e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.85995594e-01,   2.00420499e-01,   2.06431195e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   3.00280005e-03, ...,
            6.68690634e+00,   6.80123520e+00,   6.78233862e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.92390003e-03, ...,
            6.65580606e+00,   6.76990700e+00,   6.75134230e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.69729993e-03, ...,
            6.56245947e+00,   6.67532301e+00,   6.65775442e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            5.19419730e-01,   5.45642674e-01,   5.55949271e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.83199704e-01,   1.97745398e-01,   2.03933597e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  2.16100001e-04,   1.02049001e-02,   9.11696032e-02, ...,
            6.36338997e+00,   6.45821190e+00,   6.43479300e+00],
         [  2.08800004e-04,   9.98819992e-03,   8.99311975e-02, ...,
            6.33109903e+00,   6.42568445e+00,   6.40258265e+00],
         [  1.87900005e-04,   9.35900025e-03,   8.62796977e-02, ...,
            6.23368359e+00,   6.32755280e+00,   6.30540562e+00],
         ..., 
         [  0.00000000e+00,   4.80000017e-06,   1.39199998e-04, ...,
            4.59726900e-01,   4.81187105e-01,   4.86550689e-01],
         [  0.00000000e+00,   2.30000001e-06,   5.93000004e-05, ...,
            1.75960705e-01,   1.88354000e-01,   1.92037299e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.41999985e-05,   3.76689993e-03,   5.51913008e-02, ...,
            6.35471106e+00,   6.45056057e+00,   6.42764091e+00],
         [  3.27999987e-05,   3.67300003e-03,   5.43375015e-02, ...,
            6.32188129e+00,   6.41749001e+00,   6.39543056e+00],
         [  2.89000000e-05,   3.40240006e-03,   5.18306009e-02, ...,
            6.22500753e+00,   6.31990385e+00,   6.29825354e+00],
         ..., 
         [  0.00000000e+00,   1.09999996e-06,   5.75999984e-05, ...,
            4.56144512e-01,   4.77866292e-01,   4.83506590e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.59000008e-05, ...,
            1.73315600e-01,   1.85841694e-01,   1.89714506e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.39620004e-03,   3.35027017e-02, ...,
            6.34603214e+00,   6.44236898e+00,   6.42048597e+00],
         [  0.00000000e+00,   1.35629997e-03,   3.29227000e-02, ...,
            6.31320477e+00,   6.40984154e+00,   6.38827848e+00],
         [  0.00000000e+00,   1.24200003e-03,   3.12226005e-02, ...,
            6.21633101e+00,   6.31171227e+00,   6.29110432e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.54000006e-05, ...,
            4.52588886e-01,   4.74567086e-01,   4.80489790e-01],
         [  0.00000000e+00,   1.00000001e-07,   1.17999998e-05, ...,
            1.70713603e-01,   1.83361903e-01,   1.87424600e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   7.21999968e-05,   7.57599995e-03, ...,
            6.31945896e+00,   6.41887760e+00,   6.39957619e+00],
         [  0.00000000e+00,   6.92999965e-05,   7.40269991e-03, ...,
            6.28717041e+00,   6.38635206e+00,   6.36682224e+00],
         [  0.00000000e+00,   6.14000019e-05,   6.90140016e-03, ...,
            6.19030190e+00,   6.28876877e+00,   6.27019739e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.60000002e-06, ...,
            4.42094803e-01,   4.64805514e-01,   4.71537799e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.30000001e-06, ...,
            1.63139194e-01,   1.76128805e-01,   1.80707797e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.70000000e-05,   4.62719984e-03, ...,
            6.31078005e+00,   6.41122866e+00,   6.39242411e+00],
         [  0.00000000e+00,   2.58000000e-05,   4.51290002e-03, ...,
            6.27849150e+00,   6.37870359e+00,   6.36021662e+00],
         [  0.00000000e+00,   2.25999993e-05,   4.18339996e-03, ...,
            6.18216419e+00,   6.28057957e+00,   6.26304531e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.30000001e-06, ...,
            4.38652396e-01,   4.61598605e-01,   4.68592107e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.60688102e-01,   1.73779204e-01,   1.78527206e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   2.82890000e-03, ...,
            6.30210114e+00,   6.40357733e+00,   6.38526964e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.75389990e-03, ...,
            6.26981497e+00,   6.37050962e+00,   6.35306454e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.53829989e-03, ...,
            6.17348766e+00,   6.27293110e+00,   6.25589561e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.00000021e-07, ...,
            4.35236990e-01,   4.58407998e-01,   4.65662688e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.58280000e-01,   1.71462297e-01,   1.76368400e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       ..., 
       [[[  1.10300003e-04,   5.45680011e-03,   5.05620018e-02, ...,
            3.12169504e+00,   3.13715339e+00,   3.12665820e+00],
         [  1.06500003e-04,   5.33809979e-03,   4.98499013e-02, ...,
            3.10240889e+00,   3.11789036e+00,   3.10752988e+00],
         [  9.57000011e-05,   4.99449996e-03,   4.77560014e-02, ...,
            3.04498196e+00,   3.06064415e+00,   3.05063677e+00],
         ..., 
         [  0.00000000e+00,   2.49999994e-06,   7.56000009e-05, ...,
            2.08547607e-01,   2.18382597e-01,   2.20232397e-01],
         [  0.00000000e+00,   1.20000004e-06,   3.22999986e-05, ...,
            8.06510970e-02,   8.63090008e-02,   8.77989009e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  1.70000003e-05,   1.98030006e-03,   3.02383006e-02, ...,
            3.11738515e+00,   3.13324642e+00,   3.12316036e+00],
         [  1.63000004e-05,   1.92990003e-03,   2.97535006e-02, ...,
            3.09809923e+00,   3.11403775e+00,   3.10408688e+00],
         [  1.43999996e-05,   1.78499997e-03,   2.83387993e-02, ...,
            3.04067206e+00,   3.05679154e+00,   3.04713917e+00],
         ..., 
         [  0.00000000e+00,   6.00000021e-07,   3.08999988e-05, ...,
            2.06920594e-01,   2.16874093e-01,   2.18855098e-01],
         [  0.00000000e+00,   3.00000011e-07,   1.39000003e-05, ...,
            7.94389993e-02,   8.51586983e-02,   8.67331997e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   7.22899975e-04,   1.81559008e-02, ...,
            3.11302161e+00,   3.12939382e+00,   3.11971736e+00],
         [  0.00000000e+00,   7.01799989e-04,   1.78316999e-02, ...,
            3.09373569e+00,   3.11018515e+00,   3.10058904e+00],
         [  0.00000000e+00,   6.41699997e-04,   1.68855004e-02, ...,
            3.03636241e+00,   3.05293894e+00,   3.04369593e+00],
         ..., 
         [  0.00000000e+00,   1.00000001e-07,   1.35000000e-05, ...,
            2.05309898e-01,   2.15376407e-01,   2.17488796e-01],
         [  0.00000000e+00,   1.00000001e-07,   6.30000022e-06, ...,
            7.82483965e-02,   8.40191990e-02,   8.56892988e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   3.59000005e-05,   3.99329979e-03, ...,
            3.10003853e+00,   3.11783624e+00,   3.10927868e+00],
         [  0.00000000e+00,   3.45000008e-05,   3.89979989e-03, ...,
            3.08080649e+00,   3.09868169e+00,   3.09020519e+00],
         [  0.00000000e+00,   3.04999994e-05,   3.62979993e-03, ...,
            3.02354097e+00,   3.04148960e+00,   3.03336668e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            2.00547606e-01,   2.10948706e-01,   2.13433594e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            7.47736990e-02,   8.07038024e-02,   8.26179013e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.33000003e-05,   2.41929991e-03, ...,
            3.09572887e+00,   3.11398363e+00,   3.10578108e+00],
         [  0.00000000e+00,   1.27000003e-05,   2.35820003e-03, ...,
            3.07649684e+00,   3.09482908e+00,   3.08676195e+00],
         [  0.00000000e+00,   1.10999999e-05,   2.18249997e-03, ...,
            3.01923132e+00,   3.03769135e+00,   3.02997828e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.98985398e-01,   2.09489003e-01,   2.12100103e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            7.36531988e-02,   7.96239972e-02,   8.16176981e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   1.46770000e-03, ...,
            3.09141922e+00,   3.11018515e+00,   3.10233784e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.42800005e-03, ...,
            3.07218695e+00,   3.09097648e+00,   3.08326435e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.31409999e-03, ...,
            3.01497531e+00,   3.03389287e+00,   3.02653503e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.97433904e-01,   2.08045706e-01,   2.10777506e-01],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            7.25487992e-02,   7.85657987e-02,   8.06339979e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  6.76999989e-05,   3.46309994e-03,   3.28803994e-02, ...,
            1.91745019e+00,   1.91365540e+00,   1.90873158e+00],
         [  6.54000032e-05,   3.38799995e-03,   3.24189998e-02, ...,
            1.90565240e+00,   1.90198910e+00,   1.89714527e+00],
         [  5.88000003e-05,   3.17010004e-03,   3.10558006e-02, ...,
            1.87052810e+00,   1.86720717e+00,   1.86255038e+00],
         ..., 
         [  0.00000000e+00,   1.60000002e-06,   4.91999999e-05, ...,
            1.29054695e-01,   1.34390503e-01,   1.35515794e-01],
         [  0.00000000e+00,   8.00000009e-07,   2.09999998e-05, ...,
            4.99616005e-02,   5.31668998e-02,   5.40850013e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  1.03000002e-05,   1.24230003e-03,   1.95126999e-02, ...,
            1.91475666e+00,   1.91126788e+00,   1.90660012e+00],
         [  9.89999990e-06,   1.21070002e-03,   1.92015003e-02, ...,
            1.90295875e+00,   1.89960158e+00,   1.89501393e+00],
         [  8.69999985e-06,   1.12000003e-03,   1.82886999e-02, ...,
            1.86783457e+00,   1.86487389e+00,   1.86041903e+00],
         ..., 
         [  0.00000000e+00,   4.00000005e-07,   1.99999995e-05, ...,
            1.28047302e-01,   1.33462593e-01,   1.34668693e-01],
         [  0.00000000e+00,   2.00000002e-07,   9.00000032e-06, ...,
            4.92100008e-02,   5.24565987e-02,   5.34303002e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   4.48600011e-04,   1.16341002e-02, ...,
            1.91206312e+00,   1.90888035e+00,   1.90446877e+00],
         [  0.00000000e+00,   4.35599999e-04,   1.14268996e-02, ...,
            1.90026522e+00,   1.89721406e+00,   1.89288247e+00],
         [  0.00000000e+00,   3.98400007e-04,   1.08212000e-02, ...,
            1.86519480e+00,   1.86254060e+00,   1.85828757e+00],
         ..., 
         [  0.00000000e+00,   1.00000001e-07,   8.69999985e-06, ...,
            1.27050698e-01,   1.32540196e-01,   1.33827105e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.99999999e-06, ...,
            4.84704003e-02,   5.17560989e-02,   5.27831987e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   2.16999997e-05,   2.51160003e-03, ...,
            1.90403616e+00,   1.90177202e+00,   1.89801979e+00],
         [  0.00000000e+00,   2.08000001e-05,   2.45300005e-03, ...,
            1.89223838e+00,   1.89015996e+00,   1.88643348e+00],
         [  0.00000000e+00,   1.84000000e-05,   2.28350004e-03, ...,
            1.85722184e+00,   1.85548663e+00,   1.85194790e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   8.99999975e-07, ...,
            1.24098502e-01,   1.29805401e-01,   1.31329507e-01],
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            4.63171005e-02,   4.97104004e-02,   5.08899987e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   7.90000013e-06,   1.51320000e-03, ...,
            1.90134263e+00,   1.89938450e+00,   1.89588833e+00],
         [  0.00000000e+00,   7.60000012e-06,   1.47510006e-03, ...,
            1.88959861e+00,   1.88777244e+00,   1.88430202e+00],
         [  0.00000000e+00,   6.59999978e-06,   1.36540004e-03, ...,
            1.85458207e+00,   1.85309911e+00,   1.84981644e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            1.23128802e-01,   1.28910094e-01,   1.30504206e-01],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            4.56217006e-02,   4.90473993e-02,   5.02746999e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   9.13100026e-04, ...,
            1.89870286e+00,   1.89705122e+00,   1.89375687e+00],
         [  0.00000000e+00,   0.00000000e+00,   8.88400013e-04, ...,
            1.88690507e+00,   1.88543916e+00,   1.88217056e+00],
         [  0.00000000e+00,   0.00000000e+00,   8.17699998e-04, ...,
            1.85188854e+00,   1.85076582e+00,   1.84768498e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            1.22169897e-01,   1.28020197e-01,   1.29689902e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            4.49359007e-02,   4.83924001e-02,   4.96664010e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  3.57999998e-05,   1.92870002e-03,   1.89859997e-02, ...,
            1.06622577e+00,   1.05327833e+00,   1.05216610e+00],
         [  3.46000015e-05,   1.88690005e-03,   1.87187009e-02, ...,
            1.05970728e+00,   1.04687536e+00,   1.04582644e+00],
         [  3.11000003e-05,   1.76570006e-03,   1.79334003e-02, ...,
            1.04025972e+00,   1.02782941e+00,   1.02680743e+00],
         ..., 
         [  0.00000000e+00,   8.99999975e-07,   2.83999998e-05, ...,
            7.25433975e-02,   7.47457966e-02,   7.54147023e-02],
         [  0.00000000e+00,   4.00000005e-07,   1.21000003e-05, ...,
            2.81419996e-02,   2.96302997e-02,   3.01632006e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  5.29999988e-06,   6.79999997e-04,   1.11498004e-02, ...,
            1.06471741e+00,   1.05192173e+00,   1.05096376e+00],
         [  5.10000018e-06,   6.62799983e-04,   1.09719997e-02, ...,
            1.05819893e+00,   1.04557312e+00,   1.04462409e+00],
         [  4.50000016e-06,   6.13100012e-04,   1.04507999e-02, ...,
            1.03875124e+00,   1.02652717e+00,   1.02560508e+00],
         ..., 
         [  0.00000000e+00,   2.00000002e-07,   1.14000004e-05, ...,
            7.19724000e-02,   7.42248967e-02,   7.49391988e-02],
         [  0.00000000e+00,   1.00000001e-07,   5.10000018e-06, ...,
            2.77180001e-02,   2.92342007e-02,   2.97975000e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.41600006e-04,   6.58260006e-03, ...,
            1.06320894e+00,   1.05061948e+00,   1.04976141e+00],
         [  0.00000000e+00,   2.34599996e-04,   6.46529999e-03, ...,
            1.05669057e+00,   1.04421651e+00,   1.04342175e+00],
         [  0.00000000e+00,   2.14600004e-04,   6.12290017e-03, ...,
            1.03724289e+00,   1.02517056e+00,   1.02445734e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.90000002e-06, ...,
            7.14121014e-02,   7.37093985e-02,   7.44692013e-02],
         [  0.00000000e+00,   0.00000000e+00,   2.30000001e-06, ...,
            2.73004994e-02,   2.88428999e-02,   2.94362996e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   1.11999998e-05,   1.38300005e-03, ...,
            1.05862987e+00,   1.04660404e+00,   1.04615438e+00],
         [  0.00000000e+00,   1.06999996e-05,   1.35070004e-03, ...,
            1.05211151e+00,   1.04025543e+00,   1.03981471e+00],
         [  0.00000000e+00,   9.49999958e-06,   1.25750003e-03, ...,
            1.03271770e+00,   1.02126372e+00,   1.02085030e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.99999999e-07, ...,
            6.97475001e-02,   7.21845999e-02,   7.30756000e-02],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            2.60857008e-02,   2.77006999e-02,   2.83787996e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   3.99999999e-06,   8.26200005e-04, ...,
            1.05712152e+00,   1.04530180e+00,   1.04500663e+00],
         [  0.00000000e+00,   3.90000014e-06,   8.05400021e-04, ...,
            1.05060303e+00,   1.03895307e+00,   1.03861237e+00],
         [  0.00000000e+00,   3.39999997e-06,   7.45499972e-04, ...,
            1.03120923e+00,   1.01996148e+00,   1.01970267e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            6.92033991e-02,   7.16854036e-02,   7.26165026e-02],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            2.56929994e-02,   2.73305997e-02,   2.80344002e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   4.94399981e-04, ...,
            1.05561304e+00,   1.04399943e+00,   1.04380429e+00],
         [  0.00000000e+00,   0.00000000e+00,   4.81099996e-04, ...,
            1.04909468e+00,   1.03759658e+00,   1.03741002e+00],
         [  0.00000000e+00,   0.00000000e+00,   4.42799996e-04, ...,
            1.02975476e+00,   1.01865911e+00,   1.01850033e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            6.86592981e-02,   7.11916015e-02,   7.21628964e-02],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            2.53062006e-02,   2.69648992e-02,   2.76951008e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]]], dtype=float32))"""
str = repr(image)
#print(str)
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageLight.__str__() ###########

print("test ImageLight.__str__()")

str_ref = \
"""(array1d_ipix_pixel = array([ PixelWaterLight(lat = 68.76786, lon = -104.88453, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 0, rrs_type = 'A', array1d_iband_Rrs = [0.008642000146210194, 0.008084000088274479, 0.006331999786198139, 0.00469799991697073, 0.003625999903306365, 0.0020359999034553766], array1d_idepth_chl = [0.2825790047645569, 0.28540900349617004, 0.28870299458503723, 0.2924950122833252, 0.29681700468063354, 0.30170199275016785, 0.3071799874305725, 0.313277006149292, 0.3200179934501648, 0.32742199301719666, 0.33550500869750977, 0.3442760109901428, 0.353738009929657, 0.3638859987258911, 0.37470901012420654, 0.3861849904060364, 0.39828601479530334, 0.410971999168396, 0.42419400811195374, 0.43789398670196533, 0.45200398564338684, 0.4664449989795685, 0.481128990650177, 0.4959630072116852, 0.5108399987220764, 0.5256519913673401, 0.5402809977531433, 0.5546069741249084, 0.5685070157051086, 0.581853985786438, 0.5945240259170532, 0.6063950061798096, 0.6173480153083801, 0.627269983291626, 0.6360549926757812, 0.6436060070991516, 0.6498379707336426, 0.6546769738197327, 0.6580619812011719, 0.6599469780921936, 0.6603019833564758, 0.6591100096702576, 0.6563720107078552, 0.6521040201187134, 0.6463389992713928, 0.6391239762306213, 0.6305199861526489, 0.6206009984016418, 0.6094539761543274, 0.5971760153770447, 0.583873987197876, 0.5696600079536438, 0.5546550154685974, 0.5389800071716309, 0.5227599740028381, 0.5061209797859192, 0.48918700218200684, 0.47207701206207275, 0.45490700006484985, 0.4377889931201935, 0.4208250045776367, 0.40411099791526794, 0.38773301243782043, 0.3717679977416992, 0.3562859892845154, 0.3413420021533966, 0.32698699831962585, 0.31325799226760864, 0.3001840114593506, 0.28778600692749023, 0.27607399225234985, 0.26505300402641296, 0.254720002412796, 0.24506500363349915, 0.23607300221920013, 0.22772200405597687, 0.21999000012874603, 0.21284900605678558, 0.20626799762248993, 0.20021599531173706, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514]),
       PixelWaterLight(lat = 68.839119, lon = -104.9695, year = 2009, month = 8, day = 21, doy = 233, ibin45N = 2, rrs_type = 'A', array1d_iband_Rrs = [6.399999983841553e-05, 0.0007999999797903001, 0.0017180000431835651, 0.0033179998863488436, 0.0039900001138448715, 0.0011520000407472253], array1d_idepth_chl = [51.34635543823242, 54.6530876159668, 59.353553771972656, 64.84622192382812, 69.99886322021484, 73.42073059082031, 73.95088195800781, 71.13446807861328, 65.42147827148438, 57.970096588134766, 50.17124938964844, 43.15963363647461, 37.539974212646484, 33.391170501708984, 30.453460693359375, 28.350486755371094, 26.74401092529297, 25.396499633789062, 24.168567657470703, 22.989830017089844, 21.829195022583008, 20.674541473388672, 19.521663665771484, 18.369260787963867, 17.21697425842285, 16.06471061706543, 14.912453651428223, 13.760197639465332, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], array1d_itime_cf = [0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591, 0.5821999907493591], array1d_itime_o3 = [276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875, 276.79998779296875], array1d_itime_taucld = [5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514, 5.519999980926514])], dtype=object), array4d_itaucld_io3_ithetas_iwl_ed0minus = array([[[[  2.46599986e-04,   1.15595004e-02,   1.02635399e-01, ...,
            7.21043253e+00,   7.33221912e+00,   7.30728006e+00],
         [  2.38399996e-04,   1.13199996e-02,   1.01288103e-01, ...,
            7.18108988e+00,   7.30266428e+00,   7.27753830e+00],
         [  2.14900007e-04,   1.06236003e-02,   9.73128974e-02, ...,
            7.09181023e+00,   7.21219444e+00,   7.18813705e+00],
         ..., 
         [  0.00000000e+00,   5.50000004e-06,   1.57799994e-04, ...,
            6.59078896e-01,   6.84351087e-01,   6.95586503e-01],
         [  0.00000000e+00,   2.70000010e-06,   6.73000031e-05, ...,
            2.10019693e-01,   2.19942600e-01,   2.25101799e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.90999994e-05,   4.27869987e-03,   6.22630008e-02, ...,
            7.20080853e+00,   7.32366276e+00,   7.29871464e+00],
         [  3.75999989e-05,   4.17440012e-03,   6.13318011e-02, ...,
            7.17095280e+00,   7.29359102e+00,   7.26951933e+00],
         [  3.31000010e-05,   3.87299992e-03,   5.85886016e-02, ...,
            7.08167362e+00,   7.20366430e+00,   7.18011808e+00],
         ..., 
         [  0.00000000e+00,   1.30000001e-06,   6.55999975e-05, ...,
            6.53923213e-01,   6.79589927e-01,   6.91259086e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.95000009e-05, ...,
            2.06878603e-01,   2.17028797e-01,   2.22394004e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.58960000e-03,   3.78668010e-02, ...,
            7.19067144e+00,   7.31458950e+00,   7.29069567e+00],
         [  0.00000000e+00,   1.54500001e-03,   3.72284018e-02, ...,
            7.16135454e+00,   7.28449202e+00,   7.26152658e+00],
         [  0.00000000e+00,   1.41729997e-03,   3.53609994e-02, ...,
            7.07207537e+00,   7.19459105e+00,   7.17209911e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.90000007e-05, ...,
            6.48858905e-01,   6.74920619e-01,   6.86969817e-01],
         [  0.00000000e+00,   2.00000002e-07,   1.35000000e-05, ...,
            2.03784794e-01,   2.14146897e-01,   2.19713494e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   8.26999967e-05,   8.60089995e-03, ...,
            7.16133785e+00,   7.28788710e+00,   7.26666498e+00],
         [  0.00000000e+00,   7.95000014e-05,   8.40890035e-03, ...,
            7.13145638e+00,   7.25778913e+00,   7.23746967e+00],
         [  0.00000000e+00,   7.04999984e-05,   7.85250030e-03, ...,
            7.04220343e+00,   7.16788864e+00,   7.14806843e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-06, ...,
            6.33799374e-01,   6.61026120e-01,   6.74144387e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.50000005e-06, ...,
            1.94786206e-01,   2.05736294e-01,   2.11883903e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   3.09999996e-05,   5.25970012e-03, ...,
            7.15120125e+00,   7.27935648e+00,   7.25921869e+00],
         [  0.00000000e+00,   2.97000006e-05,   5.13269985e-03, ...,
            7.12185812e+00,   7.24925900e+00,   7.22947693e+00],
         [  0.00000000e+00,   2.59999997e-05,   4.76620020e-03, ...,
            7.03260517e+00,   7.15935850e+00,   7.14007568e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.50000005e-06, ...,
            6.28884971e-01,   6.56486571e-01,   6.69931114e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.91874802e-01,   2.03007996e-01,   2.09335804e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   3.21920007e-03, ...,
            7.14160299e+00,   7.27028370e+00,   7.25119972e+00],
         [  0.00000000e+00,   0.00000000e+00,   3.13579990e-03, ...,
            7.11172104e+00,   7.24018574e+00,   7.22145796e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.89530004e-03, ...,
            7.02246809e+00,   7.15025949e+00,   7.13205671e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            6.23970628e-01,   6.51930571e-01,   6.65755808e-01],
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            1.89008296e-01,   2.00320795e-01,   2.06820399e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  2.29800004e-04,   1.08067002e-02,   9.62229967e-02, ...,
            6.75160360e+00,   6.85922956e+00,   6.83517504e+00],
         [  2.22000002e-04,   1.05796000e-02,   9.49361995e-02, ...,
            6.72050095e+00,   6.82789373e+00,   6.80362940e+00],
         [  1.99999995e-04,   9.92020033e-03,   9.11398008e-02, ...,
            6.62713575e+00,   6.73329639e+00,   6.71003056e+00],
         ..., 
         [  0.00000000e+00,   5.10000018e-06,   1.47900006e-04, ...,
            5.48654497e-01,   5.72791815e-01,   5.80892026e-01],
         [  0.00000000e+00,   2.49999994e-06,   6.31000003e-05, ...,
            2.03703105e-01,   2.17257798e-01,   2.22078100e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.64000007e-05,   3.99489980e-03,   5.83126992e-02, ...,
            6.74228239e+00,   6.85094452e+00,   6.82739258e+00],
         [  3.49000002e-05,   3.89640010e-03,   5.74234016e-02, ...,
            6.71117973e+00,   6.81961107e+00,   6.79639339e+00],
         [  3.08000017e-05,   3.61169991e-03,   5.48100993e-02, ...,
            6.61781979e+00,   6.72501373e+00,   6.70279741e+00],
         ..., 
         [  0.00000000e+00,   1.20000004e-06,   6.14000019e-05, ...,
            5.44404387e-01,   5.68835974e-01,   5.77289820e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.75999992e-05, ...,
            2.00637802e-01,   2.14354798e-01,   2.19389200e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.48260000e-03,   3.54324989e-02, ...,
            6.73296356e+00,   6.84265900e+00,   6.82015610e+00],
         [  0.00000000e+00,   1.44060003e-03,   3.48262005e-02, ...,
            6.70186090e+00,   6.81132603e+00,   6.78861046e+00],
         [  0.00000000e+00,   1.32020004e-03,   3.30503993e-02, ...,
            6.60850143e+00,   6.71673107e+00,   6.69501734e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.71000008e-05, ...,
            5.40154219e-01,   5.64880073e-01,   5.73687613e-01],
         [  0.00000000e+00,   1.00000001e-07,   1.26000004e-05, ...,
            1.97615594e-01,   2.11489797e-01,   2.16733098e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   7.69000035e-05,   8.03130027e-03, ...,
            6.70554399e+00,   6.81780577e+00,   6.79735470e+00],
         [  0.00000000e+00,   7.39000025e-05,   7.84969982e-03, ...,
            6.67444372e+00,   6.78647232e+00,   6.76635838e+00],
         [  0.00000000e+00,   6.54000032e-05,   7.32359989e-03, ...,
            6.58109188e+00,   6.69188547e+00,   6.67276764e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.79999995e-06, ...,
            5.27613521e-01,   5.53283513e-01,   5.62990129e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            1.88834593e-01,   2.03133598e-01,   2.08956093e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.87999992e-05,   4.90880013e-03, ...,
            6.69622517e+00,   6.80952024e+00,   6.79012156e+00],
         [  0.00000000e+00,   2.75999992e-05,   4.78880014e-03, ...,
            6.66512489e+00,   6.77818966e+00,   6.75857830e+00],
         [  0.00000000e+00,   2.40999998e-05,   4.44239983e-03, ...,
            6.57177591e+00,   6.68360281e+00,   6.66553402e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            5.23497820e-01,   5.49435973e-01,   5.59442282e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.85995594e-01,   2.00420499e-01,   2.06431195e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   3.00280005e-03, ...,
            6.68690634e+00,   6.80123520e+00,   6.78233862e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.92390003e-03, ...,
            6.65580606e+00,   6.76990700e+00,   6.75134230e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.69729993e-03, ...,
            6.56245947e+00,   6.67532301e+00,   6.65775442e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            5.19419730e-01,   5.45642674e-01,   5.55949271e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.83199704e-01,   1.97745398e-01,   2.03933597e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  2.16100001e-04,   1.02049001e-02,   9.11696032e-02, ...,
            6.36338997e+00,   6.45821190e+00,   6.43479300e+00],
         [  2.08800004e-04,   9.98819992e-03,   8.99311975e-02, ...,
            6.33109903e+00,   6.42568445e+00,   6.40258265e+00],
         [  1.87900005e-04,   9.35900025e-03,   8.62796977e-02, ...,
            6.23368359e+00,   6.32755280e+00,   6.30540562e+00],
         ..., 
         [  0.00000000e+00,   4.80000017e-06,   1.39199998e-04, ...,
            4.59726900e-01,   4.81187105e-01,   4.86550689e-01],
         [  0.00000000e+00,   2.30000001e-06,   5.93000004e-05, ...,
            1.75960705e-01,   1.88354000e-01,   1.92037299e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  3.41999985e-05,   3.76689993e-03,   5.51913008e-02, ...,
            6.35471106e+00,   6.45056057e+00,   6.42764091e+00],
         [  3.27999987e-05,   3.67300003e-03,   5.43375015e-02, ...,
            6.32188129e+00,   6.41749001e+00,   6.39543056e+00],
         [  2.89000000e-05,   3.40240006e-03,   5.18306009e-02, ...,
            6.22500753e+00,   6.31990385e+00,   6.29825354e+00],
         ..., 
         [  0.00000000e+00,   1.09999996e-06,   5.75999984e-05, ...,
            4.56144512e-01,   4.77866292e-01,   4.83506590e-01],
         [  0.00000000e+00,   6.00000021e-07,   2.59000008e-05, ...,
            1.73315600e-01,   1.85841694e-01,   1.89714506e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.39620004e-03,   3.35027017e-02, ...,
            6.34603214e+00,   6.44236898e+00,   6.42048597e+00],
         [  0.00000000e+00,   1.35629997e-03,   3.29227000e-02, ...,
            6.31320477e+00,   6.40984154e+00,   6.38827848e+00],
         [  0.00000000e+00,   1.24200003e-03,   3.12226005e-02, ...,
            6.21633101e+00,   6.31171227e+00,   6.29110432e+00],
         ..., 
         [  0.00000000e+00,   3.00000011e-07,   2.54000006e-05, ...,
            4.52588886e-01,   4.74567086e-01,   4.80489790e-01],
         [  0.00000000e+00,   1.00000001e-07,   1.17999998e-05, ...,
            1.70713603e-01,   1.83361903e-01,   1.87424600e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   7.21999968e-05,   7.57599995e-03, ...,
            6.31945896e+00,   6.41887760e+00,   6.39957619e+00],
         [  0.00000000e+00,   6.92999965e-05,   7.40269991e-03, ...,
            6.28717041e+00,   6.38635206e+00,   6.36682224e+00],
         [  0.00000000e+00,   6.14000019e-05,   6.90140016e-03, ...,
            6.19030190e+00,   6.28876877e+00,   6.27019739e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.60000002e-06, ...,
            4.42094803e-01,   4.64805514e-01,   4.71537799e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.30000001e-06, ...,
            1.63139194e-01,   1.76128805e-01,   1.80707797e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.70000000e-05,   4.62719984e-03, ...,
            6.31078005e+00,   6.41122866e+00,   6.39242411e+00],
         [  0.00000000e+00,   2.58000000e-05,   4.51290002e-03, ...,
            6.27849150e+00,   6.37870359e+00,   6.36021662e+00],
         [  0.00000000e+00,   2.25999993e-05,   4.18339996e-03, ...,
            6.18216419e+00,   6.28057957e+00,   6.26304531e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.30000001e-06, ...,
            4.38652396e-01,   4.61598605e-01,   4.68592107e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.60688102e-01,   1.73779204e-01,   1.78527206e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   2.82890000e-03, ...,
            6.30210114e+00,   6.40357733e+00,   6.38526964e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.75389990e-03, ...,
            6.26981497e+00,   6.37050962e+00,   6.35306454e+00],
         [  0.00000000e+00,   0.00000000e+00,   2.53829989e-03, ...,
            6.17348766e+00,   6.27293110e+00,   6.25589561e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.00000021e-07, ...,
            4.35236990e-01,   4.58407998e-01,   4.65662688e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.58280000e-01,   1.71462297e-01,   1.76368400e-01],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       ..., 
       [[[  1.10300003e-04,   5.45680011e-03,   5.05620018e-02, ...,
            3.12169504e+00,   3.13715339e+00,   3.12665820e+00],
         [  1.06500003e-04,   5.33809979e-03,   4.98499013e-02, ...,
            3.10240889e+00,   3.11789036e+00,   3.10752988e+00],
         [  9.57000011e-05,   4.99449996e-03,   4.77560014e-02, ...,
            3.04498196e+00,   3.06064415e+00,   3.05063677e+00],
         ..., 
         [  0.00000000e+00,   2.49999994e-06,   7.56000009e-05, ...,
            2.08547607e-01,   2.18382597e-01,   2.20232397e-01],
         [  0.00000000e+00,   1.20000004e-06,   3.22999986e-05, ...,
            8.06510970e-02,   8.63090008e-02,   8.77989009e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  1.70000003e-05,   1.98030006e-03,   3.02383006e-02, ...,
            3.11738515e+00,   3.13324642e+00,   3.12316036e+00],
         [  1.63000004e-05,   1.92990003e-03,   2.97535006e-02, ...,
            3.09809923e+00,   3.11403775e+00,   3.10408688e+00],
         [  1.43999996e-05,   1.78499997e-03,   2.83387993e-02, ...,
            3.04067206e+00,   3.05679154e+00,   3.04713917e+00],
         ..., 
         [  0.00000000e+00,   6.00000021e-07,   3.08999988e-05, ...,
            2.06920594e-01,   2.16874093e-01,   2.18855098e-01],
         [  0.00000000e+00,   3.00000011e-07,   1.39000003e-05, ...,
            7.94389993e-02,   8.51586983e-02,   8.67331997e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   7.22899975e-04,   1.81559008e-02, ...,
            3.11302161e+00,   3.12939382e+00,   3.11971736e+00],
         [  0.00000000e+00,   7.01799989e-04,   1.78316999e-02, ...,
            3.09373569e+00,   3.11018515e+00,   3.10058904e+00],
         [  0.00000000e+00,   6.41699997e-04,   1.68855004e-02, ...,
            3.03636241e+00,   3.05293894e+00,   3.04369593e+00],
         ..., 
         [  0.00000000e+00,   1.00000001e-07,   1.35000000e-05, ...,
            2.05309898e-01,   2.15376407e-01,   2.17488796e-01],
         [  0.00000000e+00,   1.00000001e-07,   6.30000022e-06, ...,
            7.82483965e-02,   8.40191990e-02,   8.56892988e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   3.59000005e-05,   3.99329979e-03, ...,
            3.10003853e+00,   3.11783624e+00,   3.10927868e+00],
         [  0.00000000e+00,   3.45000008e-05,   3.89979989e-03, ...,
            3.08080649e+00,   3.09868169e+00,   3.09020519e+00],
         [  0.00000000e+00,   3.04999994e-05,   3.62979993e-03, ...,
            3.02354097e+00,   3.04148960e+00,   3.03336668e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.39999997e-06, ...,
            2.00547606e-01,   2.10948706e-01,   2.13433594e-01],
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            7.47736990e-02,   8.07038024e-02,   8.26179013e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   1.33000003e-05,   2.41929991e-03, ...,
            3.09572887e+00,   3.11398363e+00,   3.10578108e+00],
         [  0.00000000e+00,   1.27000003e-05,   2.35820003e-03, ...,
            3.07649684e+00,   3.09482908e+00,   3.08676195e+00],
         [  0.00000000e+00,   1.10999999e-05,   2.18249997e-03, ...,
            3.01923132e+00,   3.03769135e+00,   3.02997828e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   6.99999987e-07, ...,
            1.98985398e-01,   2.09489003e-01,   2.12100103e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            7.36531988e-02,   7.96239972e-02,   8.16176981e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   1.46770000e-03, ...,
            3.09141922e+00,   3.11018515e+00,   3.10233784e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.42800005e-03, ...,
            3.07218695e+00,   3.09097648e+00,   3.08326435e+00],
         [  0.00000000e+00,   0.00000000e+00,   1.31409999e-03, ...,
            3.01497531e+00,   3.03389287e+00,   3.02653503e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   3.00000011e-07, ...,
            1.97433904e-01,   2.08045706e-01,   2.10777506e-01],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            7.25487992e-02,   7.85657987e-02,   8.06339979e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  6.76999989e-05,   3.46309994e-03,   3.28803994e-02, ...,
            1.91745019e+00,   1.91365540e+00,   1.90873158e+00],
         [  6.54000032e-05,   3.38799995e-03,   3.24189998e-02, ...,
            1.90565240e+00,   1.90198910e+00,   1.89714527e+00],
         [  5.88000003e-05,   3.17010004e-03,   3.10558006e-02, ...,
            1.87052810e+00,   1.86720717e+00,   1.86255038e+00],
         ..., 
         [  0.00000000e+00,   1.60000002e-06,   4.91999999e-05, ...,
            1.29054695e-01,   1.34390503e-01,   1.35515794e-01],
         [  0.00000000e+00,   8.00000009e-07,   2.09999998e-05, ...,
            4.99616005e-02,   5.31668998e-02,   5.40850013e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  1.03000002e-05,   1.24230003e-03,   1.95126999e-02, ...,
            1.91475666e+00,   1.91126788e+00,   1.90660012e+00],
         [  9.89999990e-06,   1.21070002e-03,   1.92015003e-02, ...,
            1.90295875e+00,   1.89960158e+00,   1.89501393e+00],
         [  8.69999985e-06,   1.12000003e-03,   1.82886999e-02, ...,
            1.86783457e+00,   1.86487389e+00,   1.86041903e+00],
         ..., 
         [  0.00000000e+00,   4.00000005e-07,   1.99999995e-05, ...,
            1.28047302e-01,   1.33462593e-01,   1.34668693e-01],
         [  0.00000000e+00,   2.00000002e-07,   9.00000032e-06, ...,
            4.92100008e-02,   5.24565987e-02,   5.34303002e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   4.48600011e-04,   1.16341002e-02, ...,
            1.91206312e+00,   1.90888035e+00,   1.90446877e+00],
         [  0.00000000e+00,   4.35599999e-04,   1.14268996e-02, ...,
            1.90026522e+00,   1.89721406e+00,   1.89288247e+00],
         [  0.00000000e+00,   3.98400007e-04,   1.08212000e-02, ...,
            1.86519480e+00,   1.86254060e+00,   1.85828757e+00],
         ..., 
         [  0.00000000e+00,   1.00000001e-07,   8.69999985e-06, ...,
            1.27050698e-01,   1.32540196e-01,   1.33827105e-01],
         [  0.00000000e+00,   0.00000000e+00,   3.99999999e-06, ...,
            4.84704003e-02,   5.17560989e-02,   5.27831987e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   2.16999997e-05,   2.51160003e-03, ...,
            1.90403616e+00,   1.90177202e+00,   1.89801979e+00],
         [  0.00000000e+00,   2.08000001e-05,   2.45300005e-03, ...,
            1.89223838e+00,   1.89015996e+00,   1.88643348e+00],
         [  0.00000000e+00,   1.84000000e-05,   2.28350004e-03, ...,
            1.85722184e+00,   1.85548663e+00,   1.85194790e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   8.99999975e-07, ...,
            1.24098502e-01,   1.29805401e-01,   1.31329507e-01],
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            4.63171005e-02,   4.97104004e-02,   5.08899987e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   7.90000013e-06,   1.51320000e-03, ...,
            1.90134263e+00,   1.89938450e+00,   1.89588833e+00],
         [  0.00000000e+00,   7.60000012e-06,   1.47510006e-03, ...,
            1.88959861e+00,   1.88777244e+00,   1.88430202e+00],
         [  0.00000000e+00,   6.59999978e-06,   1.36540004e-03, ...,
            1.85458207e+00,   1.85309911e+00,   1.84981644e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.00000005e-07, ...,
            1.23128802e-01,   1.28910094e-01,   1.30504206e-01],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            4.56217006e-02,   4.90473993e-02,   5.02746999e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   9.13100026e-04, ...,
            1.89870286e+00,   1.89705122e+00,   1.89375687e+00],
         [  0.00000000e+00,   0.00000000e+00,   8.88400013e-04, ...,
            1.88690507e+00,   1.88543916e+00,   1.88217056e+00],
         [  0.00000000e+00,   0.00000000e+00,   8.17699998e-04, ...,
            1.85188854e+00,   1.85076582e+00,   1.84768498e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            1.22169897e-01,   1.28020197e-01,   1.29689902e-01],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            4.49359007e-02,   4.83924001e-02,   4.96664010e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],


       [[[  3.57999998e-05,   1.92870002e-03,   1.89859997e-02, ...,
            1.06622577e+00,   1.05327833e+00,   1.05216610e+00],
         [  3.46000015e-05,   1.88690005e-03,   1.87187009e-02, ...,
            1.05970728e+00,   1.04687536e+00,   1.04582644e+00],
         [  3.11000003e-05,   1.76570006e-03,   1.79334003e-02, ...,
            1.04025972e+00,   1.02782941e+00,   1.02680743e+00],
         ..., 
         [  0.00000000e+00,   8.99999975e-07,   2.83999998e-05, ...,
            7.25433975e-02,   7.47457966e-02,   7.54147023e-02],
         [  0.00000000e+00,   4.00000005e-07,   1.21000003e-05, ...,
            2.81419996e-02,   2.96302997e-02,   3.01632006e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  5.29999988e-06,   6.79999997e-04,   1.11498004e-02, ...,
            1.06471741e+00,   1.05192173e+00,   1.05096376e+00],
         [  5.10000018e-06,   6.62799983e-04,   1.09719997e-02, ...,
            1.05819893e+00,   1.04557312e+00,   1.04462409e+00],
         [  4.50000016e-06,   6.13100012e-04,   1.04507999e-02, ...,
            1.03875124e+00,   1.02652717e+00,   1.02560508e+00],
         ..., 
         [  0.00000000e+00,   2.00000002e-07,   1.14000004e-05, ...,
            7.19724000e-02,   7.42248967e-02,   7.49391988e-02],
         [  0.00000000e+00,   1.00000001e-07,   5.10000018e-06, ...,
            2.77180001e-02,   2.92342007e-02,   2.97975000e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   2.41600006e-04,   6.58260006e-03, ...,
            1.06320894e+00,   1.05061948e+00,   1.04976141e+00],
         [  0.00000000e+00,   2.34599996e-04,   6.46529999e-03, ...,
            1.05669057e+00,   1.04421651e+00,   1.04342175e+00],
         [  0.00000000e+00,   2.14600004e-04,   6.12290017e-03, ...,
            1.03724289e+00,   1.02517056e+00,   1.02445734e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.90000002e-06, ...,
            7.14121014e-02,   7.37093985e-02,   7.44692013e-02],
         [  0.00000000e+00,   0.00000000e+00,   2.30000001e-06, ...,
            2.73004994e-02,   2.88428999e-02,   2.94362996e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        ..., 
        [[  0.00000000e+00,   1.11999998e-05,   1.38300005e-03, ...,
            1.05862987e+00,   1.04660404e+00,   1.04615438e+00],
         [  0.00000000e+00,   1.06999996e-05,   1.35070004e-03, ...,
            1.05211151e+00,   1.04025543e+00,   1.03981471e+00],
         [  0.00000000e+00,   9.49999958e-06,   1.25750003e-03, ...,
            1.03271770e+00,   1.02126372e+00,   1.02085030e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   4.99999999e-07, ...,
            6.97475001e-02,   7.21845999e-02,   7.30756000e-02],
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            2.60857008e-02,   2.77006999e-02,   2.83787996e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   3.99999999e-06,   8.26200005e-04, ...,
            1.05712152e+00,   1.04530180e+00,   1.04500663e+00],
         [  0.00000000e+00,   3.90000014e-06,   8.05400021e-04, ...,
            1.05060303e+00,   1.03895307e+00,   1.03861237e+00],
         [  0.00000000e+00,   3.39999997e-06,   7.45499972e-04, ...,
            1.03120923e+00,   1.01996148e+00,   1.01970267e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   2.00000002e-07, ...,
            6.92033991e-02,   7.16854036e-02,   7.26165026e-02],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            2.56929994e-02,   2.73305997e-02,   2.80344002e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],

        [[  0.00000000e+00,   0.00000000e+00,   4.94399981e-04, ...,
            1.05561304e+00,   1.04399943e+00,   1.04380429e+00],
         [  0.00000000e+00,   0.00000000e+00,   4.81099996e-04, ...,
            1.04909468e+00,   1.03759658e+00,   1.03741002e+00],
         [  0.00000000e+00,   0.00000000e+00,   4.42799996e-04, ...,
            1.02975476e+00,   1.01865911e+00,   1.01850033e+00],
         ..., 
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            6.86592981e-02,   7.11916015e-02,   7.21628964e-02],
         [  0.00000000e+00,   0.00000000e+00,   1.00000001e-07, ...,
            2.53062006e-02,   2.69648992e-02,   2.76951008e-02],
         [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00, ...,
            0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]]], dtype=float32))"""
str = image.__str__()
if str == str_ref:
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########## test ImageWaterLightGeo.__init__(year, month, day, doy, grid_file,
########### rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus,
########### geospatial_file)

print("test ImageWaterLightGeo.__init__(year, month, day, doy, grid_file, \
rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus, geospatial_file)")

ipix_ref = 2
npix_ref = 3479813
# TEST
npix_ref = 3

image = image_with_primary_production_pixel.ImageWaterLightGeo(year,
                                                               month,
                                                               day,
                                                               doy,
                                                               grid_file,
                                                               rrs_type,
                                                               rrs_file,
                                                               chl_file,
                                                               atm_file,
                                                               lut_ed0minus,
                                                               geospatial_file)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(image.array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10],
                   ed0minus_ref,
                   rtol = 1e-03) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.depth == depth_ref \
   and p.province == province_ref \
   and np.allclose(p.array1d_idepth_pp,
                   array1d_idepth_pp_ref_matsuoka2011):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWaterLightGeo.__init__(year, month, day, doy, grid_file,
########### rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus,
########### geospatial_file)

print("test ImageWaterLightGeo.__init__(year, month, day, doy, grid_file, \
rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus, geospatial_file)")

ipix_ref = 2
npix_ref = 3479813
# TEST
npix_ref = 3

image = image_with_primary_production_pixel.ImageWaterLightGeo(year,
                                                               month,
                                                               day,
                                                               doy,
                                                               grid_file,
                                                               rrs_type,
                                                               rrs_file,
                                                               chl_file,
                                                               atm_file,
                                                               lut_ed0minus,
                                                               geospatial_file)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(image.array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10],
                   ed0minus_ref,
                   rtol = 1e-03) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.depth == depth_ref \
   and p.province == province_ref \
   and np.allclose(p.array1d_idepth_pp,
                   array1d_idepth_pp_ref_matsuoka2011):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWaterLightGeo.__init__(year, month, day, doy, grid_file,
########### rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus,
########### geospatial_file, array1d_ipix_ibin45N, chl = CHL_SURFACE)

print("test ImageWaterLightGeo.__init__(year, month, day, doy, grid_file, \
rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus, geospatial_file, \
array1d_ipix_ibin45N, chl = CHL_SURFACE)")

ipix_ref = 1
npix_ref = 3479813
# TEST
npix_ref = 2

# Array of dimension npix. The number of pixels in the resulting image.
# The first dimension is the indices of the pixel in the resulting image.
# The values are the indices (0-based) of the pixels in the ISIN grid above 45
# degrees North.
# Units: Unitless.                                                             
array1d_ipix_ibin45N = np.array([0, 2], dtype = np.int32)

# The value of the option chl to use the chlorophyll-a concentration.
# 0 for the chlorophyll-a concentration vertical profile in the water column.
# 1 for the surface chlorophyll-a concentration.                             
chl = image_with_primary_production_pixel.get_array1d_idepth_pp.CHL_SURFACE

image = image_with_primary_production_pixel.ImageWaterLightGeo(year,
                                                               month,
                                                               day,
                                                               doy,
                                                               grid_file,
                                                               rrs_type,
                                                               rrs_file,
                                                               chl_file,
                                                               atm_file,
                                                               lut_ed0minus,
                                                               geospatial_file,
                                                               array1d_ipix_ibin45N,
                                                               is_surface_chlorophyl= chl)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(image.array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10],
                   ed0minus_ref,
                   rtol = 1e-03) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.depth == depth_ref \
   and p.province == province_ref \
   and np.allclose(p.array1d_idepth_pp,
                   array1d_idepth_pp_ref_surface_matsuoka2011):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWaterLightGeo.__init__(year, month, day, doy, grid_file,
########### rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus,
########### geospatial_file, array1d_ipix_ibin45N)

print("test ImageWaterLightGeo.__init__(year, month, day, doy, grid_file, \
rrs_type, rrs_file, chl_file, atm_file, lut_ed0minus, geospatial_file, \
array1d_ipix_ibin45N)")

ipix_ref = 1
npix_ref = 3479813
# TEST
npix_ref = 2

# Array of dimension npix. The number of pixels in the resulting image.
# The first dimension is the indices of the pixel in the resulting image.
# The values are the indices (0-based) of the pixels in the ISIN grid above 45
# degrees North.
# Units: Unitless.                                                             
array1d_ipix_ibin45N = np.array([0, 2], dtype = np.int32)

image = image_with_primary_production_pixel.ImageWaterLightGeo(year,
                                                               month,
                                                               day,
                                                               doy,
                                                               grid_file,
                                                               rrs_type,
                                                               rrs_file,
                                                               chl_file,
                                                               atm_file,
                                                               lut_ed0minus,
                                                               geospatial_file,
                                                               array1d_ipix_ibin45N)

#print("image: {}".format(image.__dict__))
npix = image.array1d_ipix_pixel.size
#print("npix: {}".format(npix))
p = image.array1d_ipix_pixel[ipix_ref]
#print("p: {}".format(p.__dict__))

if npix == npix_ref \
   and p.lat == lat_ref \
   and p.lon == lon_ref \
   and p.year == year \
   and p.month == month \
   and p.day == day \
   and p.doy == doy \
   and p.rrs_type == rrs_type \
   and np.allclose(p.array1d_iband_Rrs,
                   array1d_iband_Rrs_ref) \
   and np.allclose(p.array1d_idepth_chl,
                   array1d_idepth_chl_ref) \
   and np.allclose(image.array4d_itaucld_io3_ithetas_iwl_ed0minus[3][2][1][10],
                   ed0minus_ref,
                   rtol = 1e-03) \
   and np.allclose(p.array1d_itime_cf,
                   array1d_itime_cf_ref) \
   and np.allclose(p.array1d_itime_o3,
                   array1d_itime_o3_ref) \
   and np.allclose(p.array1d_itime_taucld,
                   array1d_itime_taucld_ref) \
   and p.depth == depth_ref \
   and p.province == province_ref \
   and np.allclose(p.array1d_idepth_pp,
                   array1d_idepth_pp_ref_matsuoka2011):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWaterLightGeo.export(filename) ###########

print('test ImageWaterLightGeo.export(filename)')
ipix_ref = 1
ibin45N_ref = 2
filename = "../Outputs/foo_ImageWaterLightGeo.nc"
image.export_primary_production(filename)
array1d_ipix_lat \
= Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon \
= Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
array2d_ipix_iband_Rrs \
    = Netcdf_tools.get_array2d_i_j_val(filename, "Rrs")
array2d_ipix_idepth_chl \
    = Netcdf_tools.get_array2d_i_j_val(filename, "chlz")
array2d_ipix_itime_cf \
    = Netcdf_tools.get_array2d_i_j_val(filename, "CF")
array2d_ipix_itime_o3 \
    = Netcdf_tools.get_array2d_i_j_val(filename, "O3")
array2d_ipix_itime_taucld \
    = Netcdf_tools.get_array2d_i_j_val(filename, "TauCld")
array1d_ipix_depth \
    = Netcdf_tools.get_array1d_i_val(filename, "depth")
array1d_ipix_province \
    = Netcdf_tools.get_array1d_i_val(filename, "province")
array2d_ipix_idepth_pp \
    = Netcdf_tools.get_array2d_i_j_val(filename, "array1d_idepth_pp")
array1d_ipix_pp \
    = Netcdf_tools.get_array1d_i_val(filename, "pp")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
array1d_iband_Rrs_read = array2d_ipix_iband_Rrs[ipix_ref,]
array1d_idepth_chlz_read = array2d_ipix_idepth_chl[ipix_ref,]
array1d_itime_cf_read = array2d_ipix_itime_cf[ipix_ref,]
array1d_itime_o3_read = array2d_ipix_itime_o3[ipix_ref,]
array1d_itime_taucld_read = array2d_ipix_itime_taucld[ipix_ref,]
depth_read = array1d_ipix_depth[ipix_ref]
province_read = array1d_ipix_province[ipix_ref]
array1d_idepth_pp_read = array2d_ipix_idepth_pp[ipix_ref,]
pp_read = array1d_ipix_pp[ipix_ref,]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref \
   and np.allclose(array1d_iband_Rrs_read, array1d_iband_Rrs_ref) \
   and np.allclose(array1d_idepth_chlz_read, array1d_idepth_chl_ref) \
   and np.allclose(array1d_itime_cf_read, array1d_itime_cf_ref) \
   and np.allclose(array1d_itime_o3_read, array1d_itime_o3_ref) \
   and np.allclose(array1d_itime_taucld_read, array1d_itime_taucld_ref) \
   and np.isclose(depth_read, depth_ref) \
   and np.isclose(province_read, province_ref) \
   and np.allclose(array1d_idepth_pp_read, array1d_idepth_pp_ref_matsuoka2011) \
   and np.isclose(pp_read, pp_ref_matsuoka2011):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)

########### test ImageWaterLightGeo.export(filename, grid_file) ###########

print('test ImageWaterLightGeo.export(filename, grid_file)')
filename = "../Outputs/foo_ImageWaterLightGeo.nc"
ipix_ref = 2
ibin45N_ref = 2
image.export_primary_production(filename, grid_file)
array1d_ipix_lat \
= Netcdf_tools.get_array1d_i_val(filename, "lat")
array1d_ipix_lon \
= Netcdf_tools.get_array1d_i_val(filename, "lon")
array1d_ipix_ibin45N = \
Netcdf_tools.get_array1d_i_val(filename, "ibin45N")
array2d_ipix_iband_Rrs \
    = Netcdf_tools.get_array2d_i_j_val(filename, "Rrs")
array2d_ipix_idepth_chl \
    = Netcdf_tools.get_array2d_i_j_val(filename, "chlz")
array2d_ipix_itime_cf \
    = Netcdf_tools.get_array2d_i_j_val(filename, "CF")
array2d_ipix_itime_o3 \
    = Netcdf_tools.get_array2d_i_j_val(filename, "O3")
array2d_ipix_itime_taucld \
    = Netcdf_tools.get_array2d_i_j_val(filename, "TauCld")
array1d_ipix_depth \
    = Netcdf_tools.get_array1d_i_val(filename, "depth")
array1d_ipix_province \
    = Netcdf_tools.get_array1d_i_val(filename, "province")
array2d_ipix_idepth_pp \
    = Netcdf_tools.get_array2d_i_j_val(filename, "array1d_idepth_pp")
array1d_ipix_pp \
    = Netcdf_tools.get_array1d_i_val(filename, "pp")
lat_read = array1d_ipix_lat[ipix_ref]
lon_read = array1d_ipix_lon[ipix_ref]
ibin45N_read = array1d_ipix_ibin45N[ipix_ref]
array1d_iband_Rrs_read = array2d_ipix_iband_Rrs[ipix_ref,]
array1d_idepth_chlz_read = array2d_ipix_idepth_chl[ipix_ref,]
array1d_itime_cf_read = array2d_ipix_itime_cf[ipix_ref,]
array1d_itime_o3_read = array2d_ipix_itime_o3[ipix_ref,]
array1d_itime_taucld_read = array2d_ipix_itime_taucld[ipix_ref,]
depth_read = array1d_ipix_depth[ipix_ref]
province_read = array1d_ipix_province[ipix_ref]
array1d_idepth_pp_read = array2d_ipix_idepth_pp[ipix_ref,]
pp_read = array1d_ipix_pp[ipix_ref,]
if np.isclose(lat_read, lat_ref) \
   and np.isclose(lon_read, lon_ref) \
   and ibin45N_read == ibin45N_ref \
   and np.allclose(array1d_iband_Rrs_read, array1d_iband_Rrs_ref) \
   and np.allclose(array1d_idepth_chlz_read, array1d_idepth_chl_ref) \
   and np.allclose(array1d_itime_cf_read, array1d_itime_cf_ref) \
   and np.allclose(array1d_itime_o3_read, array1d_itime_o3_ref) \
   and np.allclose(array1d_itime_taucld_read, array1d_itime_taucld_ref) \
   and np.isclose(depth_read, depth_ref) \
   and np.isclose(province_read, province_ref) \
   and np.allclose(array1d_idepth_pp_read, array1d_idepth_pp_ref_matsuoka2011) \
   and np.isclose(pp_read, pp_ref_matsuoka2011):
    npass = pass_test(npass)
else:
    nfail = fail(nfail)
    
########### end ###########
print("Failed tests: {0}. Passed tests: {1}".format(nfail, npass))
