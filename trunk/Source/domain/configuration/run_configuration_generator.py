INPUT_FILE = "input_file"
VARIABLE = "variable"
OUTPUT_CONFIGURATION = "output_configuration"
VARIABLE_INPUT_BASE_PATH = "variable_input_base_path"

CALCULATION_START_DATE = "calculation_start_date"
CALCULATION_END_DATE = "calculation_end_date"
CALCULATION_TIME_STEP_IN_OFFSET_ALIAS = "calculation_time_step_in_offset_alias"

OUTPUT_PATH_FORMAT = "path_format"
OUTPUT_FILE_NAME_FORMAT = "file_name_format"

import dateutil.parser as parser
from pandas import date_range

from domain.configuration import InputConfiguration, OutputConfiguration

class RunConfigurationGenerator:

    PATH = "path"
    FILE_NAME = "file_name"

    def __init__(self, configuration_file, input_file_factory, variable_factory):
        self.__validate_config_file(configuration_file)

        self.input_file_factory = input_file_factory
        self.variable_factory = variable_factory
        self.input_files = configuration_file.get(INPUT_FILE, {})
        self.variables = configuration_file.get(VARIABLE, {})
        self.output_configuration = configuration_file.get(OUTPUT_CONFIGURATION, {})
        self.calculation_start_date = configuration_file[CALCULATION_START_DATE]
        self.calculation_end_date = configuration_file[CALCULATION_END_DATE]
        self.calculation_time_step_in_offset_alias= configuration_file[CALCULATION_TIME_STEP_IN_OFFSET_ALIAS]

    def get_run_configurations(self):
        input_configurations = self._generate_input_configuration()
        output_configurations = self._generate_output_configuration()

        return zip(input_configurations, output_configurations)

    def _generate_input_configuration(self):
        dates_to_calculate = self._get_dates_to_calculate()
        variables = self.variable_factory.get_variables()
        input_configurations = []

        for current_date in dates_to_calculate:
            input_files_for_current_date = self.input_file_factory.generate_input_file_dictionary_for_one_date(current_date)

            current_input_configuration = self._generate_input_configuration_for_one_date(current_date, input_files_for_current_date, variables)
            input_configurations.append(current_input_configuration)

        return input_configurations

    def _generate_output_configuration(self):

        dates_to_calculate = self._get_dates_to_calculate()
        output_configurations = []
        for current_date in dates_to_calculate:
            output_file_for_current_date = self._resolve_output_configuration(current_date)
            output_path = output_file_for_current_date[self.PATH]
            output_file_name = output_file_for_current_date[self.FILE_NAME]
            current_output_configuration = OutputConfiguration(output_path, output_file_name)
            output_configurations.append(current_output_configuration)

        return output_configurations

    def _resolve_output_configuration(self, date_to_generate):
        year = date_to_generate.year
        day_of_year = date_to_generate.timetuple().tm_yday

        output_configuration = {
            self.PATH: self.output_configuration[OUTPUT_PATH_FORMAT].format(year, day_of_year),
            self.FILE_NAME: self.output_configuration[OUTPUT_FILE_NAME_FORMAT].format(year, day_of_year)
        }

        return output_configuration

    def _get_dates_to_calculate(self):
        calculation_start_date = parser.parse(self.calculation_start_date)
        calculation_end_date = parser.parse(self.calculation_end_date)

        return date_range(calculation_start_date, calculation_end_date, freq=self.calculation_time_step_in_offset_alias)

    def _generate_input_configuration_for_one_date(self, current_date, input_files, variables):
        input_configuration = InputConfiguration(
            current_date,
            input_files,
            variables)
        return input_configuration

    def __validate_config_file(self, configuration_file):
        if CALCULATION_START_DATE not in configuration_file:
            raise ValueError("Configuration file does not include {}".format(CALCULATION_START_DATE))
        if CALCULATION_END_DATE not in configuration_file:
            raise ValueError("Configuration file does not include {}".format(CALCULATION_END_DATE))
        if VARIABLE not in configuration_file:
            raise ValueError("Configuration file does not include {}".format(VARIABLE))
        if INPUT_FILE not in configuration_file:
            raise ValueError("Configuration file does not include {}".format(INPUT_FILE))
