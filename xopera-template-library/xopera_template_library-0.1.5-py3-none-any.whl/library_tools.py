import yaml


class LibraryTools:
    warnings = ""
    conn = None
    user = None

    def write_to_log(self, data):
        self.warnings += data

    def get_warnings_log(self):
        return self.warnings

    def implementation_to_dictionary(self, service_template_path):
        with open(service_template_path, 'r') as stream:
            try:
                template_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return template_dict
