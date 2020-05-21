from .si1145 import SI1145


def get_si(si_verbose=True):
    s = SI1145()
    if si_verbose:
        vis = s.readVisible()
        UV = s.readUV()
        uvIndex = UV / 100.0
        print(vis)
        print(uvIndex)
        print('Lux = %.2f' % s.readLux(readdark=True))
        print('UV = %i UV index = %.2f' % (s.readUV(), s.readUV() / 100.0))
        print('Channels enabled: %s' % s.decodeCHLIST())
        for i in s.decodeCHLIST(): print('Gain of %s is %s' % (i, s.readGain(i)))
        print('Visible reading = %i' % s.readVisible())
        print('IR = %i' % s.readIR())

        print('*------------------------------*')
        print('Changing gain ')
        s.restart('Vis', "IR")
        print('Channels enabled: %s' % s.decodeCHLIST())
    s.writeGain('Vis', gain=4)
    s.writeGain('IR', gain=3)
    s.readDarkCnt()
    print('Lux = %.2f' % s.readLux())
    for i in s.decodeCHLIST(): print('Gain of %s is %s' % (i, s.readGain(i)))
    print('Visible reading = %i' % s.readVisible())
    print('IR = %i' % s.readIR())
