
class InputConfiguration:
    calculation_date = None
    input_files = None

    latitude = None
    longitude = None
    rrs_412 = None
    rrs_443 = None
    rrs_488 = None
    rrs_531 = None
    rrs_555 = None
    rrs_667 = None
    cloud_fraction = None
    taucl = None
    ozone = None
    chlorophyl = None
    rrs_type = None
    primary_production_integration = None
    bathymetry_maximum_depth  = None
    downward_irradiance_table_file_path = None

    def __init__(self, calculation_date, input_files, variables):
        self.calculation_date = calculation_date
        self.input_files = input_files

        try:
            self.latitude = variables['latitude']
            self.longitude = variables['longitude']


            self.rrs_412 = variables['rrs_412']
            self.rrs_443 = variables['rrs_443']
            self.rrs_488 = variables['rrs_488']
            self.rrs_531 = variables['rrs_531']
            self.rrs_555 = variables['rrs_555']
            self.rrs_667 = variables['rrs_667']

            self.cloud_fraction = variables['cloud_fraction']
            self.taucl = variables['taucl']
            self.ozone = variables['ozone']

            self.chlorophyl = variables['chlorophyl']
            self.rrs_type = variables['rrs_type']
            self.primary_production_integration = variables['primary_production_integration']

            self.bathymetry_maximum_depth = variables['bathymetry_maximum_depth']

            self.downward_irradiance_table_file_path = str(input_files['downward_irradiance_table'].file_path)
        except KeyError as exception:
            raise ConfigurationError("{} variable not found in configuration file".format(exception.args[0]))


class ConfigurationError(RuntimeError):
    pass