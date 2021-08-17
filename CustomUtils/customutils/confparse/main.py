import configparser
import os


class Config:  # section and path must not be different, standart setting not
    def __init__(self, section_name, config_path, standart_setting):
        self.path = config_path
        self.section = section_name

        self.standart_config = standart_setting
        self.config = configparser.ConfigParser()

        self.check_config_file()
        self.restrict_config()

    def right_type(self, val: str, type_as=None):
        if type_as is not None:
            try:
                return type_as(val)
            except ValueError:
                pass
        elif val == "0" or val == "1":
            return bool(val)
        return int(val) if val.replace("-", "").isdigit() else val

    def __call__(self, what, type_as=None):
        self.config.read(self.path)

        value = self.config.get(self.section, what)
        if "," in value:
            return list(map(lambda v: self.right_type(v, type_as=type_as), value.split(",")))
        elif type_as is not None:
            try:
                return type_as(value)
            except ValueError:
                pass
        elif value == "0" or value == "1":
            return bool(value)
        return int(value) if value.replace("-", "").isdigit() else value

    def check_config_file(self):
        if not os.path.exists(self.path):
            self.create_config()

    def create_config(self):
        self.config.add_section(self.section)

        for key, val in self.standart_config.items():
            self.config.set(self.section, key, val)

        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def restrict_config(self):
        self.config.read(self.path)

        for key, val in self.standart_config.items():
            try:
                self.config.get(self.section, key)
            except configparser.NoOptionError:
                self.config.set(self.section, key, val)

        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def edit_config(self, setting, value):
        self.config.read(self.path)

        if value is None:
            self.config.remove_option(self.section, setting)
        else:
            if isinstance(value, bool):
                value = str(int(value))
            elif isinstance(value, int):
                value = str(value)
            elif isinstance(value, list):
                value = ",".join(map(lambda i: str(i), value))

            self.config.set(self.section, setting, value)

        with open(self.path, "w") as config_file:
            self.config.write(config_file)
