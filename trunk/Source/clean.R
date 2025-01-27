#!/usr/bin/env Rscript
# Author: Maxime Benoit-Gagne
# Creation: August 30 2016
#
# usage:
# Rscript clean.R

file <- 'pp.txt'
txt <- readLines(
  con = file
)

# Keep only lines n-100 to n-1
nlines <- length(txt)
first_line <- nlines - 100
last_line <- nlines - 1
txt2 <- txt[first_line:last_line]

# Keep only the pp.
pattern <- '.*:\ '
replacement <- ''
txt3 <- gsub(
  pattern = pattern,
  replacement = replacement,
  x = txt2
)
pattern <- '\ $'
replacement <- ''
txt4 <- gsub(
  pattern = pattern,
  replacement = replacement,
  x = txt3
)
cat(
  txt4,
  file = 'newpp.txt',
  sep = ','
)