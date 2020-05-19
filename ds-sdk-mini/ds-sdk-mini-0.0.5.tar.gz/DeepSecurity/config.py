#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

import logging

class Config():
    def __init__(self):
        """Constructor"""
        # Default Base url
        self.host = "https://dsm.example.com:4119/api"
        self.api_key = {}
        self.username = ""
        self.password = ""

        # Logging Settings
        self.logger = {}
        self.logger["urllib3_logger"] = logging.getLogger("urllib3")
        # Log format
        self.logger_format = '%(asctime)s %(levelname)s %(message)s'
        # Log stream handler
        self.logger_stream_handler = None
        # Log file handler
        self.logger_file_handler = None
        # Debug file location
        self.logger_file = None
        # Debug switch
        self.debug = False

        # SSL/TLS verification
        # Set this to false to skip verifying SSL certificate when calling API
        # from https server.
        self.verify_ssl = False
        # Set this to customize the certificate file to verify the peer.
        self.ssl_ca_cert = None
        # client certificate file
        self.cert_file = None
        # client key file
        self.key_file = None
        # Set this to True/False to enable/disable SSL hostname verification.
        self.assert_hostname = None

        # Proxy URL
        self.proxy = None
    