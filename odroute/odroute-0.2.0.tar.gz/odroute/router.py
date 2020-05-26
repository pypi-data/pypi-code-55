# -*- coding: utf-8 -*-
import logging
import sys
import zmq

from collections import namedtuple

from .exceptions import PortAlreadyUsed
from .input import StreamInput, EDIInput
from .output import ZMQOutput, EDIOutput
from .utils import index_by_dict_key, index_by_obj_prop
from .config import load_config_file

from odroute import __version__

logger = logging.getLogger(__name__)


class StreamRouter:
    """
    Router instance. Handles input and output connections & routing (priority).
    """
    _source_info = []
    _destinations = []
    _inputs = []
    _current_input = None
    _last_input = None
    _forced_port = None
    _outputs = []
    _current_config = None
    _state = None
    _state_change_callbacks = []

    DelaySettings = namedtuple('DelaySettings', [
        'nodata_failover_delay',
        'nodata_recover_delay',
        'noaudio_failover_delay',
        'noaudio_recover_delay',
        'audio_threshold'])

    def __init__(self, config, **options):
        self._current_config = config
        self._rc = None

        self._source_info = config.get('source_info')
        self._destinations = config.get('destinations')

        self.delay_settings = StreamRouter.DelaySettings(
                config.get('nodata_failover_delay'),
                config.get('nodata_recover_delay'),
                config.get('noaudio_failover_delay'),
                config.get('noaudio_recover_delay'),
                config.get('audio_threshold'))

        self.zmq_ctx = zmq.Context()

    def get_current_input(self):
        return self._current_input

    def set_auto_switch(self):
        self._forced_port = None

    def force_input(self, i):
        if i not in [inp.port for inp in self._inputs]:
            raise ValueError("Port {} not available".format(i))
        self._forced_port = i


    def register_rc(self, rc_server):
        self._rc = rc_server


    ###################################################################
    # input a.k.a. source handling
    ###################################################################
    def _get_input_ports(self):
        return [i.port for i in self._inputs]

    def _check_port_unused(self, port):
        if port in self._get_input_ports():
            raise PortAlreadyUsed("Port {} is already in use".format(port))

    def add_input(self, input_info):
        proto = input_info['protocol']
        port = input_info['port']

        self._check_port_unused(port)

        if proto == 'zmq':
            i = StreamInput(self.zmq_ctx, port, self.delay_settings)
            self._inputs.append(i)
            logger.info('Created ZMQ input on port {}'.format(port))
        elif proto == 'edi':
            i = EDIInput(port, self.delay_settings)
            self._inputs.append(i)
            logger.info('Created EDI listener socket on port {}'.format(port))
        else:
            raise RuntimeError('Unknown protocol')

    def remove_input(self, port):
        index = index_by_obj_prop(self._inputs, 'port', port)
        if index > -1:
            # This will remove both the EDIInput and the EDI StreamInput instances
            i = self._inputs.pop(index)
            i.stop()
        logger.info('Removed input socket on port {}'.format(port))

    def get_inputs(self):
        return self._inputs

    ###################################################################
    # output a.k.a. destination handling
    ###################################################################
    def add_output(self, output):
        if output['protocol'] == "zmq":
            o = ZMQOutput(self.zmq_ctx, output)
            logger.info('Created ZMQ output to {}'.format(output['endpoint']))
            self._outputs.append(o)
        elif output['protocol'] == "edi":
            o = EDIOutput(output, __version__)
            logger.info('Created EDI output to {}:{}'.format(output['host'], output['port']))
            self._outputs.append(o)
        else:
            raise RuntimeError('Unknown protocol')

    def remove_output(self, output):
        index = index_by_obj_prop(self._outputs, 'output', output)
        if index > -1:
            i = self._outputs.pop(index)
            i.stop()
            logger.info('Removed output to {}'.format(output))
        else:
            logger.warning('Cannot remove output to {}, not found'.format(output))


    def get_outputs(self):
        return self._outputs

    def _get_destinations(self):
        return [o.output for o in self._outputs]

    ###################################################################

    def _set_current_input(self):
        current_input = None

        if not self._inputs:
            self._current_input = None
            return

        # force input
        if self._forced_port:
            filtered_inputs = [i for i in self._inputs if i.port == self._forced_port]
            if filtered_inputs:
                current_input = filtered_inputs[0]

        # Loop through the inputs and return the first available one.
        if not current_input:
            available_inputs = [i for i in self._inputs if i.is_available()]
            if available_inputs:
                current_input = available_inputs[0]

        self._current_input = current_input

        if current_input is not None and current_input != self._last_input:
            logger.info('Switching inputs: {} to {}'.format(self._last_input.port if self._last_input else None, current_input.port))
            self._last_input = current_input

    def start(self):
        logger.info('Starting up with {} inputs'.format(len(self._source_info)))
        for info in self._source_info:
            self.add_input(info)
        self._source_info = []

        for dest in self._destinations:
            self.add_output(dest)
        self._destinations = []

        while True:
            # Create a new poller every time, because the EDIInput might reconnect
            # and return another socket
            poller = zmq.Poller()
            for i in self._inputs:
                poller.register(i.get_socket(), zmq.POLLIN)

            if self._rc:
                poller.register(self._rc.get_socket(), zmq.POLLIN)

            timeout = 1000
            events = poller.poll(timeout)
            for sock, event in events:
                # sock might either be an input or the RC handler

                if self._rc and sock == self._rc.get_socket().fileno():
                    self._rc.recv_and_handle()
                else:
                    for i in self._inputs:
                        if i.get_socket() == sock:
                            inputframe = i.recv()

                            if inputframe is not None:
                                self._set_current_input()

                                if self._current_input is not None and inputframe.port == self._current_input.port:
                                    for o in self._outputs:
                                        o.send(inputframe)
                            break
                    else:
                        raise RuntimeError("Did not find input for socket fd=%s", sock)
            for i in self._inputs:
                i.tick()

    def stop(self):
        logger.info('Stopping router')
        for port in self._get_input_ports():
            self.remove_input(port=port)

        for destination in self._get_destinations():
            self.remove_output(destination)

    def reload_configuration(self):
        config_file = self._current_config.get('config_file')
        config = load_config_file(config_file)

        logging.debug("Reload delay settings")

        self.delay_settings = StreamRouter.DelaySettings(
                config.get('nodata_failover_delay'),
                config.get('nodata_recover_delay'),
                config.get('noaudio_failover_delay'),
                config.get('noaudio_recover_delay'),
                config.get('audio_threshold'))

        ###############################################################
        # reconfigure outputs, a.k.a. 'destinations'
        ###############################################################
        current_destinations = self._get_destinations()
        new_destinations = config.get('destinations')
        logging.debug("Reload outputs")

        # stop removed outputs
        for dest in current_destinations:
            if dest not in new_destinations:
                self.remove_output(dest)

        # add newly configured outputs
        for dest in new_destinations:
            if dest not in current_destinations:
                self.add_output(dest)

        ###############################################################
        # reconfigure inputs
        ###############################################################
        logging.debug("Reload inputs")
        current_inputs = [{"protocol": i.protocol, "port": i.port} for i in self._inputs]
        new_source_info = config.get('source_info')

        # stop removed inputs
        for current in current_inputs:
            if current not in new_source_info:
                self.remove_input(current['port'])

        # add newly configured inputs
        for new in new_source_info:
            if new not in current_inputs:
                self.add_input(new)

        # ensure order of the inputs corresponds to order in the config, with the ZMQ coming first
        inputs = []
        for new in new_source_info:
            for i in self._inputs:
                if i.port == new['port']:
                    inputs.append(i)
        self._inputs = inputs

