from .splice import Splice
from bitn import BitBin
from .stream import Stream

class Slim(Stream):


    def parse_payload(self,payload,pid):
        '''
        If you want to customize output,
        overload this method.
        '''
        try:
            tf = Splice(payload,pid=pid)
            tf.show_command()
            return True
        except:
            return False
 
