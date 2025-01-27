from domain.input_file.base_input_file import BaseInputFile
import pandas as pd
from json import load

COLUMN = "column"

class OneLevelJson(BaseInputFile):


    def __init__(self, input_name, file_path, index_variable):
        BaseInputFile.__init__(self, input_name, file_path, index_variable)


    def _get_file_handler(self):
        try:
            file_handler = load(open(self.file_path, 'r'))
        except:
            raise IOError("File not found: {}.".format(self.file_path))

        return file_handler

    def get_column_value(self, column_name):
        file_handler = self._get_file_handler()
        variable_in_json = file_handler[column_name]
        variable = variable_in_json

        return variable
