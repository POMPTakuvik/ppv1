class BaseInputFile:

    input_name = None
    file_path = None
    index_variable = None
    details = None

    def __init__(self, input_name, file_path, details):
        self.input_name = input_name
        self.file_path = file_path
        self.index_variable = details.get('index_variable', None)
        self.details = details

    def __eq__(self, other):
        is_equal = True
        is_equal = is_equal and self.input_name == other.input_name
        is_equal = is_equal and self.file_path == other.file_path
        is_equal = is_equal and self.index_variable == other.index_variable

        return is_equal

    def get_column_value(self, column_name):
        pass