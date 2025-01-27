from domain.input_file.input_file_template.input_file_template import InputFileTemplate
import os

class YearAndDayOfYearFilePathTemplate(InputFileTemplate):

    def _resolve_variable_path_name(self, date_to_generate):
        year = date_to_generate.year
        day_of_year = "{:03}".format(date_to_generate.timetuple().tm_yday)

        return self.path_format.format(year, day_of_year)

    def _resolve_file_name(self, date_to_generate):
        year = date_to_generate.year
        day_of_year = "{:03}".format(date_to_generate.timetuple().tm_yday)

        return self.file_name_format.format(year, day_of_year)

    def generate_file_path(self, date_to_generate):
        file_path = self._resolve_variable_path_name(date_to_generate)
        file_name = self._resolve_file_name(date_to_generate)

        return os.path.join(file_path, file_name)

