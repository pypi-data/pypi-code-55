import time
from unidecode import unidecode


class LutronObject(object):
    OBJECTNAME = ''

    def __init__(self, gw, integrationId, refreshPeriod=60, readOnly=False):
        assert gw.__class__.__name__=='Lutron'
        self._gw=gw
        self._integrationId=int(integrationId)
        self._readOnly=readOnly
        self._name='%s%d' % (self.OBJECTNAME.lower(), self._integrationId)
        if not self.gw._registerObject(self):
            raise ValueError('LutronObject creation error!')
        self.logger.info('Object <%s:%d:%s> created' % (self.OBJECTNAME, self.integrationId, self.name))
        self._label=self._name
        self._periodRefresh=refreshPeriod
        self._timeoutRefresh=0
        self._onInit()

    def _onInit(self):
        pass

    def setReadOnly(self, enable=True):
        self._readOnly=enable

    def _send(self, msg):
        return self.gw._send(msg)

    def get(self, *args):
        msg='?%s,%d' % (self.OBJECTNAME, self._integrationId)
        if args:
            msg+=','+','.join([str(x) for x in args])
        return self._send(msg)

    def set(self, *args):
        if not self._readOnly:
            msg='#%s,%d' % (self.OBJECTNAME, self._integrationId)
            if args:
                msg+=','+','.join([str(x) for x in args])
            return self._send(msg)
        self.logger.warning('write disabled on readonly object')

    def match(self, search):
        try:
            if str(search).lower() in unidecode(self.name):
                return True
            if str(self.integrationId)==search:
                return True
        except:
            pass
        return False

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def gw(self):
        return self._gw

    @property
    def db(self):
        return self.gw.db

    @property
    def integrationId(self):
        return self._integrationId

    @property
    def logger(self):
        return self.gw.logger

    def _onEvent(self, *args):
        pass

    def setRefreshPeriod(self, period):
        if period<5:
            period=5
        self._periodRefresh=period

    def refresh(self):
        self.onRefresh()
        self._timeoutRefresh=time.time()+self._periodRefresh

    def onRefresh(self):
        pass

    def _manager(self):
        if self.gw.isOpen():
            if time.time()>=self._timeoutRefresh:
                self.refresh()

    def hms(self, value):
        try:
            value=float(value)
            if value<=0:
                return '00'
            if value<1:
                return '0%.02f' % value
            h=value // 3600
            value -= h*3600
            m=value // 60
            value -= m*60
            s=value
            return '%02d:%02d:%02d' % (h, m, s)
        except:
            pass
        return '00'
