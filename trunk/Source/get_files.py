#!/usr/bin/env python2

"""get files list from first files to last file
"""

#__author__ = "Maxime Benoit-Gagne - Takuvik"
#__date__   = "19 August 2016"
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

import os
#############################################################################

def get_files(first_file, last_file):
    """
    Return list of files between first_file and last_file.

    Return a list containing the files between first_file and last_file
    inclusively.

    Args:
        first_file(str):
            First file.
            The pathname of first_file shall be in the format
            */DDD/*DDD_*.*
        last_file(str):
            Last file.
            The pathname of last_file shall be in the format
            */DDD/*DDD_*.*
    Returns:
        List containing the files between first_file and last_file
        inclusively.
    """
    path = os.path.dirname(os.path.dirname(first_file))
    first_DDD = os.path.basename(os.path.dirname(first_file))
    last_DDD = os.path.basename(os.path.dirname(last_file))
    # find prefix
    first_basename = os.path.basename(first_file)
    substr = first_DDD + '_'
    prefix_pos_end = first_basename.find(substr)
    prefix = first_basename[0:prefix_pos_end]
    # find suffix
    suffix = first_basename[prefix_pos_end + len(first_DDD):]
    # construct list of files
    files = []
    for i_file in range(int(first_DDD), int(last_DDD) + 1):
        DDD = (str(i_file)).zfill(3)
        file = path + '/' + DDD + '/' + prefix + DDD + suffix
        files.append(file)
    return files
