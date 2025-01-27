#!/bin/bash
# file: map.sh
# author: Maxime Benoit-Gagne.
# creation: April 19 2015.
#
# Usage:
# ./map.sh prodfile prodname [title bottomright]
#  where
#  infile:
#   A NetCDF file containing a variable prodname.
#  prodname:
#   A product name.
#   Must be in the set {
#    Nsst
#    pic
#    PP
#    sst_avhrr
#   }
#  title:
#   The title.
#  bottomright:
#   The character string at the bottom right.
# 
# description: Create maps.
# keywords: map.

#=============================================================================
#   constants and parameters
#=============================================================================

bathyfile_input=../Inputs/Province_Zbot_MODISA_L3binV2.nc
region=-180/180/45/90
proj=S-90/90/16c
new_bathyfile=1
# optimization if you already have bathy.grd in the current directory
new_bathyfile=0
bathyfile=bathy

#=============================================================================
#   main program
#=============================================================================

usage=\
"usage:
./map.sh prodfile prodname [title bottomright]
  where
  infile:
   A NetCDF file containing a variable prodname.
  prodname:
   A product name.
   Must be in the set {
    Nsst
    pic
    PP
    sst_avhrr
   }
  title:
   The title.
  bottomright:
   The character string at the bottom right.
"

if [[ $# -eq 2 ]]
then
    filename=${1%.nc}
    prodname=$2
elif [[ $# -eq 4 ]]
then
    filename=${1%.nc}
    prodname=$2
    title=$3
    bottomright=$4
    echo ${title}
    echo ${bottomright}
else
    echo "${usage}"
    exit 1
fi

ppregex='^(pp|PP)'

gmtset \
    COLOR_FOREGROUND darkred \
    COLOR_BACKGROUND black \
    COLOR_NAN pink

# makecpt: Make GMT color palette tables.
# Create a color palette (.cpt) file.
if [[ ${prodname} =~ sst ]]
then
    table=rainbow
    cpt_range=-2/25/0.5
    log=''
elif [[ ${prodname} = "pic" ]]
then
    table=rainbow
    cpt_range=0.00001/0.1/2
    log='-Qo'
elif [[ ${prodname} =~ ${ppregex} ]]
then
    table=rainbow
    cpt_range=10/1000/2
    log='-Qo'
else
    echo "prodname ${prodname} is not supported."
    exit 1
fi
scale=scale.cpt

makecpt -C${table} ${log} -T${cpt_range} -V -Z > ${scale}

# call_NCTakuvik_2_GMT_txt.R
infile=${filename}.nc
outfile=${filename}.gmt
product_name=${prodname}
if [[ ${prodname} = "Nsst" ]]
then
    fill_value='-99'
else
    fill_value='-999'
fi
cmd="Rscript ./call_NCTakuvik_2_GMT_txt.R ${infile} ${outfile} ${product_name} ${fill_value}"
echo "${cmd}"
${cmd}

# xyz2grd: Converting an ASCII or binary table to grid file format.
# Create a grid (.grd) file.
xyzfile=${filename}.gmt
grdfile=${filename}.grd
inc=4.64k

xyz2grd ${xyzfile} -G${grdfile} -I${inc} -R${region} -F -Hi -V

# grdview: Create 3-D perspective grayshaded/colored image or mesh from a 2-D 
# grid file.
# Create a PostScript (ps) file.
relief_file=${filename}.grd
psfile=${filename}.ps

grdview ${relief_file} -J${proj} -C${scale} -K -R${region} -Ts -V > ${psfile}

# pscoast: To plot land-masses, water-masses, coastlines, borders, and rivers.
# Append to the PostScript (ps) file.
boundary_tickmarks=30g30/a10g10
resolution=f
fill=224/186/69

pscoast -J${proj} -R${region} -B${boundary_tickmarks} -D${resolution} \
	-G${fill} -K -O -W \
	>> ${psfile}

pstext -J${proj} -R${region} -K -O -V <<EOF>> ${psfile}
-180 50 12 -90 0 MC 50@+\260@+
-180 60 12 -90 0 MC 60@+\260@+
-180 70 12 -90 0 MC 70@+\260@+
-180 80 12 -90 0 MC 80@+\260@+
EOF

proj_pstext='X16/16'
region_pstext='0/16/0/16'
if [ -n "${title}" ]
then

    # pstext: To plot text strings on maps
    # Append to the PostScript (ps) file.
    echo "8 17.5 14 0 3 CM ${title}" | \
	pstext -J${proj_pstext} -R${region_pstext} -K -O -V -N >> ${psfile}
fi

if [ -n "${bottomright}" ]
then
    # pstext: To plot text strings on maps
    # Append to the PostScript (ps) file.
    echo "16 0. 14 0 3 RB ${bottomright}" | \
	pstext -J${proj_pstext} -R${region_pstext} -K -O -V -N >> ${psfile}
fi

# psscale: Plot gray scale or color scale on maps.
# Append to the PostScript (ps) file.
if [[ ${prodname} =~ sst ]]
then
    annotation=5
    units='@+\260@+C'
elif [[ ${prodname} = "pic" ]]
then
    annotation=''
    units='mol.m@+-3@+'
elif [[ ${prodname} =~ ${ppregex} ]]
then
    annotation=''
    units='mgC.m@+-2@+.d@+-1@+'
else
    annotation=''
    units=''
fi
pos=17c/8c/10c/.35c
colorbar_par="${annotation}:${prodname}:/:${units}:"

if [[ ${annotation} = '' ]]
then
    equalsized=-Li
else
    equalsized=''
fi

psscale -D${pos} -B${colorbar_par} -C${scale} -E ${equalsized} -K -O -V \
	>> ${psfile}

if [[ "${new_bathyfile}" -ne "0" ]]
then

    # call_NCTakuvik_2_GMT_txt.R on bathymetry
    infile=${bathyfile_input}
    outfile=${bathyfile}.gmt
    product_name=Zbot
    fill_value='-9999'
    cmd="Rscript ./call_NCTakuvik_2_GMT_txt.R ${infile} ${outfile} ${product_name} ${fill_value}"
    echo "${cmd}"
    ${cmd}

    # Ascii to binary conversion
    gmtconvert ${bathyfile}.gmt -bo > ${bathyfile}.b

    # gridding of bathymetry using the nearest neighbor method where not
    # documented pixels are stored as NaN
    # nearneighbor: A "Nearest neighbor" gridding algorithm
    xyzfile2=${bathyfile}.b
    gridfile=${bathyfile}.grd
    grid_spacing=5m
    search_radius=40k

    nearneighbor ${xyzfile2} -G${gridfile} -I${grid_spacing} -R${region} \
		 -S${search_radius} -V -bi3
fi

# print the contours of the bottom depth above the map
# grdcontour: Contouring of 2-D gridded data sets
grdfile2=${bathyfile}.grd
cont_int=25
annot_int=50
labels_placement_algo=d
dist=4i
low=-110
high=-15
cut=20000
smoothfactor=200
pen=0.25p,black

grdcontour ${grdfile2} -C${cont_int} -J${proj} -A${annot_int} \
	   -G${labels_placement_algo}${dist} -L${low}/${high} -O -Q${cut} \
	   -R${region} -S${smoothfactor} -V -W${pen} \
	   >> ${psfile}

# ps2raster: Converts one or several PostScript file(s) to other formats using 
# GhostScript.
# Create a JPEG (jpg) file.
ps2raster ${psfile} -A -P -Tj -V

# remove temporary files.
rm ${xyzfile} ${grdfile} ${psfile}
