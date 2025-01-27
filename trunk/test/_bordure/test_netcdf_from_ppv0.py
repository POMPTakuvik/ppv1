from unittest import TestCase
from domain.input_file.necdf_file_from_ppv0 import NetCDFFileFromPPv0

class TestNetCDFLoading(TestCase):
    A_FILE_PATH = "/mnt/nfs/output-dev/Takuvik/Teledetection/Couleur/SORTIES/36_0_0/NOCLIM/2006/225/AM2006225_PP.nc"

    def setUp(self):
        self.file_to_test = NetCDFFileFromPPv0('rrs', self.A_FILE_PATH, None)

    def test_whenGetVariable_thenGetIndexedVariable(self):
        variable = self.file_to_test.get_column_value('Rrs412')
        print(variable)