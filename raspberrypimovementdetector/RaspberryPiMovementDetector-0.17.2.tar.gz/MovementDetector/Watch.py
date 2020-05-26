import time
# create an EventEmitter instance
from pymitter import EventEmitter
from concurrent.futures import ThreadPoolExecutor


class Watch(object):
  # def __init__(self, gpio, trig, echo, func_in, func_out, offset):
  def __init__(self, **kwargs):    
    """ Watch(gpio=GPIO, trig=23, echo=24, func_in=None, func_out=None, offset=200)
            The Watch class.
            Please always use *kwargs* in the constructor.
            - *gpio*: Pass the GPIO object
            - *trig*: Pin for trigger
            - *echo*: Pin for trigger
            - *func_in*: handler when a objects comes into field
            - *func_out*: handler when a objects goes out of field
            - *offset*: offset in cm to determine if the object is IN zone or OUT zone
            """
    def dummy_func_in():
      print("Dummy in function")
    def dummy_func_out():
      print("Dummy out function")
    super(Watch, self).__init__()
    func_in = kwargs.get("func_in", dummy_func_in)
    func_out = kwargs.get("func_out", dummy_func_out)
    self._ee = EventEmitter(wildcard=True, new_listener=True, max_listeners=-1)    
    self._ee.on("ObjectIn", func_in)
    self._ee.on("ObjectOut", func_out)
    self._gpio = kwargs.get("gpio",None)
    self._trig = kwargs.get("trig",23)
    self._echo = kwargs.get("echo",24)
    self._offset = kwargs.get("offset",200)
    self._wasIn = False
    self._observer = ThreadPoolExecutor(max_workers=1)
    self._observer_on = True
    self._future = None

  def trigger_pin(self):
    return self._trig

  def echo_pin(self):
    return self._echo

  def ping(self):
    distance = self.get_distance()
    if distance < self._offset:
      if not self._wasIn:
        self._ee.emit("ObjectIn", distance)
        self._wasIn = True
    else:
      if self._wasIn:
        self._ee.emit("ObjectOut", distance)
        self._wasIn = False
    return

  def poll(self):
    while True:
      if self._observer_on:
        self.ping()
      else:
        return

  def observe(self):
    self._future = self._observer.submit(self.poll)
    return

  def stop(self):
    self._observer_on = False
    time.sleep(3)
    try:
      self._future.shutdown(wait=False)
    except:
      if self._future.running():
        self._observer.shutdown(wait=False)
    return

  def get_distance(self):
    print("Distance Measurement In Progress")
    self._gpio.setup(self._trig, self._gpio.OUT)
    self._gpio.setup(self._echo, self._gpio.IN)
    self._gpio.output(self._trig, False)
    print("Waiting For Sensor To Settle")
    time.sleep(2)

    self._gpio.output(self._trig, True)
    time.sleep(0.00001)
    self._gpio.output(self._trig, False)

    pulse_start = time.time()
    pulse_end = time.time()
    while self._gpio.input(self._echo)==0:
      pulse_start = time.time()

    while self._gpio.input(self._echo)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    print("Distance:",distance,"cm")

    self._gpio.cleanup()
    return distance
    
