from microapp import Project

class Meteolab(Project):
    _name_ = "meteolab"
    _version_ = "0.2.1"
    _description_ = "Meteorology Analysis Utilities"
    _long_description_ = "Tools for Analysis of Meteorology data"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/meteolab"

    def __init__(self):
        self.add_argument("--test", help="test argument")
