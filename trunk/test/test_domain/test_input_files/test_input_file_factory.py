from unittest import TestCase
from datetime import datetime

from domain.input_file.input_file_factory import InputFileFactory
from domain.input_file.input_file_template.year_and_day_of_year_file_path_template import YearAndDayOfYearFilePathTemplate
from domain.input_file.base_input_file import BaseInputFile


class TestInputFileFactory(TestCase):

    A_DATE = datetime(2008, 12, 18)

    A_CORRECT_FILE_CONFIGURATION = {"a_file_name":
        {
            "file_path_template_type" : "year_and_day_of_year",
            "file_type": "base"
        }
    }

    AN_INCORRECT_FILE_CONFIGURATION_MISSING_TYPE = {"a_file_name":{
        }}

    AN_INCORRECT_FILE_CONFIGURATION_WRONG_TYPE = {"a_file_name":{
        "file_path_template_type": "wrong_input_type"
    }}

    def setUp(self):
        self.input_file_factory = InputFileFactory(self.A_CORRECT_FILE_CONFIGURATION)

    def test_givenKnownInputType_whenMakeFileTemplate_thenCreateCorrectFileTemplate(self):
        file_template = self.input_file_factory._make_file_template(self.A_CORRECT_FILE_CONFIGURATION)

        self.assertIsInstance(file_template.values()[0], YearAndDayOfYearFilePathTemplate)

    def test_givenFileConfigurationMissingFileType_whenMakeFileTemplate_thenRaiseValueError(self):
        with self.assertRaises(ValueError):
            self.input_file_factory._make_file_template(self.AN_INCORRECT_FILE_CONFIGURATION_MISSING_TYPE)

    def test_givenFileConfigurationWithWrongFileType_whenMakeFileTemplate_thenRaiseValueError(self):
        with self.assertRaises(ValueError):
            self.input_file_factory._make_file_template(self.AN_INCORRECT_FILE_CONFIGURATION_WRONG_TYPE)

    def test_givenCorrectConfiguration_whenGenerateInputForOneDate_thenGenerateInputFile(self):
        input_file = self.input_file_factory.generate_input_file_dictionary_for_one_date(self.A_DATE)

        expected_file = BaseInputFile('a_file_name', '', {})
        self.assertEqual(expected_file, input_file['a_file_name'])

    def test_givenOneFile_whenMakeFileTemplate_thenCreateOneFileTemplate(self):
        file_templates = self.input_file_factory._make_file_template(self.A_CORRECT_FILE_CONFIGURATION)

        self.assertIsInstance(file_templates, dict)
        self.assertEqual(len(self.A_CORRECT_FILE_CONFIGURATION), len(file_templates))
