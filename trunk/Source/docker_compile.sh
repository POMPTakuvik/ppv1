##!/bin/bash

current_dir=$(pwd)

docker stop anaconda-ppv1
docker container prune -f

apt-get update
apt-get install make gcc g++ swig -y
pip install netCDF4

docker run --name=anaconda-ppv1 -it -v $current_dir:/home/ -v /Volumes:/Volumes continuumio/anaconda 
docker exec anaconda-ppv1 /bin/bash ./home/make
        


