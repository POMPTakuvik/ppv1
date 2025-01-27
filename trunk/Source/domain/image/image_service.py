import datetime

from domain.configuration import *
from domain.image.image_with_primary_production_pixel import ImageWithPrimaryProductionPixels

CONFIG_FILE_TYPE_ERROR = "Le fichier de configuration n'est pas du type attendu"
class ImageSerice:

    def calculate_primary_production_for_one_day(self, input_configuration):
        print(datetime.datetime.now().time())
        is_configuration_correctly_typed = isinstance(input_configuration, InputConfiguration)

        if is_configuration_correctly_typed:

            print("Constructing image with pixels")
            image = ImageWithPrimaryProductionPixels(input_configuration)
            image.generate_documented_pixels()

            #NO C USAGE UNTIL THIS POINT!
            downward_irradiance_table = ImageWithPrimaryProductionPixels.get_downward_irradiance_table(input_configuration.downward_irradiance_table_file_path)
            image.calculate_pp_for_image(downward_irradiance_table)

            return image
        else:
            raise TypeError(CONFIG_FILE_TYPE_ERROR)


    def save_calculated_primary_production_values(self, primary_production_image, output_configuration):
        is_configuration_correctly_typed = isinstance(output_configuration, OutputConfiguration)

        if is_configuration_correctly_typed :
            print("exporting to {0}...".format(output_configuration.file_name))
            primary_production_image.export_primary_production(output_configuration.file_destination)
        else:
            raise TypeError(CONFIG_FILE_TYPE_ERROR)

        print(datetime.datetime.now().time())

    #
    # image = calculate_primary_production_for_one_day(input_configuration)
    # save_calculated_primary_production_values(image, input_configuration, output_configuration)
