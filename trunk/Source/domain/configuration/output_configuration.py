from os import path, makedirs

class OutputConfiguration:

    file_name = ""
    output_path = ""

    def __init__(self, output_path, file_name):
        self.output_path = str(output_path)
        self.file_name = str(file_name)
        self.file_destination = str(path.join(self.output_path, self.file_name))
        self.create_destination_folder(self.file_destination)

    def create_destination_folder(self, filename):

        if not path.exists(path.dirname(filename)):
            makedirs(path.dirname(filename))

