from domain.variable.base_variable import BaseVariable

class TwoDimentions(BaseVariable):

    def get_value_in_file(self, input_files_for_one_date):
        input_file = input_files_for_one_date[self.input_file_name]
        value = input_file.get_column_value(self.column_name)

        value.columns = [self.name + "_" + str(x) for x in range(len(value.columns))]
        return value