from dateutil import parser
from unittest import TestCase

from mock import Mock

from domain.configuration import InputConfiguration, OutputConfiguration
from domain.configuration.run_configuration_generator import RunConfigurationGenerator
from domain.input_file.input_file_factory import InputFileFactory
from domain.input_file.base_input_file import BaseInputFile
from domain.variable.variable_factory import VariableFactory



class TestMultipleDaysLauncher(TestCase):

    A_START_DATE = "2006-08-13T00:00:00.000Z"
    A_END_DATE = "2006-08-14T00:00:00.000Z"
    A_END_DATE_10_DAYS_LAYER = "2006-08-23T00:00:00.000Z"
    DAILY_OFFSET = "D"
    EIGHT_DAY_OFFSET = "8D"

    A_GOOD_CONFIG_FILE = {
        'calculation_start_date': A_START_DATE,
        'calculation_end_date': A_END_DATE,
        "calculation_time_step_in_offset_alias" : DAILY_OFFSET,
        'input_file': ["file_1", "file_2", "file_3"],
        'variable': {"var_1": {'details': True}, "var_2": {'details': True}},

        'output_configuration': {
            'path_format': "base_path/{}/{}",
            'file_name_format': "base_file_name_{}{}"
        }
    }

    A_CONFIG_FILE_FOR_10_DAYS_PERIOD_AND_8_DAYS_SKIP = {
        'calculation_start_date': A_START_DATE,
        'calculation_end_date': A_END_DATE_10_DAYS_LAYER,
        "calculation_time_step_in_offset_alias" : EIGHT_DAY_OFFSET,
        'input_file': ["file_1", "file_2", "file_3"],
        'variable': {"var_1": {'details': True}, "var_2": {'details': True}},

        'output_configuration': {
            'path_format': "base_path/{}/{}",
            'file_name_format': "base_file_name_{}{}"
        }
    }

    A_GOOD_INPUT_FILE_DICTIONNARY = {
        'grid': BaseInputFile('grid', '', {}),
        'rrs': BaseInputFile('rrs', '', {}),
        'chlorophyl': BaseInputFile('chlorophyl', '', {}),
        'atmosphere': BaseInputFile('atmosphere', '', {}),
        'downward_irradiance_table': BaseInputFile('downward_irradiance_table', '', {}),
        'geospatial': BaseInputFile('geospatial', '', {})
    }

    A_BAD_CONFIG_FILE = {
        'useless_field': None
    }

    def setUp(self):
        self.mocked_input_file_factory = Mock(InputFileFactory)
        self.mocked_input_file_factory.generate_input_file_dictionary_for_one_date.return_value = self.A_GOOD_INPUT_FILE_DICTIONNARY
        self.mocked_variable_factory = Mock(VariableFactory)
        self.mocked_variable_factory.get_variables.return_value = {
            'latitude': True,
            'longitude': True,
            'rrs_412': True,
            'rrs_443': True,
            'rrs_488': True,
            'rrs_531': True,
            'rrs_555': True,
            'rrs_667': True,
            'taucl': True,
            'ozone': True,
            'cloud_fraction': True,
            'chlorophyl': True,
            'primary_production_integration': True,
            'rrs_type': True,
            'bathymetry_maximum_depth': True,
            'province': True
        }

        self.launcher = RunConfigurationGenerator(self.A_GOOD_CONFIG_FILE, self.mocked_input_file_factory, self.mocked_variable_factory)

    def test_givenConfigFileWithMissingFields_whenInitialise_thenThrowError(self):
        with self.assertRaises(ValueError):
            RunConfigurationGenerator(self.A_BAD_CONFIG_FILE, self.mocked_input_file_factory, self.mocked_variable_factory)

    def test_givenCorrectConfigFile_whenInitialise_thenNoError(self):
        self.assertIsInstance(self.launcher, RunConfigurationGenerator)

    def test_givenMultipleDaysToCompute_whenGetDaysToCalculate_thenGetArraysOfDays(self):
        days_to_calculate = self.launcher._get_dates_to_calculate()

        expected_days = [parser.parse(self.A_START_DATE), parser.parse(self.A_END_DATE)]
        self.assertListEqual(expected_days, list(days_to_calculate))

    def test_givenConfigWithNDays_whenGeneratingInputFiles_thenCallFactoryNTimes(self):
        self.launcher._generate_input_configuration()

        number_of_expected_input_dictionary = len(self.launcher._get_dates_to_calculate())
        self.assertEqual(self.mocked_input_file_factory.generate_input_file_dictionary_for_one_date.call_count, number_of_expected_input_dictionary)

    def test_givenConfigWith8DaysTimeStep_whenGetDaysToCalculate_thenGetArrayOfDaysThatAre8DaysApart(self):
        launcher = RunConfigurationGenerator(self.A_CONFIG_FILE_FOR_10_DAYS_PERIOD_AND_8_DAYS_SKIP, self.mocked_input_file_factory, self.mocked_variable_factory)
        calculation_dates =launcher._get_dates_to_calculate()

        timedelta_between_two_first_calculation_dates = calculation_dates[1]-calculation_dates[0]
        self.assertEqual(8, timedelta_between_two_first_calculation_dates.days)

    def test_givenConfigWith8DaysTimeStepAndEndDateThatDoesNotFit_whenGetDaysToCalculate_thenGetArrayOfDatesThatFitBetweenTheEndPoints(self):
        launcher = RunConfigurationGenerator(self.A_CONFIG_FILE_FOR_10_DAYS_PERIOD_AND_8_DAYS_SKIP, self.mocked_input_file_factory, self.mocked_variable_factory)
        calculation_dates = launcher._get_dates_to_calculate()

        self.assertEqual(2, len(calculation_dates))

    def test_givenConfigurationFileWithNDays_whenGenerateInputonfig_thenGenerateNInputConfig(self):
        input_configuration = self.launcher._generate_input_configuration()

        number_of_expected_input = len(self.launcher._get_dates_to_calculate())
        self.assertEqual(number_of_expected_input, len(input_configuration))

    def test_givenCorrectConfigurationFile_whenResolveOutputFilePath_thenResolveCorrectFilePath(self):
        current_date = parser.parse(self.A_START_DATE)
        file_output = self.launcher._resolve_output_configuration(current_date)

        expected_output_configuration = {'path': "base_path/2006/225", "file_name": "base_file_name_2006225"}
        self.assertDictEqual(expected_output_configuration, file_output)

    def test_givenConfigurationFileWithNDays_whenGenerateOutputConfig_thenGenerateNOutputConfig(self):
        output_configurations = self.launcher._generate_output_configuration()

        number_of_expected_output = len(self.launcher._get_dates_to_calculate())
        self.assertEqual(number_of_expected_output, len(output_configurations))

    def test_givenConfigurationFileWithNDays_whenGeneratingRunConfigurations_thenGenerateNTuplesofInputOutput(self):
        run_configurations = self.launcher.get_run_configurations()

        number_of_expected_run_configuration = len(self.launcher._get_dates_to_calculate())
        self.assertEqual(number_of_expected_run_configuration, len(run_configurations))
        self.assertIsInstance(run_configurations[0][0], InputConfiguration)
        self.assertIsInstance(run_configurations[0][1], OutputConfiguration)


