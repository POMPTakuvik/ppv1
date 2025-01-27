class InputFileTemplate:
    INPUT_NAME = "input_name"
    FILE_NAME_FORMAT = "file_name_format"
    VARIABLE_PATH_FORMAT = "path_format"

    INPUT_FILE_FULL_PATH = "full_path"
    INPUT_FILE_DETAILS = "details"
    FILE_TYPE = "file_type"

    name = ""
    path_format = ""
    file_name_format = ""
    details = []

    def __init__(self, file_configuration):
        self._validate_file_configuration(file_configuration)

        self.name = file_configuration.get(self.INPUT_NAME)

        self.path_format = file_configuration.get(self.VARIABLE_PATH_FORMAT, "")
        self.file_name_format = file_configuration.get(self.FILE_NAME_FORMAT, "")

        self.details = file_configuration.get(self.INPUT_FILE_DETAILS, {})
        self.file_type = file_configuration.get(self.FILE_TYPE, "")

    def generate_file_path(self, date_to_generate):
        pass

    def _validate_file_configuration(self, configuration_file):
        pass