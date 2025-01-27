from unittest import TestCase
from datetime import datetime
from dateutil import parser
from mock import Mock, MagicMock
from domain.configuration import InputConfiguration

from domain.image.image_with_primary_production_pixel import ImageWithPrimaryProductionPixels

from domain.variable.base_variable import BaseVariable
from domain.input_file.base_input_file import BaseInputFile
import numpy as np
import pandas as pd

SURFACE_CHLOROPHYLL = "surface"

A_FILE_PATH = "A FILE PATH"


class TestImageWithPrimaryProductionInputs(TestCase):

    A_START_DATE = "2006-08-13T00:00:00.000Z"
    A_END_DATE = "2006-08-14T00:00:00.000Z"

    A_GOOD_CONFIG_FILE = {
        'calculation_start_date': A_START_DATE,
        'calculation_end_date': A_END_DATE,
        'input_files': ["file_1", "file_2", "file_3"],
        'output_configuration': {
            'path_format': "base_path/{}/{}",
            'file_name_format': "base_file_name_{}{}"
        }
    }

    def setUp(self):
        self.mocked_fully_documented_variable = Mock(BaseVariable)
        self.mocked_input_configuration = Mock(InputConfiguration)

    def test_givenSixDataFrameWithOneColumnWithLastItemWithLeastDocumentation_whenJoinVariables_thenCreateADataFrameWithSixColumn(self):
        indexes = np.array([1, 2, 3, 4, 5, 6])
        values = np.power(indexes, 3)

        indexes = pd.Series(indexes)
        indexes.name = 'index'

        dataframe_1 = pd.DataFrame({'band_1': values}, index=indexes)
        dataframe_2 = pd.DataFrame({'band_2': values}, index=indexes)
        dataframe_3 = pd.DataFrame({'band_3': values}, index=indexes)
        dataframe_4 = pd.DataFrame({'band_4': values}, index=indexes)
        dataframe_5 = pd.DataFrame({'band_5': values}, index=indexes)
        dataframe_6 = pd.DataFrame({'band_6': values}, index=indexes)

        self.mocked_fully_documented_variable.get_value_in_file.side_effect = [dataframe_1, dataframe_2, dataframe_3,
                                                                               dataframe_4, dataframe_5, dataframe_6]
        image = ImageWithPrimaryProductionPixels(self.mocked_input_configuration)

        merge_dataframe = image._join_multiple_variables(
            [self.mocked_fully_documented_variable, self.mocked_fully_documented_variable,
             self.mocked_fully_documented_variable, self.mocked_fully_documented_variable,
             self.mocked_fully_documented_variable, self.mocked_fully_documented_variable])

        self.assertEqual(6, len(merge_dataframe.columns))

    def test_givenSixDataFrameWithOneCommonIndexWithFirstItemWithLeastDocumentation_whenJoinVariable_thenGetSixDataFrameWithOnlyOneRow(self):
        indexes = np.array([1, 2, 3, 4, 5, 6])
        values = np.power(indexes, 3)

        indexes = pd.Series(indexes)
        indexes.name = 'index'

        dataframe_6 = pd.DataFrame({'band_6': values}, index=indexes)
        dataframe_2 = pd.DataFrame({'band_2': values}, index=indexes)
        dataframe_3 = pd.DataFrame({'band_3': values}, index=indexes)
        dataframe_4 = pd.DataFrame({'band_4': values}, index=indexes)
        dataframe_5 = pd.DataFrame({'band_5': values}, index=indexes)
        dataframe_1 = pd.DataFrame({'band_1': [1]}, index=[1])
        self.mocked_fully_documented_variable.get_value_in_file.side_effect = [dataframe_1, dataframe_2, dataframe_3,dataframe_4, dataframe_5, dataframe_6]

        image = ImageWithPrimaryProductionPixels(self.mocked_input_configuration)

        merge_dataframe = image._join_multiple_variables(
            [self.mocked_fully_documented_variable, self.mocked_fully_documented_variable,
             self.mocked_fully_documented_variable, self.mocked_fully_documented_variable,
             self.mocked_fully_documented_variable, self.mocked_fully_documented_variable])

        self.assertEqual(1, len(merge_dataframe))

    def test_givenCorrectVariables_whenGenerateDocumentedPixel_thenGetArrayOfFullyDocumentedPixel(self):
        A_START_DATETIME_OBJECT = parser.parse(self.A_START_DATE)
        rrs_type = Mock(BaseVariable)
        rrs_type.get_value_in_file.return_value = 1

        fully_documented_value = np.array([3, 4, 5])
        fully_documented_index = np.array([1, 2, 3])

        latitude = Mock(BaseVariable)
        latitude.get_value_in_file.return_value = pd.DataFrame({'latitude': fully_documented_value}, index=fully_documented_index)
        latitude.name = 'latitude'

        longitude = Mock(BaseVariable)
        longitude.get_value_in_file.return_value = pd.DataFrame({'longitude': fully_documented_value}, index=fully_documented_index)
        longitude.name = 'longitude'

        rrs_412 = Mock(BaseVariable)
        rrs_412.get_value_in_file.return_value = pd.DataFrame({'rrs_412': fully_documented_value}, index=fully_documented_index)
        rrs_412.name = 'rrs_412'

        rrs_443 = Mock(BaseVariable)
        rrs_443.get_value_in_file.return_value = pd.DataFrame({'rrs_443': fully_documented_value}, index=fully_documented_index)
        rrs_443.name = 'rrs_443'

        rrs_488 = Mock(BaseVariable)
        rrs_488.get_value_in_file.return_value = pd.DataFrame({'rrs_488': fully_documented_value}, index=fully_documented_index)
        rrs_488.name = 'rrs_488'

        rrs_531 = Mock(BaseVariable)
        rrs_531.get_value_in_file.return_value = pd.DataFrame({'rrs_531': fully_documented_value}, index=fully_documented_index)
        rrs_531.name = 'rrs_531'

        rrs_555 = Mock(BaseVariable)
        rrs_555.get_value_in_file.return_value = pd.DataFrame({'rrs_555': fully_documented_value}, index=fully_documented_index)
        rrs_555.name = 'rrs_555'

        rrs_667 = Mock(BaseVariable)
        rrs_667.get_value_in_file.return_value = pd.DataFrame({'rrs_667': fully_documented_value}, index=fully_documented_index)
        rrs_667.name = 'rrs_667'

        chlorophyl = Mock(BaseVariable)
        chlorophyl.get_value_in_file.return_value = pd.DataFrame({'chlorophyl': fully_documented_value},index=fully_documented_index)
        chlorophyl.name = 'chlorophyl'
        chlorophyl.details = {'type':SURFACE_CHLOROPHYLL}

        primary_production_integration= Mock(BaseVariable)
        primary_production_integration.get_value_in_file.return_value = 0

        ozone = Mock(BaseVariable)
        ozone.get_value_in_file.return_value = pd.DataFrame({'ozone': fully_documented_value}, index=fully_documented_index)
        ozone.name = 'ozone'

        taucl = Mock(BaseVariable)
        taucl.get_value_in_file.return_value = pd.DataFrame({'taucl': fully_documented_value}, index=fully_documented_index)
        taucl.name = 'taucl'

        cloud_fraction = Mock(BaseVariable)
        cloud_fraction.get_value_in_file.return_value = pd.DataFrame({'cloud_fraction': fully_documented_value}, index=fully_documented_index)
        cloud_fraction.name = 'cloud_fraction'

        depth = Mock(BaseVariable)
        depth.get_value_in_file.return_value = pd.DataFrame({'depth': fully_documented_value}, index=fully_documented_index)
        depth.name = 'depth'

        province = Mock(BaseVariable)
        province.get_value_in_file.return_value = pd.DataFrame({'province': fully_documented_value}, index=fully_documented_index)
        province.name = 'province'

        downward_irradiance_table = Mock(BaseInputFile)

        configuration = InputConfiguration( A_START_DATETIME_OBJECT,{'downward_irradiance_table':downward_irradiance_table}, {'latitude':latitude, 'longitude':longitude, 'rrs_type':rrs_type, 'rrs_412':rrs_412, 'rrs_443':rrs_443, 'rrs_488':rrs_488, 'rrs_531':rrs_531, 'rrs_555':rrs_555, 'rrs_667':rrs_667,
                                                    'chlorophyl':chlorophyl, 'primary_production_integration':primary_production_integration, 'ozone':ozone, 'taucl':taucl, 'cloud_fraction':cloud_fraction, 'bathymetry_maximum_depth':depth})

        self.image_with_primary_production_inputs = ImageWithPrimaryProductionPixels(configuration)

        self.image_with_primary_production_inputs.generate_documented_pixels()

        actual_number_of_pixel_generated = len(self.image_with_primary_production_inputs.pixels)
        expected_number_of_pixel_generated = 3

        self.assertEqual(expected_number_of_pixel_generated, actual_number_of_pixel_generated)

