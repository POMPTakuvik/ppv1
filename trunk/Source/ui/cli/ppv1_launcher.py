import argparse
import json

from domain.configuration.run_configuration_generator import RunConfigurationGenerator
from domain.image.image_service import ImageSerice
from domain.input_file.input_file_factory import InputFileFactory
from domain.variable.variable_factory import VariableFactory

argparser = argparse.ArgumentParser()
argparser.add_argument('configuration_file', type=str)
arguments = argparser.parse_args()

configuration_file = arguments.configuration_file
configuration_file_path = configuration_file

laucher_configuration = json.load(open(configuration_file_path, 'r'))
input_file_factory = InputFileFactory(laucher_configuration['input_file'])
variable_factory = VariableFactory(laucher_configuration['variable'])

run_configuration_generator = RunConfigurationGenerator(laucher_configuration, input_file_factory, variable_factory)
image_service = ImageSerice()

for run_configuration in run_configuration_generator.get_run_configurations():
        input_configuration = run_configuration[0]
        output_configuration = run_configuration[1]

        image = image_service.calculate_primary_production_for_one_day(input_configuration)
        image_service.save_calculated_primary_production_values(image, output_configuration)
