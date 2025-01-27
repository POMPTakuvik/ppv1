#!/usr/bin/env python2

"""Get map title from infile

Usage:
    python2 get_title.py infile

infile = File containing data for the map.
         The first character of infile shall be 'A'.
         The second character of infile shall be 'M'.

Example
 infile: /Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_0_0_0/2006/225/AM2006225_pp.nc
 The output of
 python2 get_title.py infile
 will be the character string
 Version 1_0_0_0 Rrs from MODIS_Aqua and atm products from MODIS_Aqua
"""

#__author__ = "Maxime Benoit-Gagne - Takuvik"
#__date__   = "2 August 2016"

import os.path
import sys

try:
    infile = sys.argv[1]
except:
    print __doc__
    sys.exit(1)

doy = os.path.dirname(infile)
year = os.path.dirname(doy)
version = os.path.dirname(year)
doy = os.path.basename(doy)
year = os.path.basename(year)
version = os.path.basename(version)
infile_basename = os.path.basename(infile)
rrs_type = infile_basename[0]
if rrs_type == 'A':
    rrs_string = "MODIS_Aqua"
else:
    print __doc__
    sys.exit(1)
atm_type = infile_basename[1]
if atm_type == 'M':
    atm_string = "MODIS_Aqua"
else:
    print __doc__
    sys.exit(1)
title = "Version " \
        + version \
        + " Rrs from " \
        + rrs_string \
        + " and atm products from " \
        + atm_string
print(title)
