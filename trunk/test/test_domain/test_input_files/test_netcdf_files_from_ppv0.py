from unittest import TestCase
import datetime

from domain.input_file.input_file_template.year_and_day_of_year_file_path_template import YearAndDayOfYearFilePathTemplate

class TestNetCdfFilesFromPPV0(TestCase):

    A_DATE = datetime.datetime(2008, 12, 18)
    CORRECT_FILE_CONFIGURATION = {
        "input_name":"chrolophylle",
        "path_format": "All/Daily/{}/{}/",
        "file_path_template_type": "",
        "file_name_format":"A{}{}_chlz_00_04.nc"
    }

    def test_givenCorrectInput_whenResolvingVariableFilePath_createCorrectPath(self):
        input_file = YearAndDayOfYearFilePathTemplate(self.CORRECT_FILE_CONFIGURATION)

        variable_path_name = input_file._resolve_variable_path_name(self.A_DATE)

        expected_variable_path_name = "All/Daily/2008/353/"
        self.assertEqual(expected_variable_path_name, variable_path_name)

    def test_givenCorrectInput_whenCreateFileName_createCorrectFileName(self):
        input_file = YearAndDayOfYearFilePathTemplate(self.CORRECT_FILE_CONFIGURATION)

        file_name = input_file._resolve_file_name(self.A_DATE)

        expected_file_name = "A2008353_chlz_00_04.nc"
        self.assertEqual(expected_file_name, file_name)

    def test_givenCorrectInput_whenGenerateFilePath_createCorrectFilePath(self):
        input_file = YearAndDayOfYearFilePathTemplate(self.CORRECT_FILE_CONFIGURATION)

        file_path = input_file.generate_file_path(self.A_DATE)

        expected_file_path = "All/Daily/2008/353/A2008353_chlz_00_04.nc"
        self.assertEqual(expected_file_path, file_path)

