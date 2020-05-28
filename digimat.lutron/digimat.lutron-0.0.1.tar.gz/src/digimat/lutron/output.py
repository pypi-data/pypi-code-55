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

    def setLevel(self, level, delay=0):
        level='%.02f' % level
        if delay<=0:
            return self.set(1, level)

        if delay<1:
            delay='0%.02f' % delay
        else:
            h=delay // 3600
            delay -= h*3600
            m=delay // 60
            delay -= m*60
            s=delay
            delay='%02d:%02d:%02d' % (h, m, s)

        return self.set(1, level, delay)

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
