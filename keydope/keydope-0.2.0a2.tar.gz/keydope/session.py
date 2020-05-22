# Library for handling user sessions.
#
# Good dbus resources:
# - http://0pointer.net/blog/the-new-sd-bus-api-of-systemd.html
# - https://dbus.freedesktop.org/doc/dbus-tutorial.html

import logging
from typing import Optional

_DBUS_AVAILABLE = True
try:
    import dbus
    from dbus.mainloop.glib import DBusGMainLoop
    from gi.repository import GObject
except ImportError:
    _DBUS_AVAILABLE = False

# Well known dbus names
_LOGIND_BUS_NAME = 'org.freedesktop.login1'
_PROPERTIES_INTERFACE = 'org.freedesktop.DBus.Properties'
_MANAGER_INTERFACE = 'org.freedesktop.login1.Manager'
_SEAT_INTERFACE = 'org.freedesktop.login1.Seat'
_SESSION_INTERFACE = 'org.freedesktop.login1.Session'

logger = logging.getLogger(__name__)


def get_session_monitor():
    if _DBUS_AVAILABLE:
        return DbusSessionMonitor()
    logging.warning('dbus not available, not monitoring sessions')
    return DummySessionMonitor()


class DummySessionMonitor:

    # pylint: disable=no-self-use
    def get_active_session_id(self) -> Optional[str]:
        return None

    # pylint: disable=no-self-use
    def monitor(self, _):
        return


class DbusSessionMonitor:

    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        self._bus = dbus.SystemBus()
        logind_object = self._bus.get_object(_LOGIND_BUS_NAME,
                                             '/org/freedesktop/login1')
        seats = logind_object.ListSeats(dbus_interface=_MANAGER_INTERFACE)
        logging.debug(f'Seats seen by keydope: {seats}')
        if not seats:
            raise SystemError('No seats available')
        if len(seats) > 1:
            logging.warning('Keydope detected multiple seats, using first one.')
        seat_object = self._bus.get_object(
            _LOGIND_BUS_NAME, f'/org/freedesktop/login1/seat/{seats[0][0]}')
        # We can also use `Get` to get only a single property.
        seat_get_all = seat_object.get_dbus_method(
            'GetAll', dbus_interface=_PROPERTIES_INTERFACE)
        # _seat_getter is a callabale that returns the properties of the seat
        # owning this process.
        self._seat_getter = lambda: seat_get_all(_SEAT_INTERFACE)
        # self._seat_getter = seat_object.get_dbus_method('Get', )
        # Cache session getters for performance.
        # TODO: Measure and see if it really matters.
        self._session_id_to_getter = {}
        self._mainloop = GObject.MainLoop()

    def _get_active_session(self):
        session_id = self.get_active_session_id()
        if not session_id:
            return None
        if session_id not in self._session_id_to_getter:
            session_object = self._bus.get_object(
                _LOGIND_BUS_NAME,
                f'/org/freedesktop/login1/session/{session_id}')
            session_get_all = session_object.get_dbus_method(
                'GetAll', dbus_interface=_PROPERTIES_INTERFACE)
            self._session_id_to_getter[session_id] = lambda: session_get_all(
                _SESSION_INTERFACE)
        return self._session_id_to_getter[session_id]()

    def get_active_session_id(self) -> Optional[str]:
        return str(self._seat_getter()['ActiveSession'][0])

    def monitor(self, callback):

        # pylint: disable=unused-argument
        def _handler(signal, value, *args, **kwargs):
            # There may be no active session, for example after a user switches
            # to another virtual console and before they log in.
            active_session = None
            if signal == _SEAT_INTERFACE and 'ActiveSession' in value:
                active_session = self._get_active_session()
            callback(active_session)

        self._bus.add_signal_receiver(_handler,
                                      bus_name=_LOGIND_BUS_NAME,
                                      path_keyword='path',
                                      member_keyword='member')
        self._mainloop.run()
