#!/usr/bin/env python2

"""Functions to read and write NetCDF4 files.
"""

# author: Maxime Benoit-Gagne - Takuvik - Canada.
# date of creation: November 12, 2015.
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
#
# See svn/Takuvik/Teledetection/SOP/Python/Python2/Python2Anaconda.docx
# to install Python from Anaconda and netCDF4.

########### Importing modules ###########

import netCDF4
import numpy as np
import sys

########### functions ###########

"""
Read a 1d variable from a NetCDF4 file.

Args:
    ncfile(str):
        The netCDF4 file.
    variable(str):
        The variable name.
        The variable has one dimension.
        The type of the variable has is the same as in the NetCDF4 file.

Returns:
    numpy.array:
    Array of dimension n.
    The first dimension is the dimension of variable.
    The values are the values of variable.

Raises:
    IOError: If ncfile is not found or doesn't contain a variable named
    variable.

"""
def get_array1d_i_val(ncfile, variable):
    try:
        # open the netCDF file for reading.
        fh = netCDF4.Dataset(ncfile,'r')
    except:
        raise IOError("File not found: {}.".format(ncfile))
    try:
        # read the data in variable named array1d_i_val.
        array1d_i_val = fh.variables[variable][:]
    except:
        raise IOError("Variable {} not found in {}.".format(variable, ncfile))
    fh.close()
    return array1d_i_val

"""
Read a 2d variable in float32 form a NetCDF4 file.

Args:
    ncfile(str):
        The netCDF4 file.
    variable(str):
        The variable name.
        The variable has two dimensions.
        The type of the variable has is the same as in the NetCDF4 file.

Returns:
    numpy.array:
    Array of dimension nx*ny.
    The first dimension is the first dimension of the variable.
    The second dimension is the second dimension of the variable.
    The values are the values of variable.

Raises:
    IOError: If ncfile is not found or doesn't contain a variable named
    variable.

"""
def get_array2d_i_j_val(ncfile, variable):
    try:
        # open the netCDF file for reading.
        fh = netCDF4.Dataset(ncfile,'r')
    except:
        raise IOError("File not found: {}.".format(ncfile))
    try:
        # read the data in variable named array1d_i_val.
        array2d_i_j_val = fh.variables[variable][:]
        
    except:
        raise IOError("Variable {} not found in {}.".format(variable, ncfile))
    fh.close()
    return array2d_i_j_val



"""
Read a variable in a NetCDF4 file and write it in another NetCDF4 file.

Args:
    infile(str):
        The input netCDF4 file.
    variable(str):
        The variable name.
    outfile(str):
        The output netCDF4 file.
        If outfile doesn't exist, it is created.

Raises:
    IOError: If infile is not found, doesn't contain a variable named
    variable or the path for outfile doesn't exist.

"""
# Standby.
