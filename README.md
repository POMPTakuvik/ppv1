# ppv1
Primary productivity code from Belanger et al. 2013 modified for vertically resolved chl-a.

See [General Specifications](https://goo.gl/7nDb61). Please note that the access will be restricted until publication.

Go to trunk > Source to begin.

# Takuvik primary production model (starter guide)

This document provides general information to quickly start with PPv1.

Faudrait d'ailleurs arreter de caller ca ppv1 pour le commun des mortèles ca ne veut pas dire grand chose!

## Table of Contents

1. [Docker installation](#docker-installation)
2. [Download PPv1 docker](#download-ppv1-docker)
3. [Configure PPv1 input files](#configure-ppv1-input-files)
4. [Run PPv1 docker](#run-ppv1-docker)

## Docker installation (#docker-installation)

PPv1 has been build in a [Docker](https://www.docker.com/) image. The first step is to install Docker on your machine. Please consult [Docker documentation](https://docs.docker.com/install/) to install Docker on your computer.

## Download PPv1 docker

Once Docker is installed, you will need to pull PPv1 image on your machine. At this time, the docker is private and you will need to log on [Docker Hub](https://hub.docker.com/) first.  You will need to ask your system administrator for access granted.

```bash=
docker login
docker pull takuvik/ppv1
```

## Configure PPv1 input files

A JSON configuration file is needed to run PPv1. This file provides information about the user inputs to be used within PPv1.

###  Required variables

`calculation_start_date`: first date to calculate  
`calculation_end_date`: last date to calculate (only one day if `calculation_start_date` == `calculation_start_date`)  
`calculation_time_step_in_offset_alias`: string to specify time step in python [pandas offset](https://pandas.pydata.org/pandas-docs/stable/timeseries.html#timeseries-offset-aliases)  

`input_file`: a dictionary of input files referred in the variable section. 
* `input_file_name`: name of the input file name as referred in the variable section
    * `file_path_template_type`: value to resolve in the path and filename format for each date   (takes one of the following value)
        * `constant_file`: `/.../folder/my_file.csv`
        * `fixed_directory_variable_file_ymd`: `/.../folder/my_file_{yyyy}_{mm}_{dd}.csv`
        * `year_and_day_of_year` : `/.../{yyyy}/{doy}/my_file_{yyyy}_{doy}.csv`
    * `path_format`: base path for each file: ".../folder/{}/{}"
    * `file_name_format` : "data_rimouski_ppv1_{}{}{}.csv"
    * `type`: type of file to load   (takes one of the following value)
        * `netcdf_from_ppv0`: legacy support (ppv0 output)
        * `netcdf_from_bloomstate2`: Output generated by bloomstate script
        * `netcdf_indexed_one_level`: Regular NetCDF, with variables at the root
        * `base`: Loading behavior is explicitly coded by file (avoid usage)
        * `flat_json`: JSON with all values at it's root
        * `csv`: Regular CSV file
    * `details` (optional) : dictionary of special variable to use. Mostly used for passing indexing variable name
        * `{index_variable" : "bin_index"}`

`variable`: dictionnary of all variable to be used (all are mendatory)
* `variable_name` : 
    * `input_file_name`: reference to input_file farther down in the exmaple
    * `column_name`: reference to the column name within the file  
    * `type`: type of value to extract (takes one of the following value)
        * `single_value`: a scalar value (used for boolean etc.)
        * `vector`: a one dimension indexed vector (used with pixel index)
        * `2_dimentions` : a two dimensions indexed matrix (use with pixel index and depth, ex.: Eric R. bloomstate 2)
    * `details` (optional): dictionnary for special variable type.
    


`output_configuration`: a dictionary of values for output
* `path_format`: output equivalent of the input file path format
* `file_name_format`: output equivalent of the input file path format
        
    
###  Example of configuration file (JSON document)
    
```json=
{
    "calculation_start_date":"2015-05-09T00:00:00.000Z",
    "calculation_end_date":"2015-05-09T00:00:00.000Z",
    "calculation_time_step_in_offset_alias":"8D",


    "input_file": {

        "rimouski_all_data": {
            "file_path_template_type": "fixed_directory_variable_file_ymd",
            "file_type": "csv",
            "path_format": "/home/jtbai/Programs/mixed/ppv1/rimouski_data/",
            "file_name_format": "data_rimouski_ppv1_{}{}{}.csv",
            "details":{
                "index_variable" : "bin_index"
            }
        },

        "other_values": {
            "file_path_template_type": "constant_file",
            "file_type": "flat_json",
            "path_format": "/mnt/nfs/output-prod/Takuvik/Teledetection/All/ppv1_configuration_files",
            "file_name_format": "other_values_no_pp_integration.json"
        },
        "downward_irradiance_table": {
            "file_path_template_type": "constant_file",
            "file_type": "base",
            "path_format": "/mnt/nfs/taku-njall/LUTS/",
            "file_name_format": "Ed0moins_LUT_5nm_v2.dat"
        }
    },

    "variable" : {
        "rrs_412" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "NRRS412_intp",
            "type" : "vector"
        },

        "rrs_443" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "NRRS443_intp",
            "type" : "vector"
        },


        "rrs_488" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "NRRS490_intp",
            "type" : "vector"
        },

        "rrs_531" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "NRRS531_intp",
            "type" : "vector"
        },

        "rrs_555" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "NRRS555_intp",
            "type" : "vector"
        },

        "rrs_667" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "NRRS670_intp",
            "type" : "vector"
        },

        "cloud_fraction" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "cf",
            "type" : "vector"
        },

        "taucl" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "cot",
            "type" : "vector"
        },

        "ozone" : {
            "input_file_name": "rimouski_all_data",
            "column_name": "tom",
            "type" : "vector"
        },

        "latitude":{
            "input_file_name": "rimouski_all_data",
            "column_name": "latitude",
            "type" : "vector"
        },

        "longitude":{
            "input_file_name": "rimouski_all_data",
            "column_name": "longitude",
            "type" : "vector"
        },

        "bathymetry_maximum_depth" :{
            "input_file_name": "rimouski_all_data",
            "column_name": "Zbot",
            "type" : "vector"
        },

        "chlorophyl":{
            "input_file_name": "rimouski_all_data",
            "column_name": "CHL1_intp",
            "type" : "vector",
            "details":{
                "type":"surface"
            }
        },

        "primary_production_integration" :{
            "input_file_name": "other_values",
            "column_name": "primary_production_integration",
            "type" : "single_value"
        },

        "rrs_type" :{
            "input_file_name": "other_values",
            "column_name": "rrs_type",
            "type" : "single_value"
        }

    },

    "output_configuration":{
        "path_format":"/mnt/nfs/output-dev/Takuvik/Teledetection/Products/pp/1_2_10_1/{}/{}",
        "file_name_format":"AM{}{}_Rimouski_run_ppv1_final_no_integration.csv"
    }
}
```

## Run PPv1 docker

```bash=
docker run -it [-v section] takuvik/ppv1 [configuration file path]
```
### -v section

docker needs acces to configuration file, input and output path that are stored outside the docker. the -v argument maps [host folder]:[container folder]. These path will highly depend on your configuration file and your computer setup.

#### Access to configuration file

add `-v [folder where your file is]:/takuvik/configuration_file`

#### Acces to input file

add `-v [where on your computer the root of the data source is]:[where the config file will search]`

#### Acces to output file

add `-v [where on your computer the root of the data output is]:[where the configuration file will save the folder search]`

### Docker run command example
```bash=
docker run -it \
-v /home/jtbai/Programs/mixed/ppv1/trunk/Source/configuration_file/:/takuvik/configuration_file \
-v /mnt/nfs/:/mnt/nfs/ \
takuvik/ppv1 configuration_file/dev_run_one_image_with_pp_integration.json 
```

Latest working version:

```bash=
docker run -it \
-v /home/pmassicotte/Desktop/:/takuvik/configuration_file \
-v /mnt/nfs/:/mnt/nfs/ \
ppv1 configuration_file/config_ppz.json
```

#### Command explanation ####
```bash=
Docker run with a terminal and an interactive command 
mapping of configuration_file path 
mapping the input AND output root
[docker image] [target configuration file]
```

## Build PPv1

```bash=
docker build -t ppv1 .
```

## Push PPv1

```bash=
docker push takuvik/ppv1
```

