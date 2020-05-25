import configparser
import os

from shield34_reporter.consts.shield34_properties_constants import Shield34PropertiesConstants
from shield34_reporter.exceptions import Shield34PropertiesFileNotFoundException, Shield34PropertiesSyntaxIncorrect
from shield34_reporter.utils.file_handler import FileHandler
from shield34_reporter.utils.logger import Shield34Logger


class Shield34Properties:
    DEFAULT_API_BASE_URL = 'https://reports-api.shield34.com'
    isInitialized = False
    configParser = configparser.ConfigParser()
    api_key = None
    api_secret = None
    binding_server_mode = None
    api_base_url = DEFAULT_API_BASE_URL
    external_proxy_address = None
    propertiesFilePath = None
    enable_ssl_certificate_verification=True
    selenium_proxy_address=None

    @staticmethod
    def get_value(section, key):
        if not Shield34Properties.isInitialized:
            raise Shield34PropertiesSyntaxIncorrect
        return Shield34Properties.configParser.get(section, key)

    @staticmethod
    def getPropertiesFilePath():
        filename = None
        if Shield34Properties.propertiesFilePath is not None:
            if os.path.exists(Shield34Properties.propertiesFilePath) and os.path.isfile(Shield34Properties.propertiesFilePath):
                filename = Shield34Properties.propertiesFilePath

        if filename is None:
            filename = Shield34Properties.findPropertiesFilePath()

        if filename is None:
            raise Shield34PropertiesFileNotFoundException

        return filename



    @staticmethod
    def findPropertiesFilePath():
        path = "."
        filename = ""
        while filename == "":
            filename = FileHandler.find_files(path, 'shield34.ini')
            if filename == "":
                new_path = os.path.abspath(os.path.join(path, os.pardir))
                if new_path == path:
                    break
                else:
                    path = new_path
        if filename == "":
            return None
        return filename

    @staticmethod
    def setPropertiesFilePath(filename):
        Shield34Properties.propertiesFilePath = filename

    @staticmethod
    def readPropertiesFile():
        propertiesFilePath = ""
        try:
            propertiesFilePath = Shield34Properties.getPropertiesFilePath()
            if propertiesFilePath != "":
                Shield34Properties.configParser.read(propertiesFilePath)
                Shield34Properties.isInitialized = True
            else:
                Shield34Logger.logger.error("{} config file not found...".format(propertiesFilePath))
        except Shield34PropertiesFileNotFoundException as e:
            Shield34Logger.logger.error("Configuration ini config file not found...")
            raise e

        if propertiesFilePath == "":
            raise Shield34PropertiesFileNotFoundException



    @staticmethod
    def initialize():
        if not Shield34Properties.isInitialized:
            Shield34Properties.readPropertiesFile()
            Shield34Properties.api_key = Shield34Properties.get_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_REPORTS_API_KEY)
            Shield34Properties.api_secret = Shield34Properties.get_value(
                Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                Shield34PropertiesConstants.PROP_REPORTS_API_SECRET)
            try:
                Shield34Properties.binding_server_mode = Shield34Properties.get_value(
                    Shield34PropertiesConstants.PROP_PROXY_SECTION,
                    Shield34PropertiesConstants.PROP_PROXY_BINDING_MODE)
            except Exception:
                Shield34Properties.binding_server_mode = "local"
            try:
                Shield34Properties.api_base_url = Shield34Properties.get_value(
                    Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                    Shield34PropertiesConstants.PROP_REPORTS_API_BASE_URL)
            except Exception:
                Shield34Properties.api_base_url = Shield34Properties.DEFAULT_API_BASE_URL
                pass

            try:
                Shield34Properties.external_proxy_address = Shield34Properties.get_value(
                    Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_SECTION,
                    Shield34PropertiesConstants.PROP_EXTERNAL_PROXY_ADDRESS)
                if Shield34Properties.external_proxy_address == '':
                    Shield34Properties.external_proxy_address = None
            except Exception:
                Shield34Properties.external_proxy_address = None

            try:
                Shield34Properties.enable_ssl_certificate_verification = Shield34Properties.get_value(
                    Shield34PropertiesConstants.PROP_REPORTS_SECTION,
                    Shield34PropertiesConstants.PROP_ENABLE_SSL_CERTIFICATE_VERIFICATION)
                Shield34Properties.enable_ssl_certificate_verification = Shield34Properties.enable_ssl_certificate_verification.lower() == 'true'
            except Exception:
                Shield34Properties.enable_ssl_certificate_verification = True

            try:
                Shield34Properties.selenium_proxy_address = Shield34Properties.get_value(
                    Shield34PropertiesConstants.PROP_PROXY_SECTION,
                    Shield34PropertiesConstants.PROP_SELENIUM_PROXY_ADDRESS)
                if Shield34Properties.selenium_proxy_address == '' :
                    Shield34Properties.selenium_proxy_address = Shield34Properties.external_proxy_address
            except Exception:
                Shield34Properties.selenium_proxy_address = Shield34Properties.external_proxy_address


            Shield34Properties.isInitialized = True
