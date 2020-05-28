# Install with:
# cd (fullfile(matlabroot,'extern','engines','python'))
# system('python setup.py install')
#

import matlab
print(matlab)
import matlab.engine
                                            
class MatlabCallback:
  def __init__(self, name, callback_name):
    try:
      import matlab.engine
    except Exception as e:
      print(str)
    self.engine = matlab.engine.connect_matlab(name)
    self.callback = self.engine.workspace[callback_name]
    print(self.callback)

  def __eval__(self,*args):
    ret = self.callback(*args)
