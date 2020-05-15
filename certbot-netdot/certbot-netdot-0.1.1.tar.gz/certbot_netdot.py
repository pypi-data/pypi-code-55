import logging
import itertools
import re
import zope.interface

from certbot.plugins.dns_common import DNSAuthenticator
from certbot.interfaces import IAuthenticator, IPluginFactory
from datetime import datetime, timedelta
from time import sleep

import pynetdot


logger = logging.getLogger(__name__)


def as_bool(obj):
    if isinstance(obj, str):
        obj = obj.strip().lower()
        if obj in ['True', 'true', 'yes', 'on', 'y', 't', '1']:
            return True
        elif obj in ['False', 'false', 'no', 'off', 'n', 'f', '0']:
            return False
        else:
            raise ValueError("String is not true/false: %r" % obj)
    return bool(obj)


@zope.interface.implementer(IAuthenticator)
@zope.interface.provider(IPluginFactory)
class NetdotAuthenticator(DNSAuthenticator):
    """
    Netdot DNS ACME authenticator.

    This Authenticator uses the Netdot REST API to fulfill a dns-01 challenge.
    """

    #: Short description of plugin
    description = __doc__.strip().split("\n", 1)[0]

    #: TTL for the validation TXT record
    ttl = 30

    def __init__(self, *args, **kwargs):
        super(NetdotAuthenticator, self).__init__(*args, **kwargs)
        self._client = None
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds=90):
        super(NetdotAuthenticator, cls).add_parser_arguments(
            add, default_propagation_seconds)
        add("credentials", help="Netdot credentials INI file.")


    def more_info(self):
        """
        More in-depth description of the plugin.
        """

        return "\n".join(line[4:] for line in __doc__.strip().split("\n"))

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "Netdot credentials INI file",
            {
                "endpoint": "Api endpoint",
                "username": "API username for Netdot account",
                "password": "API password for Netdot account"
            }
        )

    def _get_netdot_client(self):
        verify = self.credentials.conf("verify")

        # Default verify to True
        if verify is None:
            verify = True

        return NetdotClient(
            self.credentials.conf("endpoint"),
            self.credentials.conf("username"),
            self.credentials.conf("password"),
            as_bool(verify)
        )

    def _perform(self, domain, validation_name, validation):
        netdot = self._get_netdot_client()
        netdot.add_txt_record(validation_name, validation, ttl=self.ttl)

    def _cleanup(self, domain, validation_name, validation):
        netdot = self._get_netdot_client()
        netdot.remove_record(validation_name)


class NetdotClient:
    """
    Encapsulates the communication with netdot
    """

    def __init__(self, *args, **kwargs):
        pynetdot.setup(*args, **kwargs)

    def lookup_rr(self, name):
        response = pynetdot.RR.search(name=name)
        if response:
            return response[0]

    def get_or_create_rr(self, name):
        rr = self.lookup_rr(name)
        if not rr:
            rr = pynetdot.RR()
            rr.name = name

        rr.active = True
        rr.save()
        return rr

    def remove_record(self, name):
        rr = self.lookup_rr(name)
        if rr:
            rr.delete()

    def add_txt_record(self, validation_name, validation, ttl=30):
        rr = self.get_or_create_rr(validation_name)

        rrtxt = pynetdot.RRTXT()
        rrtxt.txtdata = validation
        rrtxt.ttl = ttl
        rrtxt.rr = rr

        rrtxt.save()
