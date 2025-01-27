#!/usr/bin/env python2

"""Generate _PPz.nc files.

Usage:
    python2 run_ppz.py
"""

#__author__ = "Maxime Benoit-Gagne - Takuvik"
#__date__   = "8 Februart 2016"
#
# Interpreter:
# $ python
# Python 2.7.10 |Anaconda 2.4.0 (x86_64)| (default, Oct 19 2015, 18:31:17) 
# [GCC 4.2.1 (Apple Inc. build 5577)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# Anaconda is brought to you by Continuum Analytics.
# Please check out: http://continuum.io/thanks and https://anaconda.org
#
# See svn/Takuvik/Teledetection/SOP/Python/Python2/Python2Anaconda.docx
# to install Python from Anaconda and netCDF4.

########### Importing modules ###########

from domain.image import image_with_primary_production_pixel

########### main ###########

year = 2006
month = 8
day = 13
doy = 225
grid_file = "/mnt/nfs/output-dev/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2006/225/AM2006225_PP.nc"
rrs_type = "A"
rrs_file = "/mnt/nfs/output-dev/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2006/225/AM2006225_PP.nc"
chl_file = "/mnt/nfs/output-prod/Takuvik/Teledetection/All/Daily/2006/225/A2006225_chlz_00_04.nc"
atm_file = "/mnt/nfs/output-dev/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2006/225/AM2006225_PP.nc"
lut_ed0minus_file = "/mnt/nfs/taku-njall/LUTS/Ed0moins_LUT_5nm_v2.dat"
geospatial_file = "/mnt/nfs/output-prod/Takuvik/Teledetection/Couleur/SORTIES/Bathymetre/Province_Zbot_MODISA_L3binV2.nc"
outfile = "/mnt/nfs/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/2006/225/AM2006225_ppz.nc"

print("processing array1d_ipix_ibin45N...")

array1d_ipix_ibin45N \
    = image_with_primary_production_pixel.ImageWater.get_pixel_with_chlorophyl_information(chl_file)

print(array1d_ipix_ibin45N)

print("processing image...")

image = image_with_primary_production_pixel.ImageWaterLightGeo(year,
                                                               month,
                                                               day,
                                                               doy,
                                                               grid_file,
                                                               rrs_type,
                                                               rrs_file,
                                                               chl_file,
                                                               atm_file,
                                                               lut_ed0minus_file,
                                                               geospatial_file,
                                                               array1d_ipix_ibin45N)

print("exporting to {0}...".format(outfile))

image.export_primary_production(outfile, grid_file)
                           
