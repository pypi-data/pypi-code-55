from .object import LutronObject


class LutronObjectHVAC(LutronObject):
    OBJECTNAME = 'HVAC'

    def _onInit(self):
        # lookup for object infos in the xmldb (if available)
        item=self.db.hvac(self.integrationId)
        if item is not None:
            self._name=item.get('Name')

        self._temperature=None
        self._operatingMode=None
        self._fanMode=None
        self._spheat=None
        self._spcool=None
        self._callStatus=None
        self._eco=None

    def onRefresh(self):
        """Force object data refresh"""
        self.getTemperature()
        self.getOperatingMode()
        self.getFanMode()
        self.getSetpoints()
        self.getCallStatus()
        self.getEco()

    def getTemperature(self):
        """Retrieve the actual ambiant temperature"""
        return self.get(15)

    @property
    def temperature(self):
        """Return the last known ambiant temperature"""
        return self._temperature

    def getCallStatus(self):
        return self.get(14)

    @property
    def callStatus(self):
        return self._callStatus

    @property
    def callStatusStr(self):
        state=['None-Heat', 'Heat1', 'Heat12', 'Heat123', 'Heat3',
               'None-Cool', 'Cool1', 'Cool12',
               'Off', 'EmergencyHeat', 'Dry']
        try:
            return state[self.callSatus]
        except:
            return 'Unknown'

    def setCallStatusCool1(self):
        return self.set(14, 6)

    def setCallStatusCool12(self):
        return self.set(14, 7)

    def getEco(self):
        return self.get(5)

    @property
    def eco(self):
        return self._eco

    def setEco(self, enable):
        state=1
        if enable:
            state=2
        return self.set(5, state)

    def getSetpoints(self):
        return self.get(16)

    @property
    def spheat(self):
        return self._spheat

    @property
    def spcool(self):
        return self._spcool

    def setSetPoints(self, spheat, spcool):
        if spheat<spcool:
            spheat='%.1f' % spheat
            spcool='%.1f' % spcool
            return self.set(16, spheat, spcool)

    def getOperatingMode(self):
        return self.get(3)

    @property
    def operatingMode(self):
        return self._operatingMode

    @property
    def operatingModeStr(self):
        state=['Off', 'Heat', 'Cool', 'Auto', 'EmergencyHeat', 'Locked', 'Fan', 'Dry']
        try:
            return state[self.operatingMode-1]
        except:
            return 'Unknown'

    def setOperatingMode(self, mode):
        return self.set(3, mode)

    def setOperatingModeOff(self):
        self.setOperatingMode('1')

    def setOperatingModeHeat(self):
        self.setOperatingMode('2')

    def setOperatingModeCool(self):
        self.setOperatingMode('3')

    def setOperatingModeAuto(self):
        self.setOperatingMode('4')

    def getFanMode(self):
        return self.get(4)

    @property
    def fanMode(self):
        return self._fanMode

    @property
    def fanModeStr(self):
        state=['Auto', 'On', 'Cycler', 'NoFan', 'High', 'Medium', 'Low', 'Top']
        try:
            return state[self.fanMode-1]
        except:
            return 'Unknown'

    def setFanMode(self, mode):
        return self.set(4, mode)

    def setFanModeAuto(self):
        self.setFanMode('1')

    def setFanModeOn(self):
        self.setFanMode('1')

    def setFanModeHigh(self):
        self.setFanMode('5')

    def setFanModeMedium(self):
        self.setFanMode('6')

    def setFanModeLow(self):
        self.setFanMode('7')

    def setFanModeTop(self):
        self.setFanMode('8')

    def setAuto(self):
        self.setFanModeAuto()
        self.setOperatingModeAuto()

    def setMaximumCool(self):
        self.setOperatingModeCool()
        self.setFanModeHigh()

    def setMaximumHeat(self):
        self.setOperatingModeHeat()
        self.setFanModeHigh()

    def setOff(self):
        self.setOperatingModeOff()

    def RAZ(self):
        self.setAuto()
        self.setSetPoints(22, 22.5)

    def _onEvent(self, *args):
        action=int(args[0])
        if action==15:
            self._temperature=float(args[1])
            return True
        elif action==3:
            self._operatingMode=int(args[1])
            return True
        elif action==4:
            self._fanMode=int(args[1])
            return True
        elif action==5:
            state=int(args[1])
            if state==2:
                self._eco=True
            elif state==1:
                self._eco=False
            return True
        elif action==14:
            self._callStatus=int(args[1])
            return True
        elif action==16:
            self._spheat=float(args[1])
            self._spcool=float(args[2])
            return True

    def __repr__(self):
        try:
            return '<%s:%s:%s(T=%.1f, SP=%.01f/%.01f, MODE=%d:%s, STATE=%d:%s, FAN=%d:%s, ECO=%d)>' % (self.__class__.__name__,
                self.integrationId, self.name,
                self.temperature, self.spheat, self.spcool,
                self.operatingMode, self.operatingModeStr,
                self.callStatus, self.callStatusStr,
                self.fanMode, self.fanModeStr,
                self.eco)
        except:
            # self.logger.exception('repr')
            return '<%s:%d:%s>' % (self.__class__.__name__, self.integrationId, self.name)
