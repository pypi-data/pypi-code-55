class LutronMessage(object):
    COMMAND = None

    def __init__(self, gw):
        assert gw.__class__.__name__=='Lutron'
        self._gw=gw

    @property
    def name(self):
        return self.COMMAND

    @property
    def gw(self):
        return self._gw

    @property
    def logger(self):
        return self.gw.logger

    def send(self, msg):
        return self.gw._send(msg)

    def get(self, topic, *args):
        msg='?%s,%s' % (self.name, topic)
        if args:
            msg+=','+','.join([str(x) for x in args])
        return self.send(msg)

    def set(self, topic, *args):
        msg='#%s,%s' % (self.name, topic)
        if args:
            msg+=','+','.join([str(x) for x in args])
        return self.send(msg)


class LutronMessageSYSTEM(LutronMessage):
    COMMAND = "SYSTEM"

    def getTime(self):
        return self.get(1)

    def getTimeZone(self):
        return self.get(4)

    def getDate(self):
        return self.get(2)

    def getOSrevision(self):
        return self.get(8)


class LutronMessageWithIntegrationId(LutronMessage):
    def __init__(self, gw, integrationId):
        super().__init__(gw)
        self._integrationId=integrationId

    @property
    def integrationId(self):
        return self._integrationId

    def get(self, topic, *args):
        super().get(self.integrationId, topic, *args)

    def set(self, topic, *args):
        super().set(self.integrationId, topic, *args)


class LutronMessageMONITORING(LutronMessage):
    COMMAND = "MONITORING"

    def enable(self, topic, state=True):
        if state:
            return self.set(topic, 1)
        return self.set(topic, 2)

    def diagnostic(self, state=True):
        return self.enable(1, state)

    def event(self, state=True):
        return self.enable(2, state)

    def button(self, state=True):
        return self.enable(3, state)

    def led(self, state=True):
        return self.enable(4, state)

    def zone(self, state=True):
        return self.enable(5, state)

    def occupancy(self, state=True):
        return self.enable(6, state)

    def scene(self, state=True):
        return self.enable(8, state)

    def hvac(self, state=True):
        return self.enable(17, state)

    def prompt(self, state=True):
        return self.enable(12, state)

    def all(self, state=True):
        return self.enable(255, state)
