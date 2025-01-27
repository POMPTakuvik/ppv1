#!/usr/bin/env python2

"""Plot different PP algorithms again each other.

Usage:
    python2 run_compare.py
"""

#__author__ = "Maxime Benoit-Gagne - Takuvik"
#__date__   = "2 August 2016"
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

import os.path
import subprocess

########### main ###########

PPhv0_36_0_0 = "../Inputs/2006/225/AM2006225_PP_v00_36_00_00.nc"
PPhv1_2_9_1 = "../Outputs/2006/225/AM2006225_pph_v01_02_09_01.nc"

xinfile = PPhv0_36_0_0
xproduct = "PP"
yinfile = PPhv1_2_9_1
yproduct = "pp"
outfile = "../Outputs/2006/225/1_2_9_1pph_vs_0_36_0_0pph.jpg"
main = "PPh version 1_2_9_1 vs PPh version 0_36_0_0 on August 13th 2006 above 45 degrees North"
xlab = "PPh version 0_36_0_0  (mgC.m^-2.d^-1)"
ylab = "PPh version 1_2_9_1  (mgC.m^-2.d^-1)"

compare = "./compare.R"

subprocess.call([compare,
                 xinfile,
                 xproduct,
                 yinfile,
                 yproduct,
                 outfile,
                 main,
                 xlab,
                 ylab])

PPhv0_36_0_0 = "../Inputs/2006/225/AM2006225_PP_v00_36_00_00.nc"
PPzv1_2_9_1 = "../Outputs/2006/225/AM2006225_ppz_v01_02_09_01.nc"

xinfile = PPhv0_36_0_0
xproduct = "PP"
yinfile = PPzv1_2_9_1
yproduct = "pp"
outfile = "../Outputs/2006/225/1_2_9_1ppz_vs_0_36_0_0pph.jpg"
main = "PPz version 1_2_9_1 vs PPh version 0_36_0_0 on August 13th 2006 above 45 degrees North"
xlab = "PPh version 0_36_0_0 (mgC.m^-2.d^-1)"
ylab = "PPz version 1_2_9_1 (mgC.m^-2.d^-1)"

compare = "./compare.R"

subprocess.call([compare,
                 xinfile,
                 xproduct,
                 yinfile,
                 yproduct,
                 outfile,
                 main,
                 xlab,
                 ylab])

PPhv1_2_9_1 = "../Outputs/2006/225/AM2006225_pph_v01_02_09_01.nc"
PPzv1_2_9_1 = "../Outputs/2006/225/AM2006225_ppz_v01_02_09_01.nc"

xinfile = PPhv1_2_9_1
xproduct = "pp"
yinfile = PPzv1_2_9_1
yproduct = "pp"
outfile = "../Outputs/2006/225/1_2_9_1ppz_vs_1_2_9_1pph.jpg"
main = "PPz version 1_2_9_1 vs PPh version 1_2_9_1 on August 13th 2006 above 45 degrees North"
xlab = "PPh version 1_2_9_1 (mgC.m^-2.d^-1)"
ylab = "PPz version 1_2_9_1 (mgC.m^-2.d^-1)"

compare = "./compare.R"

subprocess.call([compare,
                 xinfile,
                 xproduct,
                 yinfile,
                 yproduct,
                 outfile,
                 main,
                 xlab,
                 ylab])
