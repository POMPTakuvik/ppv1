#!/usr/bin/env python2

"""Get map year and day of year from infile

Usage:
    python2 get_bottomright.py infile

infile = File containing data for the map.

Example
 infile: /Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_0_0_0/2006/225/AM2006225_pp.nc
 The output of
 python2 get_title.py infile
 will be the character string
 2006-225
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
doy = os.path.basename(doy)
year = os.path.basename(year)
bottomright = str(year) + '-' + str(doy)
print(bottomright)
