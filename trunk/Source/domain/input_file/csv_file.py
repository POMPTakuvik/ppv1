from domain.input_file.base_input_file import BaseInputFile
import pandas as pd


COLUMN = "columns"

class CSVFile(BaseInputFile):

    def _get_file_handler(self):
        try:
            file_handler = pd.read_csv(self.file_path, index_col=self.index_variable)
        except:
            raise IOError("File not found: {}.".format(self.file_path))

        return file_handler

    def get_column_value(self, column_name):
        print("getting variable: {}".format(column_name))
        file_handler = self._get_file_handler()
        variable_in_netcdf = file_handler

        values = variable_in_netcdf[column_name][:]

        variable = pd.DataFrame(values).dropna()
        print("Obtained {} values".format(variable.shape[0]))
        return variable

