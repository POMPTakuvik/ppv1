#!/bin/bash

prodfiles=("/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/2006/225/AM2006225_ppz.nc")

titles=("PPz version 1.2.10.1 with MODIS")
bottomrights=("13 August 2006")
products=("pp")
i=0

for prodfile in ${prodfiles[*]}
do
    if [ ! -f ${prodfile} ]
    then
	echo "${prodfile} not found!"
    else
	echo "processing ${prodfile}..."
	#title="$(./get_title.py ${prodfile})"
	title="${titles[i]}"
	echo "title: ${title}"
	#bottomright="$(./get_bottomright.py ${prodfile})"
	bottomright="${bottomrights[i]}"
	echo "bottomright: ${bottomright}"
	product="${products[i]}"
	
	./map.sh "${prodfile}" "${product}" "${title}" "${bottomright}"
	i=$((i+1))
    fi
done
