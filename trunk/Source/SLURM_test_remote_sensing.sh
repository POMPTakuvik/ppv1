#!/bin/bash

#SBATCH -D /home/mabeg99/ppv1/trunk/Source
#SBATCH -J test_remote_sensing
#SBATCH -o test_remote_sensing-%j.out
#SBATCH -c 2
#SBATCH -p ibismini
#SBATCH --mail-type=ALL
#SBATCH --mail-user=maxime.benoit-gagne@takuvik.ulaval.ca
#SBATCH --time=0-00:01
#SBATCH --mem=10240

# Load the software with module if applicable:
module load python/2.7

# Type your command line here
python2 test_remote_sensing.py
