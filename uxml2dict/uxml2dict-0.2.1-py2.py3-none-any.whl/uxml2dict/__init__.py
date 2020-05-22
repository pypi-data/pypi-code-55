"Microapp xmltodict module wrapper"

from typing import Any
from microapp import App
import xmltodict

class Xml2Dict(App):

    _name_ = "uxml2dict"
    _version_ = "0.2.1"
    _description_ = "Microapp xmltodict module wrapper"
    _long_description_ = "Microapp xmltodict module wrapper"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/uxml2dict"

    def __init__(self, mgr):

        self.add_argument("data", help="xml data")
        self.add_argument("-f", dest="xmlfile", action="store_true", help="read xml file")
        self.add_argument("-p", dest="print", action="store_true", help="print xml data")

        self.register_forward("data", type=Any, help="Python dictionary object")

    def perform(self, mgr, args):

        data = args.data["_"]

        if args.xmlfile:

            with open(data) as f:
                data = f.read()

        xml = xmltodict.parse(data)

        if args.print:
            import pprint
            pprint.pprint(xml)

        self.add_forward(data=xml)
