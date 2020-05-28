from .object import LutronObject


class LutronObjectOUTPUT(LutronObject):
    OBJECTNAME = 'OUTPUT'

    def _onInit(self):
        # lookup for object infos in the xmldb (if available)
        item=self.db.output(self.integrationId)
        self._type=None
        if item is not None:
            self._name=item.get('Name')
            self._type=item.get('OutputType')

        self._level=None

    def match(self, search):
        if super().match(search):
            return True

        try:
            if str(search).lower() in self._type.lower():
                return True
        except:
            pass
        return False

    def onRefresh(self):
        """Force object data refresh"""
        self.getLevel()

    def getLevel(self):
        return self.get(1)

    @property
    def level(self):
        return self._level

    def setLevel(self, level, fade=0, delay=0):
        fade=self.hms(fade)
        return self.set(1, level, self.hms(fade), self.hms(delay))

    def off(self, delay=0):
        return self.setLevel(0)

    def on(self, delay=0):
        return self.setLevel(100)

    def _onEvent(self, *args):
        action=int(args[0])
        if action==1:
            self._level=float(args[1])
            return True

    def __repr__(self):
        try:
            return '<%s:%s:%s(%.2f)>' % (self.__class__.__name__,
                self.integrationId, self.name,
                self.level)
        except:
            # self.logger.exception('repr')
            return '<%s:%d:%s>' % (self.__class__.__name__, self.integrationId, self.name)
