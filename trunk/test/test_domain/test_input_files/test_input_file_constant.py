from unittest import TestCase
import datetime

from domain.input_file.input_file_template.constant_file_path_template import ConstantFilePathTemplate

class TestNetCdfFilesFromPPV0(TestCase):

    A_DATE = datetime.datetime(2008, 12, 18)

    CORRECT_FILE_CONFIGURATION = {
        "input_name":"chrolophylle",
        "path_format": "All/Daily/12/41/",
        "input_file_type": "",
        "file_name_format": "A1241_chlz_00_04.nc"
    }

    def test_givenCorrectInput_whenGenerateFilePath_createCorrectFilePath(self):
        input_file = ConstantFilePathTemplate(self.CORRECT_FILE_CONFIGURATION)

        file_path = input_file.generate_file_path(self.A_DATE)

        expected_file_path = "All/Daily/12/41/A1241_chlz_00_04.nc"
        self.assertEqual(expected_file_path, file_path)
