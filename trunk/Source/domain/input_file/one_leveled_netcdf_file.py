from domain.input_file.base_input_file import BaseInputFile
import numpy as np
import pandas as pd
import netCDF4


class OneLeveledNetCDFFile(BaseInputFile):

    def _get_file_handler(self):
        try:
            file_handler = netCDF4.Dataset(self.file_path, 'r')
        except:
            raise IOError("File not found: {}.".format(self.file_path))

        return file_handler

    def get_column_value(self, column_name):
        print("getting variable: {}".format(column_name))

        file_handler = self._get_file_handler()
        variable_in_netcdf = file_handler.variables

        indexes = variable_in_netcdf[self.index_variable][:]
        values = variable_in_netcdf[column_name][:]

        variable = pd.DataFrame({column_name: values}, index=indexes).dropna()

        print("Obtained {} values".format(variable.shape[0]))
        return variable

