from domain.input_file.input_file_template.input_file_template import InputFileTemplate
import os

class ConstantFilePathTemplate(InputFileTemplate):

    def generate_file_path(self, _):
        return os.path.join(self.path_format, self.file_name_format)
