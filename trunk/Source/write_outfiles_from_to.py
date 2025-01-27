#!/usr/bin/env python2

"""Generate primary productivity from a chlorophyll-a concentration profile.

python2 write_outfiles_from_to.py (without arguments) to see usage.

Interpreter:
$ python
Python 2.7.12 |Anaconda 2.4.0 (x86_64)| (default, Jul  2 2016, 17:43:17) 
[GCC 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2336.11.00)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org

See svn/Takuvik/Teledetection/SOP/Python/Python2/Python2Anaconda.docx
to install Python from Anaconda and netCDF4.
"""

#__author__ = "Maxime Benoit-Gagne - Takuvik"
#__date__   = "19 August 2016"

########### Importing modules ###########

import datetime
import os
import os.path
import shutil
import subprocess
import sys

import get_files
from domain.image import image_with_primary_production_pixel

#############################################################################

hint_no_multithread_same_day = """
Hint about the error: Do not run in parallel two processus of 
write_outfiles_from_to.py for the same day with different arguments.
write_outfiles_from_to.py is not multithread over the same day...
"""

def get_index(input_string, sub_string, ordinal):
    """
    find nth substring in string

    reference: 
    modified from:
    https://stackoverflow.com/questions/21199943/index-of-second-repeated-character-in-a-string

    Args:
        input_string(string):
            Input string.
        sub_string(string):
            Substring.
        ordinal(int):
            Which occurence of the substring is searched.
    Returns:
        The position of the nth substring in string.
    Raises:
        ValueError: 
            If sub_string is not in input_string a number of times equals to 
            ordinal.
    """
    occurences = input_string.count(sub_string)
    if occurences < ordinal:
        raise ValueError("ordinal {} - is invalid".format(ordinal))
    current = -1
    for i in range(ordinal):
        current = input_string.index(sub_string, current + 1)
    #else:
    #    raise ValueError("ordinal {} - is invalid".format(ordinal))
    return current

def get_outfile_temp(file):
    """
    return the name of the temporary outfile under the root of ppv1 project

    return the name of the temporary outfile under the root of ppv1 project
    if necessary

    Example 1:
    file = "/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/2006/225/AM2006225_ppz.nc"
    get_outfile_temp will return "../Outputs/2006/225/AM2006225_ppz.nc"

    Example 2:
    file = "../Outputs/2006/225/AM2006225_ppz.nc"
    get_outfile_temp will return "../Outputs/2006/225/AM2006225_ppz.nc"

    Args:
        file(str):
            File.
            The pathname shall be in the format */DDD/*DDD_*.*
    Returns:
        The name of the temporary outfile under the root of ppv1 project.
        """
    file_temp = file
    if not file.startswith("../Outputs"):
        path = os.path.dirname(os.path.dirname(os.path.dirname(file)))
        file_temp = "../Outputs/" + file[len(path) + 1:]
    return file_temp
    
def pull(file,
         user = "maximebenoit-gagne",
         dns = "taku-eirikr.takuvik.ulaval.ca"):
    """
    pull file from file structure to under the root of ppv1 project

    pull file from file structure to under the root of ppv1 project if
    necessary.

    Example 1:
    file = "/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2006/225/AM2006225_PP.nc"
    pull(file) will copy file to "../Inputs/2006/225/AM2006225_PP.nc" and
    will return "../Inputs/2006/225/AM2006225_PP.nc".

    Example 2:
    file = "../Inputs/2006/225/AM2006225_PP.nc"
    pull(file) will do nothing (because file is already under the root of
    ppv1 project) and will return "../Inputs/2006/225/AM2006225_PP.nc".

    Args:
        file(str):
            File.
            The pathname shall be in the format */DDD/*DDD_*.*
        user(str):
            Username of the user on the remote machine if scp is needed to 
            pull the file.
            This argument is not used if copy is needed to pull the file.
            Defaults to maximebenoit-gagne.
        dns(str):
            Domain Name Server (DNS) name of the remote machine if scp is 
            needed to pull the file.
            This argument is not used if copy is needed to pull the file.
            Defaults to taku-eirikr.takuvik.ulaval.ca.
    Returns:
        The relative pathname of the file under the root of ppv1 project.
    """
    file_dest = file
    if not file.startswith("../Inputs"):
        print("\nmissing file: {}...".format(file))
        path = os.path.dirname(os.path.dirname(os.path.dirname(file)))
        file_dest = "../Inputs/" + file[len(path) + 1:]
        pos_end_volume = get_index(file,
                                   "/",
                                   3)
        volume = file[:(pos_end_volume + 1)]
        if os.path.isdir(volume):
            print(" copying file: {}...".format(file))
            shutil.copyfile(file, file_dest)
        else:
            print(" scp file: {}\n from user: {}\n and from machine: {}..."
                  .format(file,
                          user,
                          dns)
            )
            indir = os.path.dirname(file_dest)
            if not os.path.isdir(indir):
                try:
                    os.makedirs(indir)
                except(OSError) as err:
                    print(hint_no_multithread_same_day)
                    raise err
            subprocess.call(["scp",
                             "-r",
                             user + "@" + dns + ":" + file,
                             file_dest])
            
    return file_dest

def push(source,
         dest,
         user = "maximebenoit-gagne",
         dns = "taku-eirikr.takuvik.ulaval.ca"):
    """
    push source to dest

    push source to dest if source and dest are different.
    does nothing if source and dest are equal.

    Example 1:
    push(source = "../Outputs/2006/225/AM2006225_ppz.nc",
         dest   = "/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/2006/225/AM2006225_ppz.nc")
    will push source to dest.

    Example 2:
    push(source = "/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/2006/225/AM2006225_ppz.nc",
         dest   = "/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/2006/225/AM2006225_ppz.nc")
    will do nothing

    Args:
        source(str):
            File to push.
        dest(str):
            Destination of the file to push.
        user(str):
            Username of the user on the remote machine if scp is needed to 
            push the file.
            This argument is not used if copy is needed to push the file.
            Defaults to maximebenoit-gagne.
        dns(str):
            Domain Name Server (DNS) name of the remote machine if scp is 
            needed to push the file.
            This argument is not used if copy is needed to push the file.
            Defaults to taku-eirikr.takuvik.ulaval.ca.
    Returns:
        nothing
    """
    if source != dest:
        pos_end_volume = get_index(dest,
                                   "/",
                                   3)
        volume = dest[:(pos_end_volume + 1)]
        if os.path.isdir(volume):
            print(" copying file from: {}\n to: {}..."
                  .format(source,
                          dest)
            )
            outdir = os.path.dirname(dest)
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            shutil.copyfile(source, dest)
        else:
            print(" scp file from: {}\n to: {}\n with user: {}\n to machine: {}..."
                  .format(source,
                          dest,
                          user,
                          dns)
            )
            outdir = os.path.dirname(dest)
            subprocess.call(["ssh",
                             user + "@" + dns,
                             "mkdir",
                             "-p",
                             outdir])
            subprocess.call(["scp",
                             "-r",
                             source,
                             user + "@" + dns + ":" + dest])

def write_outfiles_from_to(grid_file,
                           rrs_type,
                           rrs_first_file,
                           rrs_last_file,
                           chl_first_file,
                           chl_last_file,
                           atm_first_file,
                           atm_last_file,
                           lut_ed0minus_file,
                           geospatial_file,
                           chl,
                           first_outfile,
                           last_outfile):
    """
    write oufiles containing primary productivity

    Args:
        grid_file(str): 
            NetCDF file containing the latitudes and longitudes of the
            MODIS ISIN grid above 45 North.
            The file shall include a variable lat and a variable lon of 
            length 3479813.
        rrs_type(char): S for SeaWiFS and A for MODIS-AQUA.
        rrs_first_file(str):
            First NetCDF file containing the variables Rrs412, Rrs443, Rrs488,
            Rrs531, Rrs555 and Rrs667.
            The pathname of rrs_first_file shall be in the format 
            */DDD/*DDD_*.*
        rrs_last_file(str):
            Last NetCDF file containing the variables Rrs412, Rrs443, Rrs488,
            Rrs531, Rrs555 and Rrs667.
            The pathname of rrs_last_file shall be in the format 
            */DDD/*DDD_*.*
        chl_first_file(str):
            First NetCDf file containing the variable
            float chlz(ipix, idepth) ;
                chlz:units = "mgChl-a.m^-3" ;
                chlz:missing_value = -999.f ;
            The pathname of chl_first_file shall be in the format 
            */DDD/*DDD_*.*
        chl_last_file(str):
            Last NetCDf file containing the variable
            float chlz(ipix, idepth) ;
                chlz:units = "mgChl-a.m^-3" ;
                chlz:missing_value = -999.f ;
            The pathname of chl_last_file shall be in the format 
            */DDD/*DDD_*.*
        atm_first_file(str):
            First NetCDF file containing the variables CF_mean, O3_mean
            and TauCld_mean.
            The pathname of atm_first_file shall be in the format 
            */DDD/*DDD_*.*
        atm_last_file(str):
            Last NetCDF file containing the variables CF_mean, O3_mean
            and TauCld_mean.
            The pathname of atm_last_file shall be in the format 
            */DDD/*DDD_*.*
        lut_ed0minus(str):
            The atmospheric lookup table.				   
            Dimensions: Wavelength(83) * Thetas(19) * Ozone(8) * TauCld(8).
        geospatial_file(str):
            NetCDf geospatial information file containing the variables
            float Zbot(ipix) ;
                Zbot:units = "m" ;
            uint8 province(ipix) ;
        chl(str):
            The option to choose to use the surface chlorophyll-a concentration
            or the vertical profile of the chlorophyll-a concentration. 
            surface to use the surface chlorophyll-a concentration. 
            column to use the vertical profile of the chlorophyll-a 
            concentration.
        first_outfile(str):
            First NetCDF output file.
        last_outfile(str):
            Last NetCDF output file.

    Raises:
        ValueError: If the number of files from different types differ.

    """
    rrs_files = get_files.get_files(first_file = rrs_first_file,
                                            last_file  = rrs_last_file)
    chl_files = get_files.get_files(first_file = chl_first_file,
                                            last_file  = chl_last_file)
    atm_files = get_files.get_files(first_file = atm_first_file,
                                            last_file  = atm_last_file)
    outfiles = get_files.get_files(first_file = first_outfile,
                                           last_file  = last_outfile)

    nrrs_files = len(rrs_files)
    nchl_files = len(chl_files)
    natm_files = len(atm_files)
    noutfiles  = len(outfiles)

    if nrrs_files != nchl_files or nrrs_files != natm_files or nrrs_files != noutfiles:
        raise ValueError("""
The number of files from different types differ.
    number of Rrs files: {0}
    number of chlorophyll-a files: {1}
    number of atmospheric files: {2}
    number of output files: {3}
        """.format(nrrs_files,
                   nchl_files,
                   natm_files,
                   noutfiles)
        )

    user = "maximebenoit-gagne"
    dns = "taku-eirikr.takuvik.ulaval.ca"

    for ifile in range(nrrs_files):
        rrs_file = rrs_files[ifile]
        rrs_file_dest = pull(rrs_file, user, dns)
        chl_file = chl_files[ifile]
        chl_file_dest = pull(chl_file, user, dns)
        atm_file = atm_files[ifile]
        atm_file_dest = pull(atm_file, user, dns)
        outfile  = outfiles[ifile]
        outfile_temp = get_outfile_temp(outfile)
 
        year = os.path.basename(os.path.dirname(os.path.dirname(rrs_file_dest)))
        doy = os.path.basename(os.path.dirname(rrs_file_dest))
        fmt = '%Y.%j'
        s = year + '.' + doy
        dt = datetime.datetime.strptime(s, fmt)
        tt = dt.timetuple()
        month = tt.tm_mon
        day = tt.tm_mday

        year = int(year)
        month = int(month)
        day = int(day)
        doy = int(doy)

        try:
            array1d_ipix_ibin45N \
                = image_with_primary_production_pixel.ImageWater.get_pixel_with_chlorophyl_information(chl_file_dest)
        except(IOError) as err:
            print(hint_no_multithread_same_day)
            raise err

        print("processing:")
        print("image = remote_sensing.ImageWaterLightGeo(")
        print("                                          year = {0},"\
              .format(year))
        print("                                          month = {0},"\
              .format(month))
        print("                                          day = {0},"\
              .format(day))
        print("                                          doy = {0},"\
              .format(doy))
        print("                                          grid_file = {0},"\
              .format(grid_file))
        print("                                          rrs_type = {0},"\
              .format(rrs_type))
        print("                                          rrs_file = {0},"\
              .format(rrs_file_dest))
        print("                                          chl_file = {0},"\
              .format(chl_file_dest))
        print("                                          atm_file = {0},"\
              .format(atm_file_dest))
        print("                                          lut_ed0minus_file = {0},"\
              .format(lut_ed0minus_file))
        print("                                          geospatial_file = {0},"\
              .format(geospatial_file))
        print("                                          chl = {0},"\
              .format(chl))
        print("                                          array1d_ipix_ibin45N = ...")
        print("                                         )")

        if chl == 'surface':
            chl_int \
                = image_with_primary_production_pixel.get_array1d_idepth_pp.CHL_SURFACE
        elif chl == 'column':
            chl_int \
                = image_with_primary_production_pixel.get_array1d_idepth_pp.CHL_COLUMN
        else:
            print 'chl shall be either surface or column.'
            sys.exit()

        image = image_with_primary_production_pixel.ImageWaterLightGeo(year,
                                                                       month,
                                                                       day,
                                                                       doy,
                                                                       grid_file,
                                                                       rrs_type,
                                                                       rrs_file_dest,
                                                                       chl_file_dest,
                                                                       atm_file_dest,
                                                                       lut_ed0minus_file,
                                                                       geospatial_file,
                                                                       array1d_ipix_ibin45N,
                                                                       is_surface_chlorophyl= chl_int)

        outdir = os.path.dirname(outfile_temp)
        if not os.path.isdir(outdir):
            os.makedirs(outdir)

        image.export_primary_production(outfile_temp, grid_file)
        # TEST
        #file_object = open(outfile_temp, 'w')
        #file_object.close()
        # END OF TEST
        
        push(outfile_temp, outfile)

        if(rrs_file_dest != rrs_file
           and rrs_file_dest
           != "../Inputs/2006/225/AM2006225_PP_v00_36_00_00.nc"
           and os.path.isfile(rrs_file_dest)):
            os.remove(rrs_file_dest)
        if(chl_file_dest != chl_file
           and chl_file_dest
           != "../Inputs/2006/225/A2006225_chlz_00_05.nc"
           and os.path.isfile(chl_file_dest)):
            os.remove(chl_file_dest)
        if(atm_file_dest != atm_file
           and atm_file_dest
           != "../Inputs/2006/225/AM2006225_PP_v00_36_00_00.nc"
           and os.path.isfile(atm_file_dest)):
            os.remove(atm_file_dest)
        if(outfile_temp != outfile
           and outfile_temp
           != "/Outputs/2006/225/AM2006225_pph_v01_02_09_01.nc"
           and outfile_temp
           != "/Outputs/2006/225/AM2006225_ppz_v01_02_09_01.nc"
           and outfile_temp
           != "/Outputs/2006/225/AM2006225_pph_v01_02_10_01.nc"
           and outfile_temp
           != "/Outputs/2006/225/AM2006225_ppz_v01_02_10_01.nc"
           and os.path.isfile(outfile_temp)):
            os.remove(outfile_temp)

# ---------------------- main ---------------------- #

def main(*args):
    """get arguments

    Args:
        *args: argument list

    Raises:
        ValueError: If (at least) one argument is missing.
    """
    import getopt

    arg_options = ['grid_file=', \
                   'rrs_type=', \
                   'rrs_first_file=', \
                   'rrs_last_file=', \
                   'chl_first_file=', \
                   'chl_last_file=', \
                   'atm_first_file=', \
                   'atm_last_file=', \
                   'lut_ed0minus_file=', \
                   'geospatial_file=', \
                   'chl=', \
                   'first_outfile=', \
                   'last_outfile=']
    opts, arg = getopt.getopt(args, '', arg_options)

    if len(args) == 0:
        print('\nUsage:\n\t python2 write_outfiles_from_to.py --grid_file=<grid_file> --rrs_type=<rrs_type> --rrs_first_file=<rrs_first_file> --rrs_last_file=<rrs_last_file> --chl_first_file=<chl_first_file> --chl_last_file=<chl_last_file> --atm_first_file=<atm_first_file> --atm_last_file=<atm_last_file> --lut_ed0minus_file=<lut_ed0minus_file> --geospatial_file=<geospatial_file> --chl=<chl> --first_outfile=<first_outfile> --last_outfile=<last_outfile>\n')
        print('\t--'+arg_options[0][:-1]+' (required) ==> NetCDF file containing the latitudes and longitudes of the MODIS ISIN grid above 45 North. The file shall include a variable lat and a variable lon of length 3479813.\n')
        print('\t--'+arg_options[1][:-1]+' (required) ==> S for SeaWiFS and A for MODIS-AQUA.\n')
        print('\t--'+arg_options[2][:-1]+' (required) ==> First NetCDF file containing the variables Rrs412, Rrs443, Rrs488, Rrs531, Rrs555 and Rrs667. The pathname of rrs_first_file shall be in the format */DDD/*DDD_*.*\n')
        print('\t--'+arg_options[3][:-1]+' (required) ==> Last NetCDF file containing the variables Rrs412, Rrs443, Rrs488, Rrs531, Rrs555 and Rrs667. The pathname of rrs_last_file shall be in the format */DDD/*DDD_*.*\n')
        print('\t--'+arg_options[4][:-1]+' (required) ==> First NetCDf file containing the variable')
        print('                                        float chlz(ipix, idepth) ;')
        print('                                            chlz:units = "mgChl-a.m^-3" ;')
        print('                                            chlz:missing_value = -999.f ;')
        print('                                        The pathname of chl_first_file shall be in the format */DDD/*DDD_*.*\n')
        print('\t--'+arg_options[5][:-1]+' (required) ==> Last NetCDf file containing the variable')
        print('                                       float chlz(ipix, idepth) ;')
        print('                                           chlz:units = "mgChl-a.m^-3" ;')
        print('                                           chlz:missing_value = -999.f ;')
        print('                                       The pathname of chl_last_file shall be in the format */DDD/*DDD_*.*\n')
        print('\t--'+arg_options[6][:-1]+' (required) ==> First NetCDF file containing the variables CF_mean, O3_mean and TauCld_mean. The pathname of atm_first_file shall be in the format */DDD/*DDD_*.*\n')
        print('\t--'+arg_options[7][:-1]+' (required) ==> Last NetCDF file containing the variables CF_mean, O3_mean and TauCld_mean. The pathname of atm_last_file shall be in the format */DDD/*DDD_*.*\n')
        print('\t--'+arg_options[8][:-1]+' (required) ==> The atmospheric lookup table. Dimensions: Wavelength(83) * Thetas(19) * Ozone(8) * TauCld(8).\n')
        print('\t--'+arg_options[9][:-1]+' (required) ==> NetCDf geospatial information file containing the variables')
        print('                                         float Zbot(ipix) ;')
        print('                                             Zbot:units = "m" ;')
        print('                                         uint8 province(ipix) ;\n')
        print('\t--'+arg_options[10][:-1]+' (optional) ==> The option to choose to use the surface chlorophyll-a concentration or the vertical profile of the chlorophyll-a concentration. surface to use the surface chlorophyll-a concentration. column to use the vertical profile of the chlorophyll-a concentration. Defaults to column.')
        print('\t--'+arg_options[11][:-1]+' (required) ==> First NetCDF output file.\n')
        print('\t--'+arg_options[12][:-1]+' (required) ==> Last NetCDF output file.\n')
    
    else:
        for option,value in opts:
            if option == '--' + arg_options[0][:-1]:
                arg1 = value
            if option == '--' + arg_options[1][:-1]:
                arg2 = value           
            if option == '--' + arg_options[2][:-1]:
                arg3 = value
            if option == '--' + arg_options[3][:-1]:
                arg4 = value   
            if option == '--' + arg_options[4][:-1]:
                arg5 = value   
            if option == '--' + arg_options[5][:-1]:
                arg6 = value   
            if option == '--' + arg_options[6][:-1]:
                arg7 = value   
            if option == '--' + arg_options[7][:-1]:
                arg8 = value   
            if option == '--' + arg_options[8][:-1]:
                arg9 = value   
            if option == '--' + arg_options[9][:-1]:
                arg10 = value   
            if option == '--' + arg_options[10][:-1]:
                arg11 = value   
            if option == '--' + arg_options[11][:-1]:
                arg12 = value
            if option == '--' + arg_options[12][:-1]:
                arg13 = value

        # make some parameters optional
        if 'arg11' not in locals():
            arg11 = 'column'

        options = []
        for option,value in opts:
            options.append(option)

        errmsg = ''
        missing_argument = False
        for arg_option in arg_options:
            if ('--' + arg_option[:-1]) not in options:
                missing_argument = True
                errmsg += "\nargument missing: --{0}".format(arg_option[:-1])
        if missing_argument:
            raise ValueError(errmsg)

        write_outfiles_from_to(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13)
        
# ---------------------- command line ---------------------- #
if __name__=='__main__':
    main(*sys.argv[1:])
