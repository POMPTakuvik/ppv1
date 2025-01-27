from domain.input_file.base_input_file import BaseInputFile
import numpy as np
import pandas as pd
import netCDF4

COLUMN = "column"

class NetCDFFileFromBloostate2(BaseInputFile):

    DEFAULT_VALUE = -999
    IBIN45N_OFFSET = 20281863
    INDEX_NAME = 'ibin'

    def __init__(self, input_name, file_path, index_variable):
        BaseInputFile.__init__(self, input_name, file_path, index_variable)


    def _get_file_handler(self):
        try:
            file_handler = netCDF4.Dataset(self.file_path, 'r')
        except:
            raise IOError("File not found: {}.".format(self.file_path))

        return file_handler

    def get_column_value(self, column_name):
        print("getting variable: {}".format(column_name))
        file_handler = self._get_file_handler()
        variable_in_netcdf = file_handler.variables[column_name]

        value = variable_in_netcdf[:]
        one_based_grid_index = np.array(range(len(value)))+1
        offsetted_one_based_grid_index = one_based_grid_index + NetCDFFileFromBloostate2.IBIN45N_OFFSET
        documented_indexes = offsetted_one_based_grid_index [value[:,0]> NetCDFFileFromBloostate2.DEFAULT_VALUE]
        documented_values = value[value[:,0]> NetCDFFileFromBloostate2.DEFAULT_VALUE]

        variable = pd.DataFrame(documented_values, index=documented_indexes)

        variable.index.names = [self.INDEX_NAME]
        print("Obtained {} values".format(variable.shape[0]))
        return variable