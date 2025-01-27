#!/usr/bin/env python2

"""Classes useful for remote sensing scripts.
"""

# author: Maxime Benoit-Gagne - Takuvik - Canada.
# date of creation: November 6, 2015.
#
# Python from Anaconda.
#
# Interpreter:
# $ python
# Python 2.7.10 |Anaconda 2.4.0 (x86_64)| (default, Oct 19 2015, 18:31:17) 
# [GCC 4.2.1 (Apple Inc. build 5577)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# Anaconda is brought to you by Continuum Analytics.
# Please check out: http://continuum.io/thanks and https://anaconda.org
#
# See svn/Takuvik/Teledetection/SOP/Python/Python2/Python2Anaconda.docx
# to install Python from Anaconda and netCDF4.

########### Importing modules ###########
import numpy as np
import os
import os.path

import light
import datetime

import pandas as pd
from domain.pixel.pixel import Pixel
from domain.constants import *

PIXEL_INDEX_KEY = 'ipix'

LOG_PIXEL_STEP = 10000
########### classes ###########

class ImageWithPrimaryProductionPixels(object):

    def __init__(self, input_configuration):

        self.date_to_compute = input_configuration.calculation_date
        self.input_files = input_configuration.input_files
        self.rrs_type = input_configuration.rrs_type
        self.latitude = input_configuration.latitude
        self.longitude = input_configuration.longitude

        self.rrs_412 = input_configuration.rrs_412
        self.rrs_443 = input_configuration.rrs_443
        self.rrs_488 = input_configuration.rrs_488
        self.rrs_531 = input_configuration.rrs_531
        self.rrs_555 = input_configuration.rrs_555
        self.rrs_667 = input_configuration.rrs_667
        self.chlorophyl = input_configuration.chlorophyl
        self.primary_production_integration = input_configuration.primary_production_integration
        self.ozone = input_configuration.ozone
        self.taucl = input_configuration.taucl
        self.cloud_fraction = input_configuration.cloud_fraction
        self.bathymetry_maximum_depth = input_configuration.bathymetry_maximum_depth

        self.pixels = []

    def generate_documented_pixels(self):
        variable_dataframe = self._get_joined_satellite_data()

        run_rrs = self.rrs_type.get_value_in_file(self.input_files)
        chlorophyl_matrix = self.chlorophyl.get_value_in_file(self.input_files)
        chlorophyl_type = self.chlorophyl.details['type']
        self.primary_production_integration = self.primary_production_integration.get_value_in_file(self.input_files)

        pixel_number = 0
        number_of_pixel_to_calculate = variable_dataframe.shape[0]

        for pixel_index, variables in variable_dataframe.iterrows():
            dom, month, year, doy = ImageWithPrimaryProductionPixels.convert_datetime_in_dom_month_year_doy(self.date_to_compute)

            pixel = Pixel(variables[self.latitude.name], variables[self.longitude.name], year, month, dom, doy, pixel_index)
            pixel.load_rrs_type(run_rrs)
            pixel.load_rrs(variables[[self.rrs_412.name, self.rrs_443.name, self.rrs_488.name, self.rrs_531.name, self.rrs_555.name, self.rrs_667.name]])
            pixel.load_chl(chlorophyl_type, chlorophyl_matrix.loc[pixel_index])
            pixel.load_cloud_fraction(variables[self.cloud_fraction.name])
            pixel.load_ozone(variables[self.ozone.name])
            pixel.load_taucl(variables[self.taucl.name])
            pixel.load_depth(variables[self.bathymetry_maximum_depth.name]) # Depth is positive downward
            self.pixels.append(pixel)

            if pixel_number % LOG_PIXEL_STEP == 0:
                print("processing pixel {} : {}/{}...".format(pixel.ibin45N, pixel_number, number_of_pixel_to_calculate))


            pixel_number += 1


    def _get_joined_satellite_data(self):
        satelite_data = [self.latitude, self.longitude, self.rrs_412, self.rrs_443, self.rrs_488, self.rrs_531,
                         self.rrs_555, self.rrs_667, self.chlorophyl, self.ozone, self.taucl, self.cloud_fraction,
                         self.bathymetry_maximum_depth]
        variable_dataframe = self._join_multiple_variables(satelite_data)
        return variable_dataframe

    @staticmethod
    def convert_datetime_in_dom_month_year_doy(datetime_object):
        dom = datetime_object.day
        month = datetime_object.month
        year = datetime_object.year
        doy = datetime_object.timetuple().tm_yday

        return dom, month, year, doy

    def _join_multiple_variables(self, variables):
        joined_dataframe = None
        for variable in variables:
            if joined_dataframe is None:
                joined_dataframe = pd.DataFrame(variable.get_value_in_file(self.input_files))
            else:
                dataframe_to_add = variable.get_value_in_file(self.input_files)
                joined_dataframe = joined_dataframe.join(dataframe_to_add, how='inner')
            print("Output data frame has {} complete lines".format(joined_dataframe.shape[0]))
        return joined_dataframe

    def calculate_pp_for_image(self, downward_irradiance_table):

        print("Calculating PP")
        number_of_pixel_to_calculate = len(self.pixels)

        for pixel_index, pixel in enumerate(self.pixels):

            if pixel_index % LOG_PIXEL_STEP == 0:
                print("processing pixel {} : {}/{}...".format(pixel.ibin45N, pixel_index, number_of_pixel_to_calculate))

            # pixel.dump()
            pixel.calculate_pp(self.primary_production_integration, downward_irradiance_table)
        print("Done processing calculating primary production")

    def create_variable_in_output_file(self, output_file):
        pass

    def export_primary_production(self, filename):
        #The value are recalled at the time of saving so they don't stay in memory
        #for the whole calculation time...
        satellite_data = self._get_joined_satellite_data()

        number_of_pixels = len(self.pixels)
        primary_production = np.array(range(number_of_pixels), np.double)
        for pixel_index, pixel in enumerate(self.pixels):
            primary_production[pixel_index] = pixel.pp

        primary_production_dataframe = pd.DataFrame({'primary_production':primary_production}, index=satellite_data.index)
        output_data_frame = satellite_data.join(primary_production_dataframe,how='inner')

        # To generalize the output mapping, do not hack the file name here.
        # Split input file factory and reuse the file template object generation to create
        # object that can file path by using a date in a configurable behavior.
        # When this is done, remove this comment.

        output_data_frame.to_csv(filename)
        print(datetime.datetime.now().time())

    @staticmethod
    def get_downward_irradiance_table(filename):

        if(not os.path.isfile(filename)):
            raise IOError("File not found: {}".format(filename))
        downward_irradiance_table = np.zeros(shape = (light.NBWL,
                                light.NTHETAS,
                                light.NO3,
                                light.NTAUCLD,
                                light.NALB),
                       dtype = np.float32)
        print(downward_irradiance_table.shape)
        light.get_downward_irradiance_table(filename, downward_irradiance_table)
        return downward_irradiance_table

