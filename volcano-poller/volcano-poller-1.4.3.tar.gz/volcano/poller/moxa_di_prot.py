import array

try:
    import fcntl
except ImportError:
    print('MOXA DI disabled for Windows')

from volcano.general.xml_reader import XmlReader
from volcano.general import variant

from . import time_tools
from . import connected_values


class _MoxaInput:       # pylint:disable=too-few-public-methods
    def __init__(self, node):
        p = XmlReader(node)

        self.name = p.get_str('name')
        self.index = p.get_int('index', min_val=0, max_val=3)
        self.invert = p.get_bool('invert', False)
        self.tag = connected_values.ConnectedValue(self.name, variant.BoolValue(), True)
        

class MoxaDIProtocol:
    def __init__(self, my_xml_node, proposed_name, parent_log):
        p = XmlReader(my_xml_node)

        self.aux_name_ = p.get_str('name', proposed_name)
        self.log = parent_log.getChild(self.aux_name_)
        self.inputs_ = []
        self.timeout_ = time_tools.Timeout(0.1, expired=True)

        for node in my_xml_node.findall('DI'):
            inp = _MoxaInput(node)
            self.inputs_.append(inp)

    def aux_name(self):
        return self.aux_name_

    def empty(self):
        return len(self.inputs_) == 0

    def sync(self, services: dict):
        assert isinstance(services, dict), dict
        
        for inp in self.inputs_:
            inp.tag.sync(services)

    def run_once_safe(self, _reactor) -> None:
        log = self.log

        if not self.timeout_.is_expired():
            return
    
        self.timeout_.start()

        try:
        
            with open('/dev/dio') as fd:
                for inp in self.inputs_:
                    buf = array.array('l', [inp.index, 0])
                    res = fcntl.ioctl(fd, 17, buf)
                    if res == 0:
                        input_state = 0 if buf[1] == 1 else 1
                        tag_state = input_state == 0 if inp.invert else input_state == 1
                        inp.tag.set(tag_state)
                    else:
                        log.warn('Error reading input #%s. ioctl=%s', inp.index, res)
                        inp.tag.set(False, quality=2)

        except Exception as e:  # exceptions in threads are not visible by default
            log.error(e)
            #traceback.print_exc()
            for inp in self.inputs_:
                inp.tag.set(False, quality=4)

        finally:
            _reactor.callInThread(self.run_once_safe, _reactor)

    def safe_close(self) -> None:
        self.log.info('Protocol released')
