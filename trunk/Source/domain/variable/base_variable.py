class BaseVariable:

    name = None
    column_name = None
    input_file_name = None
    details = None

    def __init__(self, variable_name,  variable_details):
        self.name = str(variable_name)
        self.column_name = str(variable_details['column_name'])
        self.input_file_name = str(variable_details['input_file_name'])

        # details field usage should be avoided at all cost:
        # It breaks polymorphism usage at higher abstraction levels.
        self.details = variable_details.get('details', {})

    def get_value_in_file(self, input_files_for_one_date):
        raise NotImplemented()
