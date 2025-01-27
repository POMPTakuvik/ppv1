#!/usr/bin/env Rscript
#
# File:    compare.R
# Author:  Maxime Benoit-Gagne
# Creation: August 5, 2014
#
# Usage:
# ./compare.R [xinfile xproduct yinfile yproduct outfile main xlab ylab]
# xinfile: An input file in NetCDF format.
# xproduct: The name of a one-dimension variable in xinfile.
# yinfile: An input file in NetCDF format.
# yproduct: The name of a one-dimension variable in yinfile.
#           yproduct shall have the same dimension of xproduct.
#           If not, the result is undetermined.
# outfile: The output file containing a plot of yproduct versus xproduct.
# main: Title.
# xlab: Label of x axis.
# ylab: label of y axis.
#
# keywords: plot, ps2epsi

#============================================================================
# library
library(tools)
#============================================================================

#============================================================================
# Source takuvik.R.
source("takuvik.R")
#============================================================================

#============================================================================
# Constants and parameters.
xinfile <- "../Outputs/AM2006225_ppzbudget_v01_02_02_00.nc"
xproduct <- "pp"
yinfile <- "../Outputs/AM2006225_ppzbudget_v01_02_04_00.nc"
yproduct <- "pp"
outfile <- "../Outputs/1_2_4_0ppz_vs_1_2_2_0ppz.jpg"
main <- "PPz v1_2_4_0 vs PPz v1_2_2_0 on August 13th 2006 above 45 degrees North"
xlab <- "PPz v1_2_2_0 (mgC.m^-2.d^-1)"
ylab <- "PPz v1_2_4_0 (mgC.m^-2.d^-1)"

errmsg <- "Usage:
./compare.R [xinfile xproduct yinfile yproduct outfile main xlab ylab]
xinfile: An input file in NetCDF format.
xproduct: The name of a one-dimension variable in xinfile.
yinfile: An input file in NetCDF format.
yproduct: The name of a one-dimension variable in yinfile.
          yproduct shall have the same dimension of xproduct.
          If not, the result is undetermined.
outfile: The output file containing a plot of yproduct versus xproduct.
main: Title.
xlab: Label of x axis.
ylab: label of y axis.
"
#============================================================================

#============================================================================
# Main.

# Read the arguments from the command line if call_compare.R is
# run from the command line.
args <- commandArgs(TRUE)
length_args <- length(args)
if(length_args == 8){
  xinfile <- args[1]
  xproduct <- args[2]
  yinfile <- args[3]
  yproduct <-args[4]
  outfile <- args[5]
  main <- args[6]
  xlab <- args[7]
  ylab <- args[8]
}else if(length_args != 0){
  cat(errmsg)
}

# Call compare.
ptm <- proc.time()
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
yncfile <- nc_open(yinfile)
array1d_ipix_depth <- ncvar_get(
  nc = yncfile,
  varid = "depth"
)
nc_close(yncfile)
ipixmax <- length(array1d_ipix_xproduct)
# TEST
# ipixmax <- 100000

x <- array1d_ipix_xproduct[1:ipixmax]
y <- array1d_ipix_yproduct[1:ipixmax]
pos <- !is.na(x) & x > 0 & !is.na(y) & y > 0
x <- x[pos]
y <- y[pos]
depth <- array1d_ipix_depth[pos]
min <- min(min(x), min(y))
# max <- max(max(x), max(y))
max <- 1e10
lim <- c(min, max)

pos25 <- depth < 25
x25 <- x[pos25]
y25 <- y[pos25]
pos50 <- 25 < depth & depth < 50
x50 <- x[pos50]
y50 <- y[pos50]
pos75 <- 50 < depth & depth < 75
x75 <- x[pos75]
y75 <- y[pos75]
pos100 <- 75 < depth
x100 <- x[pos100]
y100 <- y[pos100]

# Statistics
# See Bailey and Werdell 2006 in RSE.
log10x <- log10(x)
log10y <- log10(y)
summary <- summary(lm((log10y)~log10x))
ratio <- log10y / log10x
median_ratio <- median(ratio)
q <- quantile(ratio)
q1 <- q[["25%"]]
q3 <- q[["75%"]]
siqr <- (q3 - q1) / 2
pd <- 100 * abs(log10x - log10y) / log10y
mpd <- median(pd)
coef <- summary$coefficients
slope <- coef[2,1]
r2 <- summary$r.squared
rmse <- summary$sigma
n <- length(x)
stat_temp <- c(median_ratio = median_ratio,
               siqr = siqr,
               mpd = mpd,
               slope = slope,
               r2 = r2,
               rmse = rmse,
               n = n)
stat <- stat_temp

dir_outfile <- dirname(outfile)
if(!dir.exists(dir_outfile)){
  dir.create(dir_outfile)
}
ps_file <- paste(
  file_path_sans_ext(outfile),
  ".ps",
  sep = ""
)
postscript(file = ps_file)
plot(
  x = x100,
  y = y100,
  type = "p",
  xlim = lim,
  ylim = lim,
  log = "xy",
  main = main,
  xlab = xlab,
  ylab = ylab,
  col = "black"
)
points(
  x = x75,
  y = y75,
  col = "red"
)
points(
  x = x50,
  y = y50,
  col = "green"
)
points(
  x = x25,
  y = y25,
  col = "blue"
)
abline(
  a = 0,
  b = 1
)
legend(
  "topleft",
  c(
    "Median Ratio (SIQR)",
    "Median % Difference",
    "Slope",
    "r2",
    "RMSE",
    "N",
    "Statistics are on the logarithms.",
    sprintf("%.3f (\u00B1%.3f)", stat['median_ratio'], stat['siqr']),
    sprintf("%.3f", stat['mpd']),
    sprintf("%.3f", stat['slope']),
    sprintf("%.3f", stat['r2']),
    sprintf("%.3f", stat['rmse']),
    stat['n'],
    ""
  ),
  bty = "n",
  ncol = 2
)
legend(
  "bottomright",
  legend = c("bathymetry (m)",
             " 0 - 25",
             "25 - 50",
             "50 - 75",
             "> 75"
  ),
  col = c("white",
          "blue",
          "green",
          "red",
          "black"
  ),
  pch = 1
)

box()
dev.off()

epsi_file <- paste(
  file_path_sans_ext(ps_file),
  ".epsi",
  sep = ""
)

cmd <- paste(
  "ps2epsi",
  " ",
  ps_file,
  " ",
  epsi_file,
  sep = ""
)
cat(cmd)
cat("\n\n")
system(cmd)

cmd <- paste(
  "convert -density 300 -rotate 90",
  " ",
  epsi_file,
  " ",
  outfile,
  sep = ""
)
cat(cmd)
cat("\n\n")
system(cmd)
file.remove(ps_file, epsi_file)

print(proc.time() - ptm)