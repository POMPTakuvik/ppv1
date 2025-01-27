from domain.variable.vector import Vector
from domain.variable.single_value import SingleValue
from domain.variable.two_dimentions import TwoDimentions
class VariableFactory:

    type_mapping = {
        'vector': Vector,
        'single_value': SingleValue,
        'two_dimentions':TwoDimentions,
    }

    def __init__(self, variable_dictionary_from_configuration):
        self.variable_dictionary = self._generate_variables(variable_dictionary_from_configuration)

    def _generate_variables(self, variable_dictionary_from_configuration):
        variable_dictionary = {}
        for variable_name, variable_details in variable_dictionary_from_configuration.items():
            variable_dictionary[str(variable_name)] = self.type_mapping[variable_details['type']](variable_name, variable_details)

        return variable_dictionary

    def get_variables(self):
        return self.variable_dictionary
