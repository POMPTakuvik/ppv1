#!/usr/bin/env python

"""Test get_array1d_idepth_pp.c:get_array1d_idepth_pp(...)

Test get_array1d_idepth_pp.c:get_array1d_idepth_pp(...) and 
get_array1d_idepth_pp_from_atm(...).

Usage:
python2 test_get_array1d_idepth_pp.py
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

import numpy

########### Importing modules ###########
import get_array1d_idepth_pp
# for ImageLight.get_array4d_itaucld_io3_ithetas_iwl_ed0minus(...).
from domain.image import image_with_primary_production_pixel

########### Constants ###########
NBDEPTHS = 101

########### functions ###########

def test_get_array1d_idepth_pp(
        array2d_itime_ivis_Ed0minus,
        lat,
        lon,
        year,
        month,
        day,
        doy,
        depth,
        rrs_type,
        array1d_iband_Rrs,
        array1d_idepth_chl,
        array1d_idepth_pp,
        chl,
        array1d_idepth_pp_ref_l):
    """
    test get_array1d_idepth_pp.get_array1d_idepth_pp(...)

    Args:
        array2d_itime_ivis_Ed0minus(numpy.float[9][61]):
            Array of dimensions 9 * 61.					    
            The first dimension is the hours from 0 to 24 by step of 3 h.
            The second dimension is the wavelenght from 400 nm to 700 nm by 
            step of 5 nm.
            The values are the downward irradiances just below the surface water
            (Ed0minus) for one pixel.
            The units are umol photons*m^-2*s^-1*nm^-1.
        lat(numpy.float32): Latitude.
            The units are degrees North.
        lon(numpy.float32): Longitude.
            From -180 to 180.
            The units are degrees East.
        year(numpy.int32): Year.
        month(numpy.int32): Month.
        day(numpy.int32): Day of month.
        doy(numpy.int32): Day of year.
        depth(numpy.float32): Depth (positive downward)
        rrs_type(char): S for SeaWiFS and A for MODIS-AQUA.
        array1d_iband_Rrs(numpy.float32[6]):
            Array of dimension NBANDS = 6.                                  
            The first dimension are the wavelengths of the bands of the     
            satellite.                                                      
            The values are the remote-sensing reflectances.                 
            The units are sr^-1.                                            
        array1d_idepth_chl(numpy.float32[101]):
            Array of dimension NBDEPTHS = 101.			     
            The first dimension is the index of the geometric depths.    
            The geometric depths are from 0 to 100 by step 1. Units: m.  
            The values are the chlorophyll-a concentration.	             
            The units are mg Chl-a m^-3.                                 
        array1d_idepth_pp(numpy.float32[100]):
            Array of dimension NBDEPTHS - 1 = 100.                           
            The first dimension is the index of the geometric depths.        
            The geometric depths are from 0 to 100 by step 1. Units: m.      
            The values are the primary productivities.                       
            Units: mgC.m^-3.d^-1.                                            
        chl(numpy.int32):
            The value of the option chl to use the chlorophyll-a concentration. 
            0 for the chlorophyll-a concentration vertical profile in the 
            water column.
            1 for the surface chlorophyll-a concentration.                      
        array1d_idepth_pp_ref_l(numpy.float32[100]):
            Array of dimension NBDEPTHS - 1 = 100.                           
            The first dimension is the index of the geometric depths.        
            The geometric depths are from 0 to 100 by step 1. Units: m.      
            The values are the expected primary productivities.
            Units: mgC.m^-3.d^-1.                                            
    """

    array1d_idepth_pp_ref = numpy.array(object = array1d_idepth_pp_ref_l,
                                        dtype = numpy.float32)

    ########### Compute primary productivity. ###########

    get_array1d_idepth_pp.get_array1d_idepth_pp(
        array2d_itime_ivis_Ed0minus,
        lat,
        lon,
        year,
        month,
        day,
        doy,
        depth,
        rrs_type,
        array1d_iband_Rrs,
        array1d_idepth_chl,
        array1d_idepth_pp,
        chl)
 
    ########### Test ###########

    if numpy.allclose(a = array1d_idepth_pp,
                      b = array1d_idepth_pp_ref):
        print("PASS\n")
    else:
        print("FAIL\n")

def test_get_array1d_idepth_pp_from_atm(
        lat,
        lon,
        year,
        month,
        day,
        doy,
        depth,
        rrs_type,
        array1d_iband_Rrs,
        array1d_idepth_chl,
        array1d_itime_cf,
        array1d_itime_o3,
        array1d_itime_taucld,
        array4d_itaucld_io3_ithetas_iwl_ed0minus,
        array1d_idepth_pp,
        chl,
        array1d_idepth_pp_ref_l):
    """
    test get_array1d_idepth_pp.get_array1d_idepth_pp_from_atm(...)

    Args:
        lat(numpy.float32): Latitude.
            The units are degrees North.
        lon(numpy.float32): Longitude.
            From -180 to 180.
            The units are degrees East.
        year(numpy.int32): Year.
        month(numpy.int32): Month.
        day(numpy.int32): Day of month.
        doy(numpy.int32): Day of year.
        depth(numpy.float32): Depth (positive downward)
        rrs_type(char): S for SeaWiFS and A for MODIS-AQUA.
        array1d_iband_Rrs(numpy.float32[6]):
            Array of dimension NBANDS = 6.                                  
            The first dimension are the wavelengths of the bands of the     
            satellite.                                                      
            The values are the remote-sensing reflectances.                 
            The units are sr^-1.                                            
        array1d_idepth_chl(numpy.float32[101]):
            Array of dimension NBDEPTHS = 101.			     
            The first dimension is the index of the geometric depths.    
            The geometric depths are from 0 to 100 by step 1. Units: m.  
            The values are the chlorophyll-a concentration.	             
            The units are mg Chl-a m^-3.                                 
        array1d_itime_cf(numpy.float32[9]):
            Array of dimensions NTIMES.
            The first dimension is the hours from 0 to 24 by step of 3 h.
            The values are the cloud fraction from 0 to 1.
            Units: unitless.
        array1d_itime_o3(numpy.float32[9]):
            Array of dimensions NTIMES.				     	    
            The first dimension is the hours from 0 to 24 by step of 3 h.   
            The values are the total ozone column at 00h UTC.		    
            Units: Dobson units.                                            
        array1d_itime_taucld(numpy.float32[9]):
            Array of dimensions NTIMES.					 	
            The first dimension is the hours from 0 to 24 by step of 3 h.	
            The values are the cloud optical thickness at 00h UTC.   		
            The values are unitless.                                            
        array4d_itaucld_io3_ithetas_iwl_ed0minus(numpy.float32[8][8][19][83]:
            Array of 4 dimensions : 					       
            NTAUCLD=8 * NO3=8 * NTHETAS=19 * NBWL=83.			       
            The first dimension is the mean cloud optical thickness.	       
            The second dimension is the total ozone column.		       
            The third dimension is the solar zenith angle.		       
            The fourth dimension is the wavelengths from 290 to 700 by step 5  
            nm.                                                                
            The values are the downward irradiance just below the water surface
            from the lookup table.					       
            The units are umol photons*m^-2*s^-1*nm^-1.                        
        array1d_idepth_pp(numpy.float32[100]):
            Array of dimension NBDEPTHS - 1 = 100.                           
            The first dimension is the index of the geometric depths.        
            The geometric depths are from 0 to 100 by step 1. Units: m.      
            The values are the primary productivities.                       
            Units: mgC.m^-3.d^-1.                                            
        chl(numpy.int32):
            The value of the option chl to use the chlorophyll-a concentration. 
            0 for the chlorophyll-a concentration vertical profile in the 
            water column.
            1 for the surface chlorophyll-a concentration.                      
        array1d_idepth_pp_ref_l(numpy.float32[100]):
            Array of dimension NBDEPTHS - 1 = 100.                           
            The first dimension is the index of the geometric depths.        
            The geometric depths are from 0 to 100 by step 1. Units: m.      
            The values are the expected primary productivities.
            Units: mgC.m^-3.d^-1.                                            
    """

    array1d_idepth_pp_ref = numpy.array(object = array1d_idepth_pp_ref_l,
                                        dtype = numpy.float32)

    ########### Compute primary productivity. ###########

    get_array1d_idepth_pp.get_array1d_idepth_pp_from_atm(
        lat,
        lon,
        year,
        month,
        day,
        doy,
        depth,
        rrs_type,
        array1d_iband_Rrs,
        array1d_idepth_chl,
        array1d_itime_cf,
        array1d_itime_o3,
        array1d_itime_taucld,
        array4d_itaucld_io3_ithetas_iwl_ed0minus,
        array1d_idepth_pp,
        chl)

    ########### Test ###########

    if numpy.allclose(a = array1d_idepth_pp,
                      b = array1d_idepth_pp_ref):
        print("PASS\n")
    else:
        print("FAIL\n")

########### main ###########

#  /////////////////////////////////////////////////////////////////////////////
#  /////////// test for get_array1d_idepth_pp with pixel at row 2    ///////////
#  /////////// of the prototype for Mathieu in                       ///////////
#  /////////// /Volumes/Disk6TB/Takuvik/Teledetection/Couleur/Other/ ///////////
#  /////////// Mathieu/Malina/Fig8/IN/IN20140815/                    ///////////
#  /////////// PPARR5_Mathieu_BG_RRS_Profile_1_1000.txt              ///////////
#  /////////////////////////////////////////////////////////////////////////////

print("Test of get_array1d_idepth_pp")
  
########### Declaration of inputs ###########

# Array of dimensions 9 * 61.					             
# The first dimension is the hours from 0 to 24 by step of 3 h.	             
# The second dimension is the wavelenght from 400 nm to 700 nm by step of 5  
# nm.								             
# The values are the downward irradiances just below the surface water       
# (Ed0minus) for one pixel.						       
# The units are umol photons*m^-2*s^-1*nm^-1.                              
array2d_itime_ivis_Ed0minus = numpy.array(
    [
        [1.759203716,1.725188282,1.685903252,2.044845854,1.685061817,1.962247802,1.344674087,2.019756521,2.215382246,2.467011613,2.643739011,2.671308186,2.702406782,2.748445381,2.852862125,3.000272902,2.967503347,2.955102347,3.122189635,3.148630843,2.906831189,3.024799846,3.045508205,2.949611165,2.969618299,3.118385141,3.049601511,3.110845621,3.154810038,3.234265488,3.174966213,3.302136091,3.094711754,3.274718617,3.120023212,3.151901953,3.294664562,3.349053055,2.862327837,3.057414035,3.278147017,3.427146986,3.308324376,3.339655836,3.394040234,3.230107814,3.197759141,3.353710003,3.341428349,3.415130149,3.136836921,3.24782228,3.432887908,3.490297164,3.53879719,3.506574595,3.513373321,3.531725667,3.030819883,3.060720262,3.135589093],
        [0.696570167,0.682739698,0.666915551,0.808487573,0.66609804,0.77548348,0.53115729,0.797407231,0.874184325,0.972697861,1.042612426,1.05344867,1.06420021,1.082005404,1.122154351,1.172289446,1.157891797,1.157496812,1.224426411,1.233325002,1.133932214,1.174860964,1.183072209,1.145212405,1.149490508,1.201945977,1.16940023,1.190053444,1.206031623,1.234119914,1.208179135,1.251338806,1.166849533,1.225166357,1.145262362,1.149402495,1.212087685,1.24978214,1.033574645,1.112053786,1.217725315,1.281205205,1.241235254,1.257177497,1.279437052,1.215269436,1.190019869,1.266302835,1.280499806,1.31321872,1.203613547,1.243449056,1.335514814,1.368367415,1.39518875,1.387615055,1.392492542,1.400957349,1.138664907,1.164111882,1.201399011],
        [0.07512039,0.073520563,0.071706056,0.086699097,0.071389291,0.082943877,0.05658151,0.084524828,0.092201129,0.102081499,0.1090699,0.109619909,0.109142919,0.110456048,0.114380385,0.117086153,0.112762911,0.111147331,0.117721233,0.116732388,0.102905256,0.102091599,0.10219102,0.09778043,0.095000162,0.095632421,0.088900227,0.087561504,0.086684912,0.086350592,0.081729637,0.081146584,0.072270784,0.072398641,0.065714618,0.063257637,0.066646627,0.070860746,0.060785447,0.06467445,0.066117188,0.067626913,0.067034647,0.070019465,0.072996915,0.070373963,0.070414615,0.077836878,0.08326745,0.089839617,0.085349086,0.09043083,0.099278777,0.103402306,0.108550193,0.110917133,0.113521205,0.116351095,0.09185957,0.100297309,0.104810026],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0.152120061,0.14885851,0.145165306,0.175578054,0.144479818,0.16787223,0.114627512,0.171476158,0.187311715,0.207644632,0.222021026,0.22353045,0.223910281,0.226886845,0.234763997,0.241841811,0.235717218,0.234427866,0.24801366,0.24763955,0.222719033,0.225571013,0.226329954,0.217676135,0.214777312,0.220058361,0.208982292,0.209164417,0.209573785,0.211528702,0.203533968,0.206267431,0.187776392,0.191963251,0.175339043,0.171318833,0.181142749,0.191677195,0.158793157,0.170428473,0.183004382,0.190450967,0.186659513,0.191800737,0.197097049,0.187678911,0.183704887,0.200908658,0.21015025,0.221064199,0.205425234,0.214047373,0.234001318,0.242090479,0.250678525,0.252529952,0.255380396,0.25880953,0.1972514,0.211491069,0.220430429],
        [0.893339542,0.876045006,0.856150849,1.03842996,0.855896765,0.99688584,0.683156766,1.026140593,1.125531977,1.253110164,1.343591927,1.358083754,1.373078691,1.396661618,1.449281961,1.51744578,1.500147168,1.498716028,1.585302183,1.597991882,1.471746625,1.527590576,1.538694069,1.490193078,1.49775482,1.56878316,1.529369595,1.558149115,1.580014685,1.618332826,1.586269897,1.645631522,1.53744582,1.618630152,1.52123372,1.53058628,1.61065571,1.653792371,1.379154605,1.481333541,1.614358545,1.696441388,1.641865962,1.661337486,1.690131635,1.60644151,1.577780056,1.671917161,1.683289172,1.724061952,1.580806913,1.633964178,1.74743701,1.786809505,1.818882792,1.807069142,1.81267805,1.823246093,1.504914039,1.532412026,1.578235493],
        [1.948078665,1.909984108,1.866060501,2.262870353,1.864286541,2.170449271,1.487044894,2.23315901,2.448984224,2.726726882,2.921321391,2.951119812,2.985167083,3.035470952,3.150457737,3.314714799,3.278104199,3.262383911,3.445842251,3.4747049,3.208295096,3.339019062,3.361261055,3.255004073,3.277307045,3.44210824,3.367026757,3.434699662,3.482817882,3.570478871,3.505221857,3.646376108,3.418281973,3.619072774,3.454585159,3.491062619,3.645368136,3.700644618,3.174482248,3.387896073,3.623031962,3.784434091,3.651693472,3.685075944,3.744509872,3.564108697,3.532376325,3.699384675,3.680697823,3.761135809,3.455665279,3.578872767,3.776365924,3.836286801,3.887459244,3.850674055,3.857453907,3.877276215,3.345568659,3.375026942,3.454999612],
        [2.365827284,2.318212182,2.263561878,2.743365842,2.258838361,2.628293703,1.799798694,2.70148016,2.961154953,3.295642571,3.528801773,3.562915205,3.602912336,3.662041147,3.799658394,4.000597445,3.955069947,3.931270017,4.149827423,4.18348831,3.863217052,4.021376439,4.04656118,3.917423873,3.944453176,4.143772446,4.05488601,4.1361585,4.192841947,4.297975318,4.219509368,4.390805184,4.11814971,4.363837877,4.179892353,4.226149014,4.404260463,4.460283259,3.852762912,4.105024295,4.368061499,4.554633723,4.392119335,4.429574342,4.499399523,4.283467995,4.254237599,4.443748016,4.410121139,4.505108132,4.141550083,4.291343858,4.513655791,4.578217603,4.634603007,4.587617525,4.594256432,4.617034367,4.024567146,4.05233581,4.14206576],
        [1.764808139,1.730674175,1.691253899,2.051324827,1.690388251,1.968436035,1.348909011,2.02610492,2.22233564,2.474740123,2.652003375,2.679641511,2.7108318,2.756997678,2.861732971,3.009646276,2.976762307,2.964267308,3.131847087,3.158357949,2.915830699,3.034177593,3.054937457,2.958734757,2.978809547,3.1280565,3.059086412,3.120521486,3.164611708,3.244317249,3.184837161,3.312426924,3.104381411,3.285009115,3.130014912,3.162030063,3.305145928,3.359566912,2.871645014,3.067280655,3.28846261,3.437832978,3.318603511,3.349995246,3.404533383,3.240107621,3.2077685,3.36406397,3.35159039,3.425495466,3.146388181,3.257734649,3.443181156,3.500671811,3.549253498,3.516896701,3.523696554,3.542090033,3.040239387,3.070133979,3.145155528],
    ],
    dtype = numpy.float32
    )
# Latitude.			 
# The units are degrees North.
lat = 68.76786
# Longitude.			
# From -180 to 180.		
# The units are degrees East.
lon = -104.884529
year = 2009
month = 8
# Day of month.
day = 21
# Day of year.
doy = 233
# Bathymetry.     
# The units are m.
depth = 79.900002
# S for SeaWiFS and A for MODIS-AQUA.
rrs_type = 'A'
# Array of dimension NBANDS = 6.					       
# The first dimension are the wavelengths of the bands of the satellite.    
# The values are the remote-sensing reflectances.			       
# The units are sr^-1.
array1d_iband_Rrs = numpy.array(
    [0.008642, 0.008084, 0.006332, 0.004698, 0.003626, 0.002036],
    dtype = numpy.float32)
# Array of dimension NBDEPTHS = 101.				  
# The first dimension is the index of the geometric depths.	  
# The geometric depths are from 0 to 100 by step 1. Units: m.  
# The values are the chlorophyll-a concentration.		  
# The units are mg Chl-a m^-3.
array1d_idepth_chl = numpy.array(
    [0.282579,0.285409,0.288703,0.292495,0.296817,0.301702,0.307180,0.313277,0.320018,0.327422,0.335505,0.344276,0.353738,0.363886,0.374709,0.386185,0.398286,0.410972,0.424194,0.437894,0.452004,0.466445,0.481129,0.495963,0.510840,0.525652,0.540281,0.554607,0.568507,0.581854,0.594524,0.606395,0.617348,0.627270,0.636055,0.643606,0.649838,0.654677,0.658062,0.659947,0.660302,0.659110,0.656372,0.652104,0.646339,0.639124,0.630520,0.620601,0.609454,0.597176,0.583874,0.569660,0.554655,0.538980,0.522760,0.506121,0.489187,0.472077,0.454907,0.437789,0.420825,0.404111,0.387733,0.371768,0.356286,0.341342,0.326987,0.313258,0.300184,0.287786,0.276074,0.265053,0.254720,0.245065,0.236073,0.227722,0.219990,0.212849,0.206268,0.200216,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
    dtype = numpy.float32)

########### Future output ###########
# Array of dimension NBDEPTHS - 1 = 100.
# The first dimension is the index of the geometric depths.
# The geometric depths are from 0 to 100 by step 1. Units: m.
# The values are the primary productivities.
# Units: mgC.m^-2.d^-1.
array1d_idepth_pp = numpy.zeros(shape = NBDEPTHS - 1,
                                dtype = numpy.float32)

########### chl = surface ###########

print("Test with chl = surface")

# The value of the option chl to use the surface chlorophyll-a concentration.
chl = get_array1d_idepth_pp.CHL_SURFACE
# Array of dimension NBDEPTHS - 1 = 100.
# The first dimension is the index of the geometric depths.
# The geometric depths are from 0 to 100 by step 1. Units: m.
# The values are the primary productivities.
# Units: mgC.m^-2.d^-1.
# TODO : Modify.
array1d_idepth_pp_ref_l_matsuoka2011 = [9.120220,8.932844,8.731698,8.514927,8.280903,8.028418,7.756937,7.466886,7.159950,6.839290,6.509616,6.176983,5.848259,5.530313,5.229079,4.948763,4.691380,4.456733,4.242784,4.046261,3.863321,3.690129,3.523285,3.360072,3.198549,3.037541,2.876546,2.715611,2.555200,2.396057,2.239088,2.085261,1.935529,1.790770,1.651747,1.519081,1.393247,1.274570,1.163235,1.059296,0.962700,0.873297,0.790861,0.715110,0.645717,0.582327,0.524566,0.472054,0.424412,0.381267,0.342259,0.307042,0.275291,0.246697,0.220973,0.197852,0.103890,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000]

test_get_array1d_idepth_pp(
    array2d_itime_ivis_Ed0minus,
    lat,
    lon,
    year,
    month,
    day,
    doy,
    depth,
    rrs_type,
    array1d_iband_Rrs,
    array1d_idepth_chl,
    array1d_idepth_pp,
    chl,
    array1d_idepth_pp_ref_l_matsuoka2011)

########### chl = column ###########

print("Test with chl = column")

# The value of the option chl to use the chlorophyll-a concentration
# vertical profile in the water column.
chl = get_array1d_idepth_pp.CHL_COLUMN
# Array of dimension NBDEPTHS - 1 = 100.
# The first dimension is the index of the geometric depths.
# The geometric depths are from 0 to 100 by step 1. Units: m.
# The values are the primary productivities.
# Units: mgC.m^-2.d^-1.
# TODO : Modify.
array1d_idepth_pp_ref_l_matsuoka2011 = [9.165866,9.075148,8.981170,8.881427,8.773249,8.653952,8.521031,8.372564,8.207620,8.026717,7.832196,7.628336,7.421108,7.217455,7.024190,6.846815,6.688540,6.549751,6.428077,6.318885,6.216055,6.112847,6.002728,5.879945,5.739959,5.579689,5.397561,5.193474,4.968619,4.725286,4.466611,4.196304,3.918381,3.636929,3.355901,3.078957,2.809335,2.549778,2.302494,2.069162,1.850944,1.648532,1.462206,1.291892,1.137228,0.997624,0.872317,0.760429,0.661005,0.573055,0.495580,0.427599,0.368165,0.185582,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000]

test_get_array1d_idepth_pp(
    array2d_itime_ivis_Ed0minus,
    lat,
    lon,
    year,
    month,
    day,
    doy,
    depth,
    rrs_type,
    array1d_iband_Rrs,
    array1d_idepth_chl,
    array1d_idepth_pp,
    chl,
    array1d_idepth_pp_ref_l_matsuoka2011)

#  /////////////////////////////////////////////////////////////////////////////
#  /////////// test of get_array1d_idepth_pp_from_atm with pixel     ///////////
#  /////////// at row 2 of the prototype for Mathieu in              ///////////
#  /////////// /Volumes/Disk6TB/Takuvik/Teledetection/Couleur/Other/ ///////////
#  /////////// Mathieu/Malina/Fig8/IN/IN20140815/                    ///////////
#  /////////// PPARR5_Mathieu_BG_RRS_Profile_1_1000.txt              ///////////
#  /////////// and the atmospheric products at corresponding pixel   ///////////
#  /////////// 2672663 (0-based) of AM2006225_PP.nc                  ///////////
#  /////////// (version 34.0.0).                                     ///////////
#  /////////////////////////////////////////////////////////////////////////////

print("Test of get_array1d_idepth_pp_from_atm")
  
########### Declaration of inputs ###########

# Array of dimensions NTIMES.					      
# The first dimension is the hours from 0 to 24 by step of 3 h.	      
# The values are the cloud fraction from 0 to 1.			      
# Units: unitless.
array1d_itime_cf = numpy.array(
    [0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822],
    dtype = numpy.float32
)

# Array of dimensions NTIMES.				       
# The first dimension is the hours from 0 to 24 by step of 3 h.   
# The values are the total ozone column at 00h UTC.	       
# Units: Dobson units.
array1d_itime_o3 = numpy.array(
    [276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8],
     dtype = numpy.float32
)

# Array of dimensions NTIMES.					   
# The first dimension is the hours from 0 to 24 by step of 3 h.	   
# The values are the cloud optical thickness at 00h UTC.   	   
# The values are unitless.
array1d_itime_taucld = numpy.array(
    [5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52],
    dtype = numpy.float32
)

lut_ed0minus = "../Inputs/Ed0moins_LUT.dat"

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
    = image_with_primary_production_pixel.ImageLight.get_array4d_itaucld_io3_ithetas_iwl_ed0minus(lut_ed0minus)

########### Future output ###########
# Array of dimension NBDEPTHS - 1 = 100.
# The first dimension is the index of the geometric depths.
# The geometric depths are from 0 to 100 by step 1. Units: m.
# The values are the primary productivities.
# Units: mgC.m^-2.d^-1.
array1d_idepth_pp = numpy.zeros(shape = NBDEPTHS - 1,
                                dtype = numpy.float32)

########### chl = surface ###########

print("Test with chl = surface")

# The value of the option chl to use the surface chlorophyll-a concentration.
chl = get_array1d_idepth_pp.CHL_SURFACE

# Array of dimension NBDEPTHS - 1 = 100.
# The first dimension is the index of the geometric depths.
# The geometric depths are from 0 to 100 by step 1. Units: m.
# The values are the expected primary productivities.
# Units: mgC.m^-2.d^-1.
# TODO : Modify.
array1d_idepth_pp_ref_l_matsuoka2011 = [7.276281,7.100162,6.906811,6.695390,6.466120,6.220589,5.961941,5.694836,5.425088,5.158994,4.902441,4.660063,4.434651,4.226973,4.035987,3.859332,3.693932,3.536549,3.384216,3.234498,3.085626,2.936507,2.786663,2.636134,2.485361,2.335063,2.186132,2.039538,1.896248,1.757170,1.623110,1.494745,1.372607,1.257085,1.148426,1.046745,0.952045,0.864230,0.783121,0.708477,0.640008,0.577388,0.520272,0.468301,0.421114,0.378354,0.339673,0.304737,0.273227,0.244842,0.219301,0.196341,0.175719,0.157211,0.140612,0.125734,0.088520,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000]

test_get_array1d_idepth_pp_from_atm(
    lat,
    lon,
    year,
    month,
    day,
    doy,
    depth,
    rrs_type,
    array1d_iband_Rrs,
    array1d_idepth_chl,
    array1d_itime_cf,
    array1d_itime_o3,
    array1d_itime_taucld,
    array4d_itaucld_io3_ithetas_iwl_ed0minus,
    array1d_idepth_pp,
    chl,
    array1d_idepth_pp_ref_l_matsuoka2011)

########### chl = column ###########

print("Test with chl = column")

# The value of the option chl to use the chlorophyll-a concentration
# vertical profile in the water column.
chl = get_array1d_idepth_pp.CHL_COLUMN

# Array of dimension NBDEPTHS - 1 = 100.
# The first dimension is the index of the geometric depths.
# The geometric depths are from 0 to 100 by step 1. Units: m.
# The values are the expected primary productivities.
# Units: mgC.m^-2.d^-1.
# TODO : Modify.
array1d_idepth_pp_ref_l_matsuoka2011 = [7.312701,7.213396,7.104436,6.984052,6.851217,6.706019,6.549954,6.386131,6.219142,6.054544,5.898037,5.754498,5.627139,5.517017,5.422954,5.341844,5.269215,5.199850,5.128415,5.049937,4.960158,4.855750,4.734463,4.595119,4.437569,4.262619,4.071864,3.867557,3.652403,3.429402,3.201684,2.972346,2.744327,2.520310,2.302652,2.093337,1.893964,1.705737,1.529494,1.365736,1.214662,1.076212,0.950117,0.835938,0.733108,0.640966,0.558790,0.485827,0.421314,0.364493,0.314631,0.271026,0.233016,0.157494,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000]

test_get_array1d_idepth_pp_from_atm(
    lat,
    lon,
    year,
    month,
    day,
    doy,
    depth,
    rrs_type,
    array1d_iband_Rrs,
    array1d_idepth_chl,
    array1d_itime_cf,
    array1d_itime_o3,
    array1d_itime_taucld,
    array4d_itaucld_io3_ithetas_iwl_ed0minus,
    array1d_idepth_pp,
    chl,
    array1d_idepth_pp_ref_l_matsuoka2011)

