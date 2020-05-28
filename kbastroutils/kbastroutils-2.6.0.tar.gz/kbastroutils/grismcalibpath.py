class GrismCalibPath:
    def __init__(self):
        CONF = {('HST','WFC3','IR'): {('G102','F098M'):'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G102.cal.V4.32/G102.F098M.V4.32.conf',
                                      ('G102','F105W'):'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G102.cal.V4.32/G102.F105W.V4.32.conf',
                                      ('G141','F140W'):'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G141.cal.V4.32/G141.F140W.V4.32.conf',
                                      ('G141','F160W'):'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G141.cal.V4.32/G141.F160W.V4.32.conf'
                                     },
                ('HST','ACS','WFC'): {('G800L','F775W',1):'/Users/kbhirombhakdi/_work/_calib_files/ACS.WFC/ACS.WFC.CHIP1.Cycle13.5.conf',
                                      ('G800L','F775W',2):'/Users/kbhirombhakdi/_work/_calib_files/ACS.WFC/ACS.WFC.CHIP2.Cycle13.5.conf'
                                     }
               }
        SENS = {('HST','WFC3','IR'): {'G102':'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G102.cal.V4.32/WFC3.IR.G102.1st.sens.2.fits',
                                      'G141':'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G141.cal.V4.32/WFC3.IR.G141.1st.sens.2.fits'
                                     },
                ('HST','ACS','WFC'): {'G800L':'/Users/kbhirombhakdi/_work/_calib_files/ACS.WFC/ACS.WFC.1st.sens.7.fits'}
               }
        BKG = {('HST','WFC3','IR'): {'G102':'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G102.cal.V4.32/WFC3.IR.G102.sky.V1.0.fits',
                                     'G141':'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G141.cal.V4.32/WFC3.IR.G141.sky.V1.0.fits'
                                    },
               ('HST','ACS','WFC'): {(1):'/Users/kbhirombhakdi/_work/_calib_files/ACS.WFC/ACS.WFC.CHIP1.msky.1.fits',
                                    (2):'/Users/kbhirombhakdi/_work/_calib_files/ACS.WFC/ACS.WFC.CHIP2.msky.1.fits'
                                    }
              }
        FLAT = {('HST','WFC3','IR'): {'G102':'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G102.cal.V4.32/WFC3.IR.G102.flat.2.fits',
                                      'G141':'/Users/kbhirombhakdi/_work/_calib_files/WFC3.IR.G141.cal.V4.32/WFC3.IR.G141.flat.2.fits'
                                     },
                ('HST','ACS','WFC'): {(1):'/Users/kbhirombhakdi/_work/_calib_files/ACS.WFC/WFC.flat.cube.CH1.2.fits',
                                     (2):'/Users/kbhirombhakdi/_work/_calib_files/ACS.WFC/WFC.flat.cube.CH2.2.fits'
                                     }
               }
        TABLE = {'CONF':CONF, 'SENS':SENS, 'BKG':BKG, 'FLAT':FLAT}
        self.table = TABLE
        