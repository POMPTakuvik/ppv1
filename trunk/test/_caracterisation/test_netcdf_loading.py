from unittest import TestCase

from domain.image.image_with_primary_production_pixel import ImageWater
from domain.input_file.necdf_file_from_ppv0 import NetCDF_2DimentionsFile


class TestNetCDFLoading(TestCase):

    def test_GetArray2dIpixIdepthChl(self):
        input_file = NetCDF_2DimentionsFile('chlorophyl', "/mnt/nfs/output-prod/Takuvik/Teledetection/All/Daily/2006/225/A2006225_chlz_00_04.nc", {'column': "chlz"})

        expected = ImageWater.get_array2d_ipix_idepth_chl(input_file)
        actual = input_file.get_column_value()

        self.assertTrue((actual==expected).all())
