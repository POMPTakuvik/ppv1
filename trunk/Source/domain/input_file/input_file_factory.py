from domain.input_file.input_file_template.constant_file_path_template import ConstantFilePathTemplate
from domain.input_file.input_file_template.year_and_day_of_year_file_path_template import YearAndDayOfYearFilePathTemplate
from domain.input_file.base_input_file import BaseInputFile
from domain.input_file.csv_file import CSVFile
from domain.input_file.input_file_template.fixed_directory_variable_file_ymd import FixedDirectoryVariableFileYMD
from domain.input_file.necdf_file_from_bloomstate2 import NetCDFFileFromBloostate2
from domain.input_file.necdf_file_from_ppv0 import NetCDFFileFromPPv0
from domain.input_file.one_level_unindex_json import OneLevelJson
from domain.input_file.one_leveled_netcdf_file import OneLeveledNetCDFFile

UNKNOWN_INPUT_NAME = "?"
FILE_PATH_TEMPLATE_TYPE = "file_path_template_type"

class InputFileFactory:

    input_file_path_template_type_mapping = {
        "year_and_day_of_year": YearAndDayOfYearFilePathTemplate,
        "constant_file" : ConstantFilePathTemplate,
        "fixed_directory_variable_file_ymd" : FixedDirectoryVariableFileYMD
    }

    input_file_type_mapping = {
        "netcdf_from_ppv0": NetCDFFileFromPPv0,
        "netcdf_from_bloomstate2": NetCDFFileFromBloostate2,
        "netcdf_indexed_one_level" : OneLeveledNetCDFFile,
        "base": BaseInputFile,
        "flat_json": OneLevelJson,
        "csv" : CSVFile
    }

    def __init__(self, input_file_list_configuration):
        self.file_templates = self._make_file_template(input_file_list_configuration)

    def _make_file_template(self, input_file_configuration_dictionary):
        file_templates = {}
        for input_file_name, input_file_details in input_file_configuration_dictionary.items():
            self.__validate_file_configuration(input_file_details)
            file_template = self.input_file_path_template_type_mapping[input_file_details[FILE_PATH_TEMPLATE_TYPE]](input_file_details)
            file_templates[str(input_file_name)] = file_template

        return file_templates


    def generate_input_file_dictionary_for_one_date(self, date_to_generate):
        input_files = {}
        for current_file_name, current_file_template in self.file_templates.items():
            input_file = self._get_input_file_instance(date_to_generate, current_file_name, current_file_template)
            input_files[current_file_name] = input_file

        return input_files

    def _get_input_file_instance(self, date_to_generate, file_name, file_template):
        input_class = self.input_file_type_mapping[file_template.file_type]
        input_file = input_class(file_name, file_template.generate_file_path(date_to_generate), file_template.details)

        return input_file


    def __validate_file_configuration(self, file_configuration):
        if FILE_PATH_TEMPLATE_TYPE not in file_configuration:
            pass
            raise ValueError("Le type d'intrant n'est pas specifie pour le fichier {}".format(file_configuration.get(ConstantFilePathTemplate.INPUT_NAME, UNKNOWN_INPUT_NAME)))

        if file_configuration[FILE_PATH_TEMPLATE_TYPE] not in self.input_file_path_template_type_mapping:
            pass
            raise ValueError("Type d'intrant inconnu pour le fichier {}".format(file_configuration.get(ConstantFilePathTemplate.INPUT_NAME, UNKNOWN_INPUT_NAME)))
