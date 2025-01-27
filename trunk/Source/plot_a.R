#!/usr/bin/env Rscript
#
# File:    plot_a.R
# Author:  Maxime Benoit-Gagne
# Creation: September 19, 2016
#
# Usage:
# ./plot_a.R
#
# keywords: plot, 

#============================================================================
# Constants and parameters.
budget_file <- "out_matsuoka2011.txt"
col.names = c("depth", "aCDM", "aphy", "aw", "at")
default_file <- "out_lee2002.txt"
#============================================================================

read_data <- function(file){
  # read the file
  ll <- scan(
    file = file,
    what = "",
    sep = "\n"
  )
  # Find number of line with the header
  pattern <- "lambda=667"
  b <- grep(
    pattern = pattern,
    x = ll
  )
  b <- b + 1
  # read data
  dat <- read.table(
    file = file,
    header = FALSE,
    col.names = col.names,
    as.is = TRUE,
    skip = b,
    nrows = 101
  )
  off <- which(dat$aCDM == -999)
  dat[off,2 : length(col.names)] <- NA
  dat[,1] <- -dat[,1]
  dat
}
#============================================================================

# main
file <- budget_file
dat_budget <- read_data(
  file = file
)
file <- default_file
dat_default <- read_data(
  file = file
)
max <- max(dat_budget$at, na.rm = TRUE)
min <- min(dat_default[2:length(col.names)], na.rm = TRUE)
min <- min(0, min)
xlim = c(min, max)
main <- c(
  "Absorption coefficients profiles at 68.77 degrees N and -104.88",
  "degrees E on August 13 2006 with PPz budget version 1 and PPz",
  "default version 1"
)
# xlab <- c(
#   "a_i(667); m^-1",
#   "i = CDM, phy, t, w"
# )
xlab <- c(
  expression('a'[i]*'(667); '*'m'^'-1'),
  "i = CDM, phy, t, w"
)
ylab <- "depth; m"
  
pdf(
  file = "/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_1_0/2006/225/a.pdf"
)
par(
  mar = c(8, 4, 7, 2) + 0.1,
  xpd = TRUE
)
plot(
  x = dat_budget$at,
  y = dat_budget$depth,
  type = "l",
  xlim = xlim,
  main = main,
  xlab = xlab,
  ylab = ylab,
  col = "black",
  lty = 1,
  axes = FALSE,
  ann = FALSE
)
lines(
  x = dat_budget$aCDM,
  y = dat_budget$depth,
  col = "black",
  lty = 2
)
lines(
  x = dat_budget$aphy,
  y = dat_budget$depth,
  col = "green",
  lty = 3
)
lines(
  x = dat_budget$aw,
  y = dat_budget$depth,
  col = "blue",
  lty = 1
)
lines(
  x = dat_default$at,
  y = dat_default$depth,
  col = "red",
  lty = 1
)
lines(
  x = dat_default$aCDM,
  y = dat_default$depth,
  col = "red",
  lty = 2
)
axis(
  side = 3
)
axis(
  side = 2
)
title(
  main = c(
    "Absorption coefficients profiles with PPz budget version 1",
    "and PPz default version 1"
  ),
  line = c(5, 4)
)
legend(
  "bottomright",
  inset = c(0, -0.4),
  legend = c(
    "aCDM budget version 1",
    "aCDM default version 1",
    "aphy",
    "at budget version 1",
    "at default version 1",
    "aw"
  ),
  col = c(
    "black",
    "red",
    "green",
    "black",
    "red",
    "blue"
  ),
  lty = c(
    2,
    2,
    1,
    1,
    1,
    1
  )
)
mtext(
  xlab,
  side = 3,
  line = c(3,2)
)
mtext(
  ylab,
  side = 2,
  line = 2
)
mtext(
  text = bquote(
    paste(
      "Coordinates: 68.77",
      degree,
      "N and -104.88",
      degree,
      "E",
      sep = ""
    )
  ),
  side = c(1),
  line = c(0),
  adj = 0,
  cex = 0.75
)
mtext(
  text ="Date: August 13, 2006",
  side = c(1),
  line = c(1),
  adj = 0,
  cex = 0.75
)
box()

dev.off()