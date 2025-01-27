#!/usr/bin/env python2

"""Generate primary productivity from a chlorophyll-a concentration profile.

Usage:
    python2 run.py
"""

#__author__ = "Maxime Benoit-Gagne - Takuvik"
#__date__   = "29 July 2016"
#
# Interpreter:
# $ python
# Python 2.7.12 |Anaconda 2.4.0 (x86_64)| (default, Jul  2 2016, 17:43:17) 
# [GCC 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2336.11.00)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# Anaconda is brought to you by Continuum Analytics.
# Please check out: http://continuum.io/thanks and https://anaconda.org
#
# See svn/Takuvik/Teledetection/SOP/Python/Python2/Python2Anaconda.docx
# to install Python from Anaconda and netCDF4.

########### Importing modules ###########

import shutil

import write_outfiles_from_to

########### main ###########

# 2006225 to 2006226

grid_file = "/Volumes/output-prod/Takuvik/Teledetection/Grid/trunk/201510151636/A45N.nc"
rrs_type = "A"
rrs_first_file = "/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/35_0_0/NOCLIM/2006/225/AM2006225_PP.nc"
rrs_last_file = "/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/35_0_0/NOCLIM/2006/226/AM2006226_PP.nc"
chl_first_file = "/Volumes/output-prod/Takuvik/Teledetection/All/Daily/2006/225/A2006225_chlz_00_04.nc"
chl_last_file = "/Volumes/output-prod/Takuvik/Teledetection/All/Daily/2006/226/A2006226_chlz_00_04.nc"
atm_first_file = "/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/35_0_0/NOCLIM/2006/225/AM2006225_PP.nc"
atm_last_file = "/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/35_0_0/NOCLIM/2006/226/AM2006226_PP.nc"
lut_ed0minus_file = "/Volumes/taku-njall/LUTS/Ed0moins_LUT.dat"
geospatial_file = "/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/Bathymetre/Province_Zbot_MODISA_L3binV2.nc"
first_outfile = "/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_1_0/2006/225/AM2006225_pp.nc"
last_outfile = "/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_1_0/2006/226/AM2006226_pp.nc"

write_outfiles_from_to.write_outfiles_from_to(
    grid_file = grid_file,
    rrs_type = rrs_type,
    rrs_first_file = rrs_first_file,
    rrs_last_file = rrs_last_file,
    chl_first_file = chl_first_file,
    chl_last_file = chl_last_file,
    atm_first_file = atm_first_file,
    atm_last_file = atm_last_file,
    lut_ed0minus_file = lut_ed0minus_file,
    geospatial_file = geospatial_file,
    first_outfile = first_outfile,
    last_outfile = last_outfile)

infiles=['README', 'run.py']
outdir = '/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_1_0'

for infile in infiles:
    shutil.copy(infile, outdir)
