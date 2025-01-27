#!/usr/bin/Rscript
#
# File:    call_NCTakuvik_2_GMT_txt.R
# Author:  Maxime Benoit-Gagne
# Date:    January 14 2015
#
# Usage:
# ./call_NCTakuvik_2_GMT_txt.R infile outfile product_name
#
# description: NetCDF to GMT.
# keywords: NetCDF, GMT.
#
# Brief description of the script:
# Call to the function
# NCTakuvik_2_GMT_txt(infile, outfile, product_name)
# in takuvik.R.
# This call uses the default values of the arguments lon_min, lon_max
# lat_min and lat_max.
#
# NCTakuvik_2_GMT_txt(infile, outfile, product_name, lon_min, lon_max, lat_min, lat_max)
# infile: A PP file. A PP file is a NetCDF file produced by the processing
#         chain at Takuvik also know as the prodprim code. The name of this 
#         file will end with _PP.nc.
# outfile: A text file in GMT format.
#          The GMT format is three columns: longitude, latitude and product.
# product_name: The product name.
# lon_min: Longitude minimum (degrees E).  Default = -180.
# lon_max: Longitude maximume (degrees E). Default =  180.
# lat_min: Latitude minimum (degrees N).   Default =  -90.
# lat_max: Latitude maximum (degrees N).   Default =   90.
# Write the selected region in outfile.

############################# TO MODIFIY #############################

#============================================================================
# Source takuvik.R.
source("takuvik.R")
#============================================================================

############################# END OF TO MODIFIY #############################

# Read the arguments.
args <- commandArgs(TRUE)
infile <- args[1]
outfile <- args[2]
product_name <- args[3]
fill_value <- as.numeric(args[4])

s <- paste("infile: ",
           infile,
           "\n",
           "outfile: ",
           outfile,
           "\n",
           "product_name: ",
           product_name,
           "\n",
           "fill_value: ",
           fill_value,
           "\n",
           sep = ""
)
cat(s)

NCTakuvik_2_GMT_txt(
  infile = infile,
  outfile = outfile,
  product_name = product_name,
  fill_value = fill_value
)
