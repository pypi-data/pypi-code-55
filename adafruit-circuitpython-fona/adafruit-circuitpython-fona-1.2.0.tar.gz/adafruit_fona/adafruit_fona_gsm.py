# The MIT License (MIT)
#
# Copyright (c) 2020 Brent Rubell for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_fona_gsm`
=================================================================================

Interface for 2G GSM cellular modems such as the Adafruit FONA808.

* Author(s): Brent Rubell

"""


class GSM:
    """Interface for interacting with FONA 2G GSM modems.
    """

    def __init__(self, fona, apn):
        """Initializes interface with 2G GSM modem.
        :param adafruit_fona fona: The Adafruit FONA module we are using.
        :param tuple apn: Tuple containing APN name, (optional) APN username,
                            and APN password.

        """
        self._iface = fona
        self._apn = apn
        self._gsm_connected = False

        # Enable GPS module
        self._iface.gps = True

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.disconnect()

    @property
    def imei(self):
        """Returns the GSM modem's IEMI number, as a string."""
        return self._iface.iemi

    @property
    def iccid(self):
        """Returns the SIM card's ICCID, as a string."""
        return self._iface.iccid

    @property
    def is_attached(self):
        """Returns if the modem is attached to the network
        and the GPS has a fix."""
        if self._iface.gps == 3 and self._iface.network_status == 1:
            return True
        return False

    @property
    def is_connected(self):
        """Returns if attached to GSM
        and an IP Addresss was obtained.

        """
        if not self._gsm_connected:
            return False
        return True

    def connect(self):
        """Connect to GSM network."""
        if self._iface.set_gprs(self._apn, True):
            self._gsm_connected = True
        else:
            # reset context for next connection attempt
            self._iface.set_gprs(self._apn, False)

    def disconnect(self):
        """Disconnect from GSM network."""
        self._iface.set_gprs(self._apn, False)
        self._gsm_connected = False
