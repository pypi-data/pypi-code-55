"""WiLight Protocol Support."""
import asyncio
from collections import deque
import logging
import codecs
import binascii


class WiLightProtocol(asyncio.Protocol):
    """WiLight device control protocol."""

    transport = None  # type: asyncio.Transport

    def __init__(self, device, disconnect_callback=None, loop=None,
                 logger=None):
        """Initialize the WiLight protocol."""
        self.device = device
        self.loop = loop
        self.logger = logger
        self._buffer = b''
        self.disconnect_callback = disconnect_callback
        self.states = {}
        self._timeout = None
        self._cmd_timeout = None
        self._keep_alive = None

    def connection_made(self, transport):
        """Initialize protocol transport."""
        self.transport = transport
        self._reset_timeout()

    def _send_keepalive_packet(self):
        """Send a keep alive packet."""
        if not self.device.in_transaction:
            packet = self.format_packet("000000", self.device.num_serial)
            #self.logger.debug('sending keep alive packet')
            self.transport.write(packet)

    def _reset_timeout(self):
        """Reset timeout for date keep alive."""
        if self._timeout:
            self._timeout.cancel()
        self._timeout = self.loop.call_later(self.device.timeout,
                                             self.transport.close)
        if self._keep_alive:
            self._keep_alive.cancel()
        self._keep_alive = self.loop.call_later(
            self.device.keep_alive_interval,
            self._send_keepalive_packet)

    def reset_cmd_timeout(self):
        """Reset timeout for command execution."""
        if self._cmd_timeout:
            self._cmd_timeout.cancel()
        self._cmd_timeout = self.loop.call_later(self.device.timeout,
                                                 self.transport.close)

    def data_received(self, data):
        """Add incoming data to buffer."""



        self._reset_timeout()




        self._buffer = data
        #self.logger.warning('recebeu data: %s', self._buffer)
        if self._valid_packet(self, self._buffer):
            self._handle_packet(self._buffer)
        else:
            if self._buffer[0:1] != b'%':
                #self.logger.warning('WiLight %s dropping invalid data: %s', self.device.num_serial, self._buffer)
                self.logger.debug('WiLight %s dropping invalid data: %s', self.device.num_serial, self._buffer)

    @staticmethod
    def _valid_packet(self, packet):
        """Validate incoming packet."""
        if packet[0:1] != b'&':
            return False
        #self.logger.warning('len de %s: %i', self.device.model, len(packet))
        if self.device.model == "0001":
            if len(packet) < 80:
                return False
        elif self.device.model == "0002":
            if len(packet) < 82:
                return False
        elif self.device.model == "0100":
            if len(packet) < 90:
                return False
        elif self.device.model == "0102":
            if len(packet) < 84:
                return False
        elif self.device.model == "0103":
            if len(packet) < 82:
                return False
        elif self.device.model == "0104":
            if len(packet) < 51:
                return False
        elif self.device.model == "0105":
            if len(packet) < 81:
                return False
        elif self.device.model == "0107":
            if len(packet) < 40:
                return False
        b_num_serial = self.device.num_serial.encode()
        #self.logger.warning('b_num_serial %s', b_num_serial)
        for i in range(0, 12):
            if packet[i + 1] != b_num_serial[i]:
                return False
        return True

    def _handle_packet(self, packet):
        """Parse incoming packet."""
        #self.logger.warning('handle data: %s', packet)
        if self.device.model == "0001":
            self._handle_0001_packet(packet)
        elif self.device.model == "0002":
            self._handle_0002_packet(packet)
        elif self.device.model == "0100":
            self._handle_0100_packet(packet)
        elif self.device.model == "0102":
            self._handle_0102_packet(packet)
        elif self.device.model == "0103":
            self._handle_0103_packet(packet)
        elif self.device.model == "0104":
            self._handle_0104_packet(packet)
        elif self.device.model == "0105":
            self._handle_0105_packet(packet)
        elif self.device.model == "0107":
            self._handle_0107_packet(packet)

    def _handle_0001_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 1):

            state = self.states.get(format(index, 'x'), None)
            if state is None:
                state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.device.num_serial, index, on)
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in state):
                if (state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0002_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 3):

            state = self.states.get(format(index, 'x'), None)
            if state is None:
                state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.device.num_serial, index, on)
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in state):
                if (state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0100_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 3):

            state = self.states.get(format(index, 'x'), None)
            if state is None:
                state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.device.num_serial, index, on)
            brightness = int(packet[26+3*index:29+3*index])
            #self.logger.warning('WiLight %s index %i, brightness: %i', self.device.num_serial, index, brightness)
            states[format(index, 'x')] = {"on": on, "brightness": brightness}
            changed = False
            if ("on" in state):
                if (state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("brightness" in state):
                if (state["brightness"] != brightness):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.states[format(index, 'x')] = {"on": on, "brightness": brightness}

        self._handle_packet_end(states, changes)

    def _handle_0102_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 3):

            state = self.states.get(format(index, 'x'), None)
            if state is None:
                state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.device.num_serial, index, on)
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in state):
                if (state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0103_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 1):

            state = self.states.get(format(index, 'x'), None)
            if state is None:
                state = {}
            motor_state = "stopped"
            if (packet[23:24] == b'1'):
                motor_state = "opening"
            if (packet[23:24] == b'0'):
                motor_state = "closing"
            #self.logger.warning('WiLight %s index %i, motor_state: %s', self.device.num_serial, index, motor_state)
            position_target = int(packet[24:27])
            #self.logger.warning('WiLight %s index %i, position_target: %i', self.device.num_serial, index, position_target)
            position_current = int(packet[27:30])
            #self.logger.warning('WiLight %s index %i, position_current: %i', self.device.num_serial, index, position_current)
            states[format(index, 'x')] = {"motor_state": motor_state, "position_target": position_target, "position_current": position_current}
            changed = False
            if ("motor_state" in state):
                if (state["motor_state"] != motor_state):
                    changed = True
            else:
                changed = True
            if ("position_target" in state):
                if (state["position_target"] != position_target):
                    changed = True
            else:
                changed = True
            if ("position_current" in state):
                if (state["position_current"] != position_current):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.states[format(index, 'x')] = {"motor_state": motor_state, "position_target": position_target, "position_current": position_current}

        self._handle_packet_end(states, changes)

    def _handle_0104_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 2):

            state = self.states.get(format(index, 'x'), None)
            if state is None:
                state = {}

            if index == 0:

                on = (packet[23:24] == b'1')
                #self.logger.warning('WiLight %s index %i, on: %s', self.device.num_serial, index, on)
                states[format(index, 'x')] = {"on": on}
                changed = False
                if ("on" in state):
                    if (state["on"] is not on):
                        changed = True
                else:
                    changed = True
                if changed:
                    changes.append(format(index, 'x'))
                    self.states[format(index, 'x')] = {"on": on}

            elif index == 1:

                direction = "off"
                if (packet[24:25] == b'0'):
                    direction = "forward"
                if (packet[24:25] == b'2'):
                    direction = "reverse"
                #self.logger.warning('WiLight %s index %i, direction: %s', self.device.num_serial, index, direction)
                speed = "low"
                if (packet[25:26] == b'1'):
                    speed = "medium"
                if (packet[25:26] == b'2'):
                    speed = "high"
                #self.logger.warning('WiLight %s index %i, speed: %s', self.device.num_serial, index, speed)
                states[format(index, 'x')] = {"direction": direction, "speed": speed}
                changed = False
                if ("direction" in state):
                    if (state["direction"] != direction):
                        changed = True
                else:
                    changed = True
                if ("speed" in state):
                    if (state["speed"] != speed):
                        changed = True
                else:
                    changed = True
                if changed:
                    changes.append(format(index, 'x'))
                    self.states[format(index, 'x')] = {"direction": direction, "speed": speed}

        self._handle_packet_end(states, changes)

    def _handle_0105_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 2):

            state = self.states.get(format(index, 'x'), None)
            if state is None:
                state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.device.num_serial, index, on)
            timer_target = int(packet[25+5*index:30+5*index])
            #self.logger.warning('WiLight %s index %i, timer_target: %i', self.device.num_serial, index, timer_target)
            timer_current = int(packet[35+5*index:40+5*index])
            #self.logger.warning('WiLight %s index %i, timer_current: %i', self.device.num_serial, index, timer_current)
            states[format(index, 'x')] = {"on": on, "timer_target": timer_target, "timer_current": timer_current}
            changed = False
            if ("on" in state):
                if (state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("timer_target" in state):
                if (state["timer_target"] != timer_target):
                    changed = True
            else:
                changed = True
            if ("timer_current" in state):
                if (state["timer_current"] != timer_current):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.states[format(index, 'x')] = {"on": on, "timer_target": timer_target, "timer_current": timer_current}

        self._handle_packet_end(states, changes)

    def _handle_0107_packet(self, packet):
        """Parse incoming packet."""
        self._reset_timeout()
        states = {}
        changes = []
        for index in range(0, 1):

            state = self.states.get(format(index, 'x'), None)
            if state is None:
                state = {}
            on = (packet[23:24] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.device.num_serial, index, on)
            hue = int(packet[36:39])
            #self.logger.warning('WiLight %s index %i, hue: %i', self.device.num_serial, index, hue)
            saturation = int(packet[39:42])
            #self.logger.warning('WiLight %s index %i, saturation: %i', self.device.num_serial, index, saturation)
            brightness = int(packet[42:45])
            #self.logger.warning('WiLight %s index %i, brightness: %i', self.device.num_serial, index, brightness)
            states[format(index, 'x')] = {"on": on, "hue": hue, "saturation": saturation, "brightness": brightness}
            changed = False
            if ("on" in state):
                if (state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("hue" in state):
                if (state["hue"] != hue):
                    changed = True
            else:
                changed = True
            if ("saturation" in state):
                if (state["saturation"] != saturation):
                    changed = True
            else:
                changed = True
            if ("brightness" in state):
                if (state["brightness"] != brightness):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.states[format(index, 'x')] = {"on": on, "hue": hue, "saturation": saturation, "brightness": brightness}

        self._handle_packet_end(states, changes)

    def _handle_packet_end(self, states, changes):
        """Finalizes packet handling."""
        for index in changes:
            #for status_cb in self.device.status_callbacks.get(index, []):
            #    # Sending states by Callbak to the index
            #    self.logger.warning('enviando callback %s index %s : %s', self.device.device_id, index, states[index])
            #    status_cb(states[index])
            status_callback = self.device.status_callbacks.get(index, None)
            if status_callback is not None:
                # Sending states by Callbak to the index
                self.logger.warning('enviando callback %s index %s : %s', self.device.device_id, index, states[index])
                status_callback(states[index])

        #self.logger.debug(states)
        if self.device.in_transaction:
            self.device.in_transaction = False
            self.device.active_packet = None
            self.device.active_transaction.set_result(states)
            while self.device.status_waiters:
                waiter = self.device.status_waiters.popleft()
                waiter.set_result(states)
            if self.device.waiters:
                self.send_packet()
            else:
                self._cmd_timeout.cancel()
        elif self._cmd_timeout:
            self._cmd_timeout.cancel()

    def send_packet(self):
        """Write next packet in send queue."""
        waiter, packet = self.device.waiters.popleft()
        #self.logger.warning('sending packet send_packet: %s', packet)
        self.device.active_transaction = waiter
        self.device.in_transaction = True
        self.device.active_packet = packet
        self.reset_cmd_timeout()
        self.transport.write(packet)

    @staticmethod
    def format_packet(command, num_serial):
        """Format packet to be sent."""
        frame_header = b"!" + num_serial.encode()
        return frame_header + command.encode()

    def connection_lost(self, exc):
        """Log when connection is closed, if needed call callback."""
        if exc:
            self.logger.error('disconnected due to error')
        else:
            self.logger.info('disconnected because of close/abort.')
        if self._keep_alive:
            self._keep_alive.cancel()
        if self.disconnect_callback:
            asyncio.ensure_future(self.disconnect_callback(), loop=self.loop)
