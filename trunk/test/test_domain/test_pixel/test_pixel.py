import numpy as np

from unittest import TestCase
from domain.pixel.pixel import Pixel

SURFACE_CHLOROPHYLL = "surface"

VERTICAL_PROFILE = "vertical_profile"


class TestPixel(TestCase):

    A_LATITUDE = 0
    A_LONGITUDE = 0
    A_DOM = 12
    A_MONTH = 8
    A_YEAR = 2006
    A_DOY = 225

    A_CHLOROPHYLL_VALUE_ARRAY = np.array(range(Pixel.NDEPTHS))
    A_PRIMARY_PRODUCTION_VALUE_ARRAY = np.array(range(Pixel.NDEPTHS))

    def test_givenSurfaceChlorophyll_whenLoadChlorophyll_thenLoadVectorOfOnlyOneValueAndZeros(self):
        pixel = Pixel(self.A_LATITUDE, self.A_LONGITUDE, self.A_YEAR, self.A_MONTH, self.A_DOM, self.A_DOY, 0)

        chlorophyll_type = SURFACE_CHLOROPHYLL
        pixel.load_chl(chlorophyll_type=chlorophyll_type, chl_by_pixel=self.A_CHLOROPHYLL_VALUE_ARRAY)

        self.assertEqual(pixel.array1d_idepth_chl[0], self.A_CHLOROPHYLL_VALUE_ARRAY [0])
        self.assertEqual(pixel.array1d_idepth_chl[1], 0)
        self.assertEqual(pixel.array1d_idepth_chl[-1], 0)
        self.assertEqual(len(pixel.array1d_idepth_chl), len(self.A_CHLOROPHYLL_VALUE_ARRAY))

    def test_givenChlorophyllProfile_whenLoadChlorophyll_thenLoadCompleteVector(self):
        pixel = Pixel(self.A_LATITUDE, self.A_LONGITUDE, self.A_YEAR, self.A_MONTH, self.A_DOM, self.A_DOY, 0)

        chlorophyll_type = VERTICAL_PROFILE
        pixel.load_chl(chlorophyll_type=chlorophyll_type, chl_by_pixel=self.A_CHLOROPHYLL_VALUE_ARRAY)
        self.assertEqual(pixel.array1d_idepth_chl[0], self.A_CHLOROPHYLL_VALUE_ARRAY[0])
        self.assertEqual(pixel.array1d_idepth_chl[1], self.A_CHLOROPHYLL_VALUE_ARRAY[1])
        self.assertEqual(pixel.array1d_idepth_chl[-1], self.A_CHLOROPHYLL_VALUE_ARRAY[-1])
        self.assertEqual(len(pixel.array1d_idepth_chl), len(self.A_CHLOROPHYLL_VALUE_ARRAY))

    def test_givenSurfaceChlorophyll_whenGetPP_thenGetOnlyFirstValue(self):
        pixel = Pixel(self.A_LATITUDE, self.A_LONGITUDE, self.A_YEAR, self.A_MONTH, self.A_DOM, self.A_DOY, 0)

        actual_primary_production = pixel._calculate_output_pp(primary_production_integration=False, primary_production_by_depth=self.A_PRIMARY_PRODUCTION_VALUE_ARRAY)

        expected_primary_production = np.sum(self.A_PRIMARY_PRODUCTION_VALUE_ARRAY[0])
        self.assertEqual(actual_primary_production, expected_primary_production)

    def test_givenSurfaceChlorophyll_whenGetPP_thenSumAllValues(self):
        pixel = Pixel(self.A_LATITUDE, self.A_LONGITUDE, self.A_YEAR, self.A_MONTH, self.A_DOM, self.A_DOY, 0)

        actual_primary_production = pixel._calculate_output_pp(primary_production_integration=True, primary_production_by_depth=self.A_PRIMARY_PRODUCTION_VALUE_ARRAY)

        expected_primary_production = np.sum(self.A_PRIMARY_PRODUCTION_VALUE_ARRAY)
        self.assertEqual(actual_primary_production, expected_primary_production )

