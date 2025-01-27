# Maxime Benoit-Gagne
# Creation: November 25, 2013

# Useful functions in R.

##############################################################################
# Packages.
library(ncdf4)

##############################################################################
# Functions not to be called from another .R script.

# Maxime Benoit-Gagne
# February 6, 2014
# vec_ipixin_lon: Longitudes of the pixels (degrees E).
# vec_ipixin_lat: Latitudes of the pixels (degrees N).
# vec_ipixin_prod: Value of the pixels.
# product_name: The name of the product. Default = "".
# outfile: A GMT text file containing three columns: longitude, latitude and product.
# lon_min: Longitude minimum (degrees E).  Default = -180.
# lon_max: Longitude maximume (degrees E). Default =  180.
# lat_min: Latitude minimum (degrees N).   Default =  -90.
# lat_max: Latitude maximum (degrees N).   Default =   90.
# vec_ipixin_l2flags: l2 flags.            Default = NULL.
# fill_value: Fill value to remove from outfile. Default = NULL.
# Select and export pixels to a GMT text file.
export <- function(
  vec_ipixin_lon,
  vec_ipixin_lat,
  vec_ipixin_prod,
  product_name = "",
  outfile,
  lon_min = -180,
  lon_max = 180,
  lat_min = -90,
  lat_max = 90,
  vec_ipixin_l2flags = NULL,
  fill_value = NULL
  ){
  df_ipixout.df <- select(
    vec_ipixin_lon,
    vec_ipixin_lat,
    vec_ipixin_prod,
    lon_min = lon_min,
    lon_max = lon_max,
    lat_min = lat_min,
    lat_max = lat_max,
    fill_value = fill_value
  )
  if(product_name == "Ice"){
    vec_ipixout_lon <- df_ipixout.df$lon
    vec_ipixout_lat <- df_ipixout.df$lat
    vec_ipixout_prod <- df_ipixout.df$prod
    Ice_max <- 1.002
    off <- vec_ipixout_prod > Ice_max
    vec_ipixout_prod[off] <- NA
    df_ipixout.df <- data.frame(
      vec_ipixout_lon,
      vec_ipixout_lat,
      vec_ipixout_prod
      )
  }
  if(!is.null(vec_ipixin_l2flags)){
    df_ipixout_l2flags.df <- select(
      vec_ipixin_lon = vec_ipixin_lon,
      vec_ipixin_lat = vec_ipixin_lat,
      vec_ipixin_prod = vec_ipixin_l2flags,
      lon_min = lon_min,
      lon_max = lon_max,
      lat_min = lat_min,
      lat_max = lat_max
    )
    colnames <- colnames(df_ipixout_l2flags.df)
    colnames <- c(colnames[1:2], "l2_flags")
    colnames(df_ipixout_l2flags.df) <- colnames
    df_ipixout.df <- cbind(
      df_ipixout.df,
      df_ipixout_l2flags.df["l2_flags"]
      )
  }
  write.table(
    x = df_ipixout.df,
    file = outfile,
    quote = FALSE,
    row.names = FALSE,
    col.names = FALSE
  )
}
##############################################################################

# Maxime Benoit-Gagne
# January 28 2015
# d1: A NetCDF4 dimension.
# d2: A NetCDF4 dimension.
# Return TRUE if both dimensions have the same name but different characteristics.
incompatible<- function(d1, d2){
  ret <- F
  if(d1$name == d2$name
     &&
     (d1$len != d2$len || d1$units != d2$units || d1$vals != d2$vals)
  ){
    ret <- T
  }
  ret
}
##############################################################################

# Maxime Benoit-Gagne
# March 18 2014
# vec_ipixin_lon: Longitudes of the pixels (degrees E).
# vec_ipixin_lat: Latitudes of the pixels (degrees N).
# vec_ipixin_prod: Value of the pixels.
# lon_min: Longitude minimum (degrees E).  Default = -180.
# lon_max: Longitude maximume (degrees E). Default =  180.
# lat_min: Latitude minimum (degrees N).   Default =  -90.
# lat_max: Latitude maximum (degrees N).   Default =   90.
# fill_value: Fill value to remove from outfile. Default = NULL.
# Return a data frame of the selected region.
# The data frame has the three variables lon, lat and prod.
select <- function(
  vec_ipixin_lon,
  vec_ipixin_lat,
  vec_ipixin_prod,
  lon_min = -180,
  lon_max = 180,
  lat_min = -90,
  lat_max = 90,
  fill_value = NULL
){
  indOut <- vec_ipixin_lon > lon_min & vec_ipixin_lon < lon_max & vec_ipixin_lat > lat_min & vec_ipixin_lat < lat_max
  if(!is.null(fill_value)){
    indOut <- indOut & vec_ipixin_prod != fill_value
  }
  indOut[is.na(indOut)] <- F
  vec_ipixout_lon <- vec_ipixin_lon[indOut]
  vec_ipixout_lat <- vec_ipixin_lat[indOut]
  vec_ipixout_prod <- vec_ipixin_prod[indOut]
  df_ipixout.df <- data.frame(
    vec_ipixout_lon,
    vec_ipixout_lat,
    vec_ipixout_prod
  )
  colnames(df_ipixout.df) <- c("lon", "lat", "prod")
  df_ipixout.df
}

##############################################################################
##############################################################################
# Functions to be called from another .R script.
# See the script test_takuvik.R for an example.

# Maxime Benoit-Gagne
# August 10 2016
#
# infiles: A vector of files paths. The files shall be NetCDF files containing  
#          one dimension variables all of the same length.
# vars: A dataframe. The observations (rows) are the variables The first
#      column is the variable name. The second column is the fill value.
# outfile: The output file containing the binning of var in infiles. The 
#          binning is computed with the median excluding pixels with the
#          fill value.
# Return an error message and exit if one variable in vars is not in the
# first infile of infiles.
# Create outfile (and the path to outfile) if outfile doesn't exist.
# Add variable to outfile if outfile exists but variable is not in outfile.
# Update variable in outfile if outfile exist and variable is in outfile.
#
# Example
# See test_bin.R.
bin <- function(infiles, vars, outfile){# print general message
  infiles_s <- " infiles="
  for (i in 1:(length(infiles) - 1)){
    infile <- infiles[i]
    infiles_s <- paste(
      infiles_s,
      infile,
      ",",
      sep = ""
    )
  }
  i <- i + 1
  infile <- infiles[i]
  infiles_s <- paste(
    infiles_s,
    infile,
    "\n",
    sep = ""
  )
  vars_s <- " vars="
  nvars <- nrow(vars)
  if(nvars > 1){
    for (i in 1:(nvars - 1)){
      cat(sprintf("i: %d\n", i))
      varname <- vars[i, 1]
      fill_value <- vars[i, 2]
      vars_s <- paste(
        vars_s,
        varname,
        "(",
        "fill value=",
        fill_value,
        ")",
        ",",
        sep = ""
      )
    }
  }
  i <- nvars
  varname <- vars[i, 1]
  fill_value <- vars[i, 2]
  vars_s <- paste(
    vars_s,
    varname,
    "(",
    "fill value=",
    fill_value,
    ")",
    "\n",
    sep = ""
  )
  outfile_s <- paste(
    " outfile=",
    outfile,
    "\n\n",
    sep = ""
  )
  general_msg <- paste(
    "takuvik.R:bin\n",
    infiles_s,
    vars_s,
    outfile_s,
    sep = ""
  )
  cat(general_msg)
  
  # create outfile
  dirname <- dirname(outfile)
  if(!dir.exists(dirname)){
    dir.create(dirname)
  }
  first_infile <- infiles[1]
  nc_first_infile <- nc_open(
    filename = first_infile
  )
  nc_close(nc_first_infile)
  vars_infile <- nc_first_infile$var
  vars_outfile <- list()
  nvar <- nrow(vars)
  for (ivar in 1:nvar){
    varname <- vars[ivar, 1]
    if(varname %in% names(vars_infile)){
      var_infile <- vars_infile[ivar]
      vars_outfile <- c(vars_outfile, var_infile)
    }else{
      err_msg <- sprintf(
        "Variable %s is not in file %s.",
        varname,
        first_infile
      )
      stop(err_msg,
           call. = F)
    }
  }
  if(file.exists(outfile)){
    nc_outfile <- nc_open(
      filename = outfile,
      write = T
    )
    for (ivar in 1:nvar){
      varname <- vars[ivar, 1]
      vars_outfile <- nc_outfile$var
      if(!(varname %in% names(vars_outfile))){
        var_infile <- vars_infile[[which(names(vars_infile) == varname)]]
        nc_outfile <- ncvar_add(
          nc = nc_outfile,
          v = var_infile
        )
      }
    }
  }else{
    nc_outfile <- nc_create(
      filename = outfile,
      vars = vars_outfile
    )
  }
  
  npix <- nc_outfile$dim[[1]]$len
  nfiles <- length(infiles)
  for(ivar in 1:nvar){
    varname <- vars[ivar, 1]
    # read infiles
    matrix_ipix_ifile_val <- matrix(
      nrow = npix,
      ncol = nfiles
    )
    fill_value <- vars[ivar, 2]
    for (ifile in 1:nfiles){
      infile <- infiles[ifile]
      nc_infile <- nc_open(
        filename = infile
      )
      array1d_ipix_val <- ncvar_get(
        nc = nc_infile,
        varid = varname
      )
      for (ipix in 1:npix){
        val <- array1d_ipix_val[ipix]
        if (val == fill_value){
          val = NA
        }
        matrix_ipix_ifile_val[ipix, ifile] <- val
      }
      nc_close(nc_infile)
    }
    # bin
    array1d_ipix_val <- array(
      dim = npix
    )
    for (ipix in 1:npix){
      val <- median(
        matrix_ipix_ifile_val[ipix,],
        na.rm = T
      )
      if(is.na(val)){
        val <- fill_value
      }
      array1d_ipix_val[ipix] <- val
    }
    # write
    ncvar_put(
      nc = nc_outfile,
      varid = varname,
      vals = array1d_ipix_val
    )
  }
  nc_close(nc_outfile)
}

################################################################
# Maxime Benoit-Gagne
# September 2 2014
# x: A vector.
# target: The target value.
# npos: The number of positions to be returned.
# Return the positions of the npos values closest to target.
# Example:
#
# x <- c(0.05, 1.2, 3, 1.01, 0.9)
# closest <- closest(x, 1, 3)
#
# closest contains:
# 4 5 2
closest <- function(x, target, npos){
  abs <- abs(x - target)
  sort <- sort(abs)
  vec_pos <- c()
  i <- 1
  while(i <= npos){
    val <- sort[i]
    pos <- which(abs == val)
    vec_pos <- c(vec_pos, pos)
    i <- i + length(pos)
  }
  vec_pos
}
################################################################

# Author:  Maxime Benoit-Gagne
# Creation: August 5, 2016
# xinfile: An input file in NetCDF format.
# xproduct: The name of a one-dimension variable in xinfile.
# yinfile: An input file in NetCDF format.
# yproduct: The name of a one-dimension variable in yinfile.
#           yproduct shall have the same dimension of xproduct.
#           If not, the result is undetermined.
# outfile: The output file containing a plot of yproduct versus xproduct.
compare <- function(xinfile,
                    xproduct,
                    yinfile,
                    yproduct,
                    outfile){
  
  xncfile <- nc_open(xinfile)
  array1d_ipix_xproduct <- ncvar_get(
    nc = xncfile,
    varid = xproduct
  )
  nc_close(xncfile)
  yncfile <- nc_open(yinfile)
  array1d_ipix_yproduct <- ncvar_get(
    nc = yncfile,
    varid = yproduct
  )
  nc_close(yncfile)
  dir_outfile <- dirname(outfile)
  if(!dir.exists(dir_outfile)){
    dir.create(dir_outfile)
  }
  pdf(file = outfile)
  plot(
    x = array1d_ipix_xproduct,
    y = array1d_ipix_yproduct,
    type = "p",
    xlab = xproduct,
    ylab = yproduct
  )
  
  box()
  dev.off()
}

##############################################################################

# Maxime Benoit-Gagne
# October 3 2014
# infile: The infile containing the following data set: Moderate Resolution 
#         Imaging Spectroradiometer (MODIS)/Aqua Aerosol Cloud Water Vapor
#         Ozone Daily L3 Global 1Deg CMG (MYD08 D3).
#         This data set comes from the National Aeronautics and Space
#         Administration (NASA) Level 1 and Atmosphere Archive and
#         Distribution System (LAADS) (v5.1).
#         The platform is Aqua.
#         The sensor is MODIS.
#         The temporal resolution is daily.
#         The spatial resolution is 1 x 1 degree.
#         Information on this data set can be found at this website:
#         http://ladsweb.nascom.nasa.gov/data/ftp_site.html
#         Data itself can be found at this ftp url:
#         ftp://ladsweb.nascom.nasa.gov/allData/51/MYD08_D3/
# lut: The lookup table that takes the wavelength, the thetas, the ozone and
#      the optical thickness to retrieve the downward irradiance.
#      The dimensions of the lut are:
#      Wavelength(83) * Thetas(19) * Ozone(8) * TauCld(8).
# lat: The latitude in degrees N from -90 to 90.
# lon: The longitude in degrees E from -180 to 180.
# Return a matrix.
# The first dimension is the indices of the wavelengths from 290 nm to 700 nm
# by step of 5 nm.
# The second dimension is the indices of the times from 0h UTC (Coordinated
# Universal Time) to 21h by step of 3 h.
# The values are the downward irradiance computed using the lookup table.
# The units are umol photons.m^-2.s^-1.nm^-1.
ed <- function(infile, lut, lat, lon){
  basename <- basename(infile)
  doy <- substr(
    x = basename,
    start = 15,
    stop = 17
    )
  cmd <- paste(
    "~/svn/Takuvik/Teledetection/Util/Ed/edMODISA ",
    infile,
    " ",
    lut,
    " ",
    lat,
    " ",
    lon,
    " ",
    doy,
    " > zz",
    sep = ""
    )
  system(cmd)
  matrix_ilambda_itime_ed0minus <- read.table("zz")
  matrix_ilambda_itime_ed0minus
}


################################################################

# Maxime Benoit-Gagne
# November 25, 2013
# year: The year.
# julian_day: The julian day.
# Return the month and the day of the month in a data frame.
# data.frame$month to get the month.
# data.frame$day to get the day of the month.
get_month_day <- function(year,
                          julian_day){
  days_per_month <- c(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
  if(year %% 4 == 0 && (year %% 100 != 0 || year %% 400 == 0)){
    days_per_month[2] <- 29
  }
  sum_temp <- days_per_month[1]
  month <- 2
  while(julian_day > sum_temp){
    sum_temp <- sum_temp + days_per_month[month]
    month <- month + 1
  }
  month <- month - 1
  sum_temp <- sum_temp - days_per_month[month]
  day <- julian_day - sum_temp
  month_day.df <- data.frame(month, day)
  month_day.df
}
##############################################################################

# Maxime Benoit-Gagne
# March 18, 2014
# infile: A text file in GMT format.
# outfile: A text file in GMT format.
# lon_min: Longitude minimum (degrees E).  Default = -180.
# lon_max: Longitude maximume (degrees E). Default =  180.
# lat_min: Latitude minimum (degrees N).   Default =  -90.
# lat_max: Latitude maximum (degrees N).   Default =   90.
# Write the selected region in outfile.
GMT_txt_2_GMT_txt <- function(infile,
                              outfile,
                              lon_min = -180,
                              lon_max = 180,
                              lat_min = -90,
                              lat_max = 90
  ){
  df_ipixin.df <- read.table(
    file = infile,
    col.names = c("lon", "lat", "prod")
    )
  vec_ipixin_lon <- df_ipixin.df$lon
  vec_ipixin_lat <- df_ipixin.df$lat
  vec_ipixin_prod <- df_ipixin.df$prod
  export(
    vec_ipixin_lon = vec_ipixin_lon,
    vec_ipixin_lat =  vec_ipixin_lat,
    vec_ipixin_prod = vec_ipixin_prod,
    outfile = outfile,
    lon_min = lon_min,
    lon_max = lon_max,
    lat_min = lat_min,
    lat_max = lat_max
  )
}
##############################################################################

# Maxime Benoit-Gagne
# Creation: July 22, 2014
# file1: A text file.
# file2: A text file. (file1 and file2 have the same number of rows).
# pos_insert1: The insertion position.
#              (pos_insert1 <= number of columns in file1 + 1).
# start2: The index of a column in file2 (inclusive).
# end2: The index of a column in file2 (inclusive). (end2 >= start2).
# sep: The field separator character. The default is sep = '' which means 'white 
#      space', that is one or more spaces, tabs, newlines or carriage returns.
# Add columns start2 to end2 of file 2 at position pos_insert1 of file 1.
# Example:
# BEFORE
# file1.txt
# A C
#
# file2.txt
# A B C
#
# CALL OF FUNCTION
# insert_columns(file1        = 'file1.txt',
#                file2        = 'file2.txt',
#                pos_insert1  = 2,
#                start2       = 2,
#                end2         = 2)
#
# AFTER
# file1.txt
# A B C
insert_columns <- function(
  file1,
  file2,
  pos_insert1,
  start2,
  end2,
  sep = ''
){
  test1.df <- read.table(
    file = file1,
    sep = sep,
    colClasses = 'character',
    comment.char = ''
  )
  test2.df <- read.table(
    file = file2,
    sep = sep,
    colClasses = 'character',
    comment.char = ''
  )
  if( nrow(test1.df) != nrow(test2.df) ){
    stop(
      "file1: ",
      file1,
      " and file2: ",
      file2,
      " don't have the same number of lines.",
      sep = ""
      )
  }
  test2_slice.df <- test2.df[start2:end2]
  if(pos_insert1 >= 2){
    test1_new.df <- test1.df[1:pos_insert1 - 1]
  }else{
    test1_new.df <- data.frame(row.names = 1:nrow(test1.df))
  }
  test1_new.df <- cbind(test1_new.df, test2_slice.df)
  if(pos_insert1 <= ncol(test1.df)){
    test1_end.df <- test1.df[pos_insert1:ncol(test1.df)]
    test1_new.df <- cbind(test1_new.df, test1_end.df)
  }
  if(sep == ''){
  	sep <- ' '
  }
  write.table(
    x = test1_new.df,
    file = file1,
    quote = FALSE,
    sep = sep,
    row.names = FALSE,
    col.names = FALSE
  )
}
##############################################################################

# Maxime Benoit-Gagne
# September 29 2014
# x: An object.
# Return mean(x, na.rm = T).
# It is usually better to use the function mean with the argument na.rm = T
# instead of using this function mean_na.rm.
# But, we can't pass the function mean with the argument na.rm = T as an 
# argument to another function.
# (We can pass functions as arguments to other functions in R.)
# In this case, mean_na.rm can be used.
# Example:
#
# x <- c(0, NA, 1)
# mean_na.rm <- mean_na.rm(x)
#
# mean_na.rm contains:
# 0.5
mean_na.rm <- function(x){
  mean(x, na.rm = T)
}
##############################################################################

# Maxime Benoit-Gagne
# October 2 2014
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
# fill_value: Fill value to remove from outfile. Default = -999
# Write the selected region in outfile.
NCTakuvik_2_GMT_txt <- function(infile,
                                outfile,
                                product_name,
                                lon_min = -180,
                                lon_max = 180,
                                lat_min = -90,
                                lat_max = 90,
                                fill_value = -999){
  ncfile <- nc_open(infile)
  vec_ipixin_lon <- ncvar_get(ncfile, "lon")
  vec_ipixin_lat <- ncvar_get(ncfile, "lat")
  vec_ipixin_prod <- ncvar_get(ncfile, product_name)
  outdir <- dirname(outfile)
  if(!file.exists(outdir)){
    dir.create(
      path = outdir,
      recursive = T
    )
  }
  export(
    vec_ipixin_lon = vec_ipixin_lon,
    vec_ipixin_lat = vec_ipixin_lat,
    vec_ipixin_prod = vec_ipixin_prod,
    outfile = outfile,
    lon_min = lon_min,
    lon_max = lon_max,
    lat_min = lat_min,
    lat_max = lat_max,
    fill_value = fill_value
  )
}
##############################################################################

# Author:  Maxime Benoit-Gagne
# Creation: July 22, 2014
# infile: An input file in a GMT text format (longitude latitude product).
# outfile: An output file in a GMT text format where the lines with a
#          product > val in column col are removed.
# val: A numeric value.
# col: A column index.
#      If col > ncol, stops the execution and return an error message.
# sep: The field separator character.
#      The default is sep = '' which means 'white space', that is one or 
#      more spaces, tabs, newlines or carriage returns.
#
# Example:
# infile.txt
# 100 45 99
# 100 45 100
# 100 45 101
# 100 45 NaN
#
# outfile.txt
# 100 45 99
# 100 45 100
# 100 45 NA
remove_values_gt_in_column <- function(infile,
                                       outfile,
                                       val,
                                       col,
                                       sep = ''){
  infile.df <- read.table(
    file = infile,
    sep = sep,
    colClasses = 'numeric',
    comment.char = ''
  )
  if(col > ncol(infile.df)){
    stop("col is not a valid column index.")
  }
  bad <- infile.df[,col] > val
  nas <- is.na(bad)
  bad[nas] <- F
  outfile.df <- infile.df[!bad,]
  write.table(
    x = outfile.df,
    file = outfile,
    quote = F,
    row.names = F,
    col.names = F
  )
}
##############################################################################

# Maxime Benoit-Gagne
# January 27 2015
#  indir: The directory of the input files.
#  prefix_infile: The prefix of the files in indir.
#                 The files have the following name format 
#                 <prefix_infile>YYYYDDD<suffix_infile>
#  suffix_infile: The suffix of the files in indir.
#                 The files have the following name format 
#                 <prefix_infile>YYYYDDD<suffix_infile>
#  variable: The varible name.
#  outdir: The directory of the output files.
#  prefix_outfile: The suffix of the files in outdir
#                  The files have the following name format 
#                  <prefix_outfile>YYYYDDD<suffix_outfile>
#  suffix_outfile: The suffix of the files in outfile.
#                  The files have the following name format 
#                  <prefix_outfile>YYYYDDD<suffix_outfile>
#  first_year: The first year.
#  last_year: The last year.
#  first_doy: The first day of year.
#  last_doy: The last day of year.
#  same_infile: T if the same infile is used for all outfiles.
#                It will be case for grid data or bathymetry for example.
#               F if a different infile is used for each outfile.
#               default: F.
#
# Read and write a variable in a tree of Takuvik files.
#
# Example
# 1/
#   2006/
#        225/
#            pp2006225ss.nc; containing variable a.
#        226/
#            pp2006226ss.nc; containing variable a.
#   2007/
#        225/
#            pp2007225ss.nc; containing variable a.
#        226/
#            pp2007226ss.nc; containing variable a.
# 2/
#   2006/
#        225/
#            pp2006225ss.nc; containing variable b.
#        226/
#            pp2006226ss.nc; containing variable b.
#   2007/
#        225/
#            pp2007225ss.nc; containing variable b.
#        226/
#            pp2007226ss.nc; containing variable b.
#
# run_update_var(
#  indir = "1",
#  prefix_infile = "pp",
#  suffix_infile = "ss.nc",
#  variable = "a",
#  outdir = "2",
#  prefix_outfile = "pp",
#  suffix_outfile = "ss.nc",
#  first_year = 2006,
#  last_year = 2007,
#  first_doy = 225,
#  last_doy = 226
# )
#
# results into
# 1/
#   2006/
#        225/
#            pp2006225ss.nc; containing variable a.
#        226/
#            pp2006226ss.nc; containing variable a.
#   2007/
#        225/
#            pp2007225ss.nc; containing variable a.
#        226/
#            pp2007226ss.nc; containing variable a.
# 2/
#   2006/
#        225/
#            pp2006225ss.nc; containing variables a and b.
#        226/
#            pp2006226ss.nc; containing variables a and b.
#   2007/
#        225/
#            pp2007225ss.nc; containing variables a and b.
#        226/
#            pp2007226ss.nc; containing variables a and b.
run_update_var <- function(
  indir,
  prefix_infile,
  suffix_infile,
  variable,
  outdir,
  prefix_outfile,
  suffix_outfile,
  first_year,
  last_year,
  first_doy,
  last_doy,
  same_infile = F
){
  for(year in seq(first_year, last_year)){
    for(doy in seq(first_doy, last_doy)){
      if(same_infile){
        infile <- sprintf(
          "%s/%s%s",
          indir,
          prefix_infile,
          suffix_infile
        )
      }else{
        infile <- sprintf(
          "%s/%i/%03i/%s%i%03i%s",
          indir,
          year,
          doy,
          prefix_infile,
          year,
          doy,
          suffix_infile
        )
      }
      outfile <- sprintf(
        "%s/%i/%03i/%s%i%03i%s",
        outdir,
        year,
        doy,
        prefix_outfile,
        year,
        doy,
        suffix_outfile
      )
      update_var(
        infile = infile,
        variable = variable,
        outfile = outfile
      )
    }
  }
}

##############################################################################

# Maxime Benoit-Gagne
# September 29 2014
# x: An object.
# Return sd(x, na.rm = T).
# It is usually better to use the function sd with the argument na.rm = T
# instead of using this function sd_na.rm.
# But, we can't pass the function sd with the argument na.rm = T as an 
# argument to another function.
# (We can pass functions as arguments to other functions in R.)
# In this case, sd_na.rm can be used.
# Example:
#
# x <- c(0, NA, 1)
# sd_na.rm <- sd_na.rm(x)
#
# sd_na.rm contains:
# 0.7071068
sd_na.rm <- function(x){
  sd(x, na.rm = T)
}

##############################################################################

# Maxime Benoit-Gagne
# January 27 2015
#
# infile: The input NetCDF file in Takuvik format.
# variable: The variable name.
# outfile: The output NetCDF file in Takuvik format.
# Return 0 if the execution was normal.
# Return -1 if not.
#
# Read and write a varible from infile to outfile.
#
# Return an error message and doesn't exit if infile doesn't exist.
# Return an error message and doesn't exit if variable is not in infile.
# Create outfile (and the path to outfile) if outfile doesn't exist.
# Update variable if variable already exists in outfile.
# Return an error message and exit if one of the dimensions of variable 
# in infile exists in outfile with different characteristics.
#
# Example
# Let the following files:
# in2006225ss.nc; containing variable a.
# out2006225ss.nc; containing variable b.
#
# update_var(
# infile = "in2006225ss.nc",
# variale = "a",
# outfile = "out2006225ss.nc"
#)
#
# results into
# in2006225ss.nc; containing variable a.
# out2006225ss.nc; containing variables a and b.
update_var <- function(infile, variable, outfile){
  general_msg <- sprintf(
    "takuvik.R:update_var\n infile=%s\n variable=%s\n outfile=%s\n",
    infile,
    variable,
    outfile
  )
  ret <- 0
  file_exists <- T
  variable_exists <- T
  outfile_exists <- F
  compatible_dims <- T
  cat(general_msg)
  # Test arguments.
  if(!file.exists(infile)){
    err_msg <- sprintf(
      "  infile not found: %s\n",
      infile
    )
    msg <- paste(
      general_msg,
      err_msg,
      sep = ""
    )
    cat(msg)
    ret <- -1
    file_exists <- F
  }
  if(file_exists){
    nc_infile <- nc_open(
      filename = infile
    )
    if(!(variable %in% names(nc_infile$var))){
      err_msg <- sprintf(
        "  variable %s not found in infile %s\n",
        variable,
        infile
      )
      msg <- paste(
        general_msg,
        err_msg,
        sep = ""
      )
      cat(msg)
      ret <- -1
      variable_exists <- F
    }
    nc_close(nc_infile)
  }
  if(file_exists && variable_exists){
    outfile_exists <- file.exists(outfile)
    if(outfile_exists){
      nc_infile <- nc_open(
        filename = infile
      )
      # dimensions of variable in infile
      Di <- (nc_infile$var[[which(names(nc_infile$var) == variable)]])$dim
      nc_close(nc_infile)
      nc_outfile <- nc_open(
        filename = outfile
      )
      # dimensions in outfile
      Do <- nc_outfile$dim
      nc_close(nc_outfile)
      # for each dimension of variable in infile
      for(di in Di){
        # for each dimension in outfile
        for(do in Do){
          if(incompatible(di, do)){
            err_msg <- sprintf(
              "  The dimensions of variable %s in infile %s exist in outfile %s with different characteristics.\n",
              variable,
              infile,
              outfile
            )
            msg <- paste(
              general_msg,
              err_msg,
              sep = ""
            )
            ret <- -1
            compatible_dims <- F
            stop(msg,
                 call. = F)
          }
        }
      }
    }
  }
  # Execution
  if(file_exists && variable_exists && compatible_dims){
    nc_infile <- nc_open(
      filename = infile
    )
    units_ncatt <- ncatt_get(
      nc = nc_infile,
      varid = variable,
      attname = "units"
    )
    if(units_ncatt$hasatt){
      units <- units_ncatt$value
    }else{
      units <- ""
    }
    dim <- (nc_infile$var[[which(names(nc_infile$var) == variable)]])$dim
    missval_ncatt <- ncatt_get(
      nc = nc_infile,
      varid = variable,
      attname = "_FillValue"
    )
    if(missval_ncatt$hasatt){
      missval <- missval_ncatt$value
    }else{
      missval <- NULL
    }
    data <- ncvar_get(
      nc = nc_infile,
      varid = variable
    )
    nc_close(nc_infile)
    var <- ncvar_def(
      name = variable,
      units = units,
      dim = dim,
      missval = missval,
      compression = 9
    )
    if(outfile_exists){
      nc_outfile <- nc_open(
        filename = outfile,
        write = T
      )
    }else{
      outdir <- dirname(outfile)
      if(!file.exists(outdir)){
        dir.create(
          path = outdir,
          recursive = T
        )
      }
      nc_outfile <- nc_create(
        filename = outfile,
        vars = var,
        force_v4 = T
      )
    }
    if(length(which(names(nc_outfile$var) == variable)) == 0){
      ncvar_add(
        nc = nc_outfile,
        v = var
      )
    }
    nc_close(nc_outfile)
    nc_outfile <- nc_open(
      filename = outfile,
      write = T
    )
    ncvar_put(
      nc = nc_outfile,
      varid = var,
      vals = data
    )
    nc_close(nc_outfile)
  }
  ret
}