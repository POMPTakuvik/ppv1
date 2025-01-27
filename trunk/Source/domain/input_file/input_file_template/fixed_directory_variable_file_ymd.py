from domain.input_file.input_file_template.input_file_template import InputFileTemplate
import os


class FixedDirectoryVariableFileYMD(InputFileTemplate):

    def _resolve_file_name(self, date_to_generate):
        year = date_to_generate.year
        month = date_to_generate.month
        day = date_to_generate.day

        return self.file_name_format.format(year, "{0:0>2}".format(month),  "{0:0>2}".format(day))

    def generate_file_path(self, date_to_generate):
        file_path = self.path_format
        file_name = self._resolve_file_name(date_to_generate)

        return os.path.join(file_path, file_name)
