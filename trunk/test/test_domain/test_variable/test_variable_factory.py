from unittest import TestCase

from domain.variable.variable_factory import VariableFactory
from domain.variable.vector import Vector

class TestVariableFactory(TestCase):

    A_VARIABLE_DICTIONARY_WITH_VECTOR_TYPE = {
        'a_variable_name': {
            'input_file_name': 'a_file_name',
            'column_name': 'a_variable_column_3',
            'type':'vector'
        }
    }

    def test_givenConfigurationFileWithVariableTypeVector_whenInit_thenVariableIsVectorType(self):
        variable_factory = VariableFactory(self.A_VARIABLE_DICTIONARY_WITH_VECTOR_TYPE)
        variables = variable_factory.get_variables()

        self.assertIsInstance(variables['a_variable_name'], Vector)