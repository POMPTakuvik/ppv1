#!/bin/bash

#SBATCH -D /home/mabeg99/ppv1/trunk/Source
#SBATCH -J run_all
#SBATCH -o run_all-%j.out
#SBATCH -c 1
#SBATCH -p ibismini
#SBATCH --mail-type=ALL
#SBATCH --mail-user=maxime.benoit-gagne@takuvik.ulaval.ca
#SBATCH --time=21-00:00
#SBATCH --mem=102400

# Load the software with module if applicable:
module load python/2.7

# Type your command line here
#bash run_all.sh

# Development and test. Inputs on outpud-prod and outputs on output-dev.

python2 write_outfiles_from_to.py \
	--grid_file="../Inputs/A45N.nc" \
	--rrs_type="A" \
	--rrs_first_file="/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2015/037/AM2015037_PP.nc" \
	--rrs_last_file="/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2015/037/AM2015037_PP.nc" \
	--chl_first_file="/Volumes/output-prod/Takuvik/Teledetection/All/Daily/2015/037/A2015037_chlz_00_05.nc" \
	--chl_last_file="/Volumes/output-prod/Takuvik/Teledetection/All/Daily/2015/037/A2015037_chlz_00_05.nc" \
	--atm_first_file="/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2015/037/AM2015037_PP.nc" \
	--atm_last_file="/Volumes/output-prod/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2015/037/AM2015037_PP.nc" \
	--lut_ed0minus_file="../Inputs/Ed0moins_LUT.dat" \
	--geospatial_file="../Inputs/Province_Zbot_MODISA_L3binV2.nc" \
	--chl="column" \
	--first_outfile="/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/2015/037/AM2015037_ppz.nc" \
	--last_outfile="/Volumes/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/2015/037/AM2015037_ppz.nc"
