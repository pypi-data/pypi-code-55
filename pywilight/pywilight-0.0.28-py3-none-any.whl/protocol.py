"""WiLight Protocol Support."""
import asyncio
from collections import deque
import logging
import codecs
import binascii


class WiLightProtocol(asyncio.Protocol):
    """WiLight device control protocol."""

    transport = None  # type: asyncio.Transport

    def __init__(self, client, disconnect_callback=None, loop=None,
                 logger=None):
        """Initialize the WiLight protocol."""
        self.client = client
        self.loop = loop
        self.logger = logger
        self._buffer = b''
        self.disconnect_callback = disconnect_callback
        self._timeout = None
        self._cmd_timeout = None
        self._keep_alive = None

    def connection_made(self, transport):
        """Initialize protocol transport."""
        self.transport = transport
        self._reset_timeout()

    def _send_keepalive_packet(self):
        """Send a keep alive packet."""
        packet = self.format_packet("000000", self.client.num_serial)
        #self.logger.debug('sending keep alive packet')
        #self.transport.write(packet)
        asyncio.get_running_loop().create_task(self.client._send(packet))

    def _reset_timeout(self):
        """Reset timeout for date keep alive."""
        if self._timeout:
            self._timeout.cancel()
        self._timeout = self.loop.call_later(self.client.timeout,
                                             self.transport.close)
        if self._keep_alive:
            self._keep_alive.cancel()
        self._keep_alive = self.loop.call_later(
            self.client.keep_alive_interval,
            self._send_keepalive_packet)

    def reset_cmd_timeout(self):
        """Reset timeout for command execution."""
        if self._cmd_timeout:
            self._cmd_timeout.cancel()
        self._cmd_timeout = self.loop.call_later(self.client.timeout,
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
                #self.logger.warning('WiLight %s dropping invalid data: %s', self.client.num_serial, self._buffer)
                self.logger.debug('WiLight %s dropping invalid data: %s', self.client.num_serial, self._buffer)

    @staticmethod
    def _valid_packet(self, packet):
        """Validate incoming packet."""
        if packet[0:1] != b'&':
            return False
        #self.logger.warning('len de %s: %i', self.client.model, len(packet))
        if self.client.model == "0001":
            if len(packet) < 80:
                return False
        elif self.client.model == "0002":
            if len(packet) < 82:
                return False
        elif self.client.model == "0100":
            if len(packet) < 90:
                return False
        elif self.client.model == "0102":
            if len(packet) < 84:
                return False
        elif self.client.model == "0103":
            if len(packet) < 82:
                return False
        elif self.client.model == "0104":
            if len(packet) < 51:
                return False
        elif self.client.model == "0105":
            if len(packet) < 81:
                return False
        elif self.client.model == "0107":
            if len(packet) < 40:
                return False
        b_num_serial = self.client.num_serial.encode()
        #self.logger.warning('b_num_serial %s', b_num_serial)
        for i in range(0, 12):
            if packet[i + 1] != b_num_serial[i]:
                return False
        return True

    def _handle_packet(self, packet):
        """Parse incoming packet."""
        #self.logger.warning('handle data: %s', packet)
        if self.client.model == "0001":
            self._handle_0001_packet(packet)
        elif self.client.model == "0002":
            self._handle_0002_packet(packet)
        elif self.client.model == "0100":
            self._handle_0100_packet(packet)
        elif self.client.model == "0102":
            self._handle_0102_packet(packet)
        elif self.client.model == "0103":
            self._handle_0103_packet(packet)
        elif self.client.model == "0104":
            self._handle_0104_packet(packet)
        elif self.client.model == "0105":
            self._handle_0105_packet(packet)
        elif self.client.model == "0107":
            self._handle_0107_packet(packet)

    def _handle_0001_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 1):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.client.num_serial, index, on)
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.client.states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0002_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 3):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.client.num_serial, index, on)
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.client.states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0100_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 3):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.client.num_serial, index, on)
            brightness = int(packet[26+3*index:29+3*index])
            #self.logger.warning('WiLight %s index %i, brightness: %i', self.client.num_serial, index, brightness)
            states[format(index, 'x')] = {"on": on, "brightness": brightness}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("brightness" in client_state):
                if (client_state["brightness"] != brightness):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.client.states[format(index, 'x')] = {"on": on, "brightness": brightness}

        self._handle_packet_end(states, changes)

    def _handle_0102_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 3):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.client.num_serial, index, on)
            states[format(index, 'x')] = {"on": on}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.client.states[format(index, 'x')] = {"on": on}

        self._handle_packet_end(states, changes)

    def _handle_0103_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 1):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            motor_state = "stopped"
            if (packet[23:24] == b'1'):
                motor_state = "opening"
            if (packet[23:24] == b'0'):
                motor_state = "closing"
            #self.logger.warning('WiLight %s index %i, motor_state: %s', self.client.num_serial, index, motor_state)
            position_target = int(packet[24:27])
            #self.logger.warning('WiLight %s index %i, position_target: %i', self.client.num_serial, index, position_target)
            position_current = int(packet[27:30])
            #self.logger.warning('WiLight %s index %i, position_current: %i', self.client.num_serial, index, position_current)
            states[format(index, 'x')] = {"motor_state": motor_state, "position_target": position_target, "position_current": position_current}
            changed = False
            if ("motor_state" in client_state):
                if (client_state["motor_state"] != motor_state):
                    changed = True
            else:
                changed = True
            if ("position_target" in client_state):
                if (client_state["position_target"] != position_target):
                    changed = True
            else:
                changed = True
            if ("position_current" in client_state):
                if (client_state["position_current"] != position_current):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.client.states[format(index, 'x')] = {"motor_state": motor_state, "position_target": position_target, "position_current": position_current}

        self._handle_packet_end(states, changes)

    def _handle_0104_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 2):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}

            if index == 0:

                on = (packet[23:24] == b'1')
                #self.logger.warning('WiLight %s index %i, on: %s', self.client.num_serial, index, on)
                states[format(index, 'x')] = {"on": on}
                changed = False
                if ("on" in client_state):
                    if (client_state["on"] is not on):
                        changed = True
                else:
                    changed = True
                if changed:
                    changes.append(format(index, 'x'))
                    self.client.states[format(index, 'x')] = {"on": on}

            elif index == 1:

                direction = "off"
                if (packet[24:25] == b'0'):
                    direction = "forward"
                if (packet[24:25] == b'2'):
                    direction = "reverse"
                #self.logger.warning('WiLight %s index %i, direction: %s', self.client.num_serial, index, direction)
                speed = "low"
                if (packet[25:26] == b'1'):
                    speed = "medium"
                if (packet[25:26] == b'2'):
                    speed = "high"
                #self.logger.warning('WiLight %s index %i, speed: %s', self.client.num_serial, index, speed)
                states[format(index, 'x')] = {"direction": direction, "speed": speed}
                changed = False
                if ("direction" in client_state):
                    if (client_state["direction"] != direction):
                        changed = True
                else:
                    changed = True
                if ("speed" in client_state):
                    if (client_state["speed"] != speed):
                        changed = True
                else:
                    changed = True
                if changed:
                    changes.append(format(index, 'x'))
                    self.client.states[format(index, 'x')] = {"direction": direction, "speed": speed}

        self._handle_packet_end(states, changes)

    def _handle_0105_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 2):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23+index:24+index] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.client.num_serial, index, on)
            timer_target = int(packet[25+5*index:30+5*index])
            #self.logger.warning('WiLight %s index %i, timer_target: %i', self.client.num_serial, index, timer_target)
            timer_current = int(packet[35+5*index:40+5*index])
            #self.logger.warning('WiLight %s index %i, timer_current: %i', self.client.num_serial, index, timer_current)
            states[format(index, 'x')] = {"on": on, "timer_target": timer_target, "timer_current": timer_current}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("timer_target" in client_state):
                if (client_state["timer_target"] != timer_target):
                    changed = True
            else:
                changed = True
            if ("timer_current" in client_state):
                if (client_state["timer_current"] != timer_current):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.client.states[format(index, 'x')] = {"on": on, "timer_target": timer_target, "timer_current": timer_current}

        self._handle_packet_end(states, changes)

    def _handle_0107_packet(self, packet):
        """Parse incoming packet."""
        states = {}
        changes = []
        for index in range(0, 1):

            client_state = self.client.states.get(format(index, 'x'), None)
            if client_state is None:
                client_state = {}
            on = (packet[23:24] == b'1')
            #self.logger.warning('WiLight %s index %i, on: %s', self.client.num_serial, index, on)
            hue = int(packet[36:39])
            #self.logger.warning('WiLight %s index %i, hue: %i', self.client.num_serial, index, hue)
            saturation = int(packet[39:42])
            #self.logger.warning('WiLight %s index %i, saturation: %i', self.client.num_serial, index, saturation)
            brightness = int(packet[42:45])
            #self.logger.warning('WiLight %s index %i, brightness: %i', self.client.num_serial, index, brightness)
            states[format(index, 'x')] = {"on": on, "hue": hue, "saturation": saturation, "brightness": brightness}
            changed = False
            if ("on" in client_state):
                if (client_state["on"] is not on):
                    changed = True
            else:
                changed = True
            if ("hue" in client_state):
                if (client_state["hue"] != hue):
                    changed = True
            else:
                changed = True
            if ("saturation" in client_state):
                if (client_state["saturation"] != saturation):
                    changed = True
            else:
                changed = True
            if ("brightness" in client_state):
                if (client_state["brightness"] != brightness):
                    changed = True
            else:
                changed = True
            if changed:
                changes.append(format(index, 'x'))
                self.client.states[format(index, 'x')] = {"on": on, "hue": hue, "saturation": saturation, "brightness": brightness}

        self._handle_packet_end(states, changes)

    def _handle_packet_end(self, states, changes):
        """Finalizes packet handling."""
        for index in changes:
            for status_cb in self.client.status_callbacks.get(index, []):
                # Sending states by Callbak to the index
                status_cb(states[index])
        if self._cmd_timeout:
            self._cmd_timeout.cancel()

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

class WiLightClient:
    """WiLight client wrapper class."""

    def __init__(self, device_id=None, host=None,
                 port=None, model=None, config_ex=None,
                 disconnect_callback=None, reconnect_callback=None,
                 loop=None, logger=None, timeout=None, reconnect_interval=None,
                 keep_alive_interval=None):
        """Initialize the WiLight client wrapper."""
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
        self.num_serial = device_id[2:]
        self.device_id = device_id
        self.host = host
        self.port = port
        self.model = model
        self.config_ex = config_ex
        self.transport = None
        self.protocol = None
        self.is_connected = False
        self.reconnect = True
        self.timeout = timeout
        self.reconnect_interval = reconnect_interval
        self.keep_alive_interval = keep_alive_interval
        self.disconnect_callback = disconnect_callback
        self.reconnect_callback = reconnect_callback
        self.status_callbacks = {}
        self.states = {}
        self.lock = None

    async def setup(self):
        """Set up the connection with automatic retry."""
        self.lock = asyncio.Lock()
        while True:
            fut = self.loop.create_connection(
                lambda: WiLightProtocol(
                    self,
                    disconnect_callback=self.handle_disconnect_callback,
                    loop=self.loop, logger=self.logger),
                host=self.host,
                port=self.port)
            try:
                self.transport, self.protocol = \
                    await asyncio.wait_for(fut, timeout=self.timeout)
            except asyncio.TimeoutError:
                self.logger.warning("Could not connect due to timeout error.")
            except OSError as exc:
                self.logger.warning("Could not connect due to error: %s",
                                    str(exc))
            else:
                self.is_connected = True
                if self.reconnect_callback:
                    self.reconnect_callback()
                break
            await asyncio.sleep(self.reconnect_interval)

    def stop(self):
        """Shut down transport."""
        self.reconnect = False
        self.logger.debug("Shutting down.")
        if self.transport:
            self.transport.close()

    async def handle_disconnect_callback(self):
        """Reconnect automatically unless stopping."""
        self.is_connected = False
        if self.disconnect_callback:
            self.disconnect_callback()
        if self.reconnect:
            self.logger.debug("Protocol disconnected...reconnecting")
            await self.setup()
            self.protocol.reset_cmd_timeout()
            packet = self.protocol.format_packet("000000", self.num_serial)
            #self.logger.warning('sending packet disconnected: %s', packet)
            #self.protocol.transport.write(packet)
            await self._send(packet)

    def register_status_callback(self, callback, index):
        """Register a callback which will fire when state changes."""
        if self.status_callbacks.get(index, None) is None:
            self.status_callbacks[index] = []
        self.status_callbacks[index].append(callback)

    async def _send(self, packet):
        """Add packet to send queue."""
        #self.logger.warning('sending packet _send: %s', packet)
        self.protocol.reset_cmd_timeout()
        async with self.lock:
            self.protocol.transport.write(packet)
            await asyncio.sleep(0.1)

    async def turn_on(self, index=None):
        """Turn on device."""
        if index is not None:
            #self.logger.warning('index turn_on ok: %s', index)
            commands_on = ["001000", "003000", "005000"]
            packet = self.protocol.format_packet(commands_on[int(index)], self.num_serial)
        else:
            #self.logger.warning('index turn_on nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def turn_off(self, index=None):
        """Turn off device."""
        if index is not None:
            #self.logger.warning('index turn_off ok: %s', index)
            commands_off = ["002000", "004000", "006000"]
            packet = self.protocol.format_packet(commands_off[int(index)], self.num_serial)
        else:
            #self.logger.warning('index turn_off nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def set_brightness(self, index=None, brightness=None):
        """Set device's brightness."""
        if (index is not None and brightness is not None):
            commands_brigthness = ["007003", "008003", "009003"]
            command = commands_brigthness[int(index)] + '{:0>3}'.format(brightness)
            #self.logger.warning('brightness command: %s', command)
            packet = self.protocol.format_packet(command, self.num_serial)
        else:
            #self.logger.warning('brightness command nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def set_hs_color(self, index=None, hue=None, saturation=None):
        """Set device's hue and saturation."""
        if (index is not None and hue is not None and saturation is not None):
            command = "012006" + '{:0>3}'.format(hue) + '{:0>3}'.format(saturation)
            #self.logger.warning('hue_saturation command: %s', command)
            packet = self.protocol.format_packet(command, self.num_serial)
        else:
            #self.logger.warning('hue_saturation command nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def set_hsb_color(self, index=None, hue=None, saturation=None, brightness=None):
        """Set device's hue, saturation and brightness."""
        if (index is not None and hue is not None and saturation is not None and brightness is not None):
            command = "011009" + '{:0>3}'.format(hue) + '{:0>3}'.format(saturation) + '{:0>3}'.format(brightness)
            #self.logger.warning('hue_sat_bri command: %s', command)
            packet = self.protocol.format_packet(command, self.num_serial)
        else:
            #self.logger.warning('hue_sat_bri command nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def set_fan_direction(self, index=None, direction=None):
        """Set fan direction."""
        if (index is not None and direction is not None):
            command = "000000"
            if direction == "forward":
                command = "003000"
            elif direction == "off":
                command = "004000"
            elif direction == "reverse":
                command = "005000"
            #self.logger.warning('direction command: %s', command)
            packet = self.protocol.format_packet(command, self.num_serial)
        else:
            #self.logger.warning('direction command nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def set_fan_speed(self, index=None, speed=None):
        """Set fan speed."""
        if (index is not None and speed is not None):
            command = "000000"
            if speed == "low":
                command = "006000"
            elif speed == "medium":
                command = "007000"
            elif speed == "high":
                command = "008000"
            #self.logger.warning('speed command: %s', command)
            packet = self.protocol.format_packet(command, self.num_serial)
        else:
            #self.logger.warning('direction command nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def cover_command(self, index=None, cv_command=None):
        """Send cover command."""
        if (index is not None and cv_command is not None):
            command = "000000"
            if cv_command == "open":
                command = "001000"
            elif cv_command == "close":
                command = "002000"
            elif cv_command == "stop":
                command = "003000"
            #self.logger.warning('cover command: %s', command)
            packet = self.protocol.format_packet(command, self.num_serial)
        else:
            #self.logger.warning('cover command nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def set_cover_position(self, index=None, position=None):
        """Set cover position."""
        if (index is not None and position is not None):
            command = "007003" + '{:0>3}'.format(position)
            #self.logger.warning('position command: %s', command)
            packet = self.protocol.format_packet(command, self.num_serial)
        else:
            #self.logger.warning('position command nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def set_switch_time(self, index=None, target_time=None):
        """Set switch time."""
        if (index is not None and target_time is not None):
            commands_target_time = ["005005", "006005"]
            command = commands_target_time[int(index)] + '{:0>5}'.format(target_time)
            #self.logger.warning('target_time command: %s', command)
            packet = self.protocol.format_packet(command, self.num_serial)
        else:
            #self.logger.warning('target_time command nok')
            packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)

    async def status(self, index=None):
        """Get current device status."""
        packet = self.protocol.format_packet("000000", self.num_serial)
        await self._send(packet)


async def create_wilight_connection(device_id=None,
                                     host=None,
                                     port=None,
                                     model=None,
                                     config_ex=None,
                                     disconnect_callback=None,
                                     reconnect_callback=None, loop=None,
                                     logger=None, timeout=None,
                                     reconnect_interval=None,
                                     keep_alive_interval=None):
    """Create WiLight Client class."""
    client = WiLightClient(device_id=device_id, host=host, port=port, model=model, config_ex=config_ex,
                        disconnect_callback=disconnect_callback,
                        reconnect_callback=reconnect_callback,
                        loop=loop, logger=logger,
                        timeout=timeout, reconnect_interval=reconnect_interval,
                        keep_alive_interval=keep_alive_interval)
    await client.setup()

    return client
