from pySatlantic import instrument

# Data to test parsing of SatView Raw Files
TEST_DATA = ['test_data/HyperSAS009_20150728/HS_a0_t45_i45.raw',
             'test_data/ES187_20180814/ES187_20180814_2035.raw',
             'test_data/HTSRB007_20180814/HTSRB007_ES187_20180814_0824.raw',
             'test_data/HyperPro068_20180826/HyperPro068_ES187_20180826_2048.raw',
             'test_data/HyperNav001_20170809/HyperNav1_Multi1.raw',
             'test_data/HyperNav002_20170807/HyperNav2_MultiCast1.raw',
             'test_data/HyperPro012_20170808/HyperPro_MultiCast1.raw']
TEST_CAL = ['test_data/HyperSAS009_20150728/',                       # Optics Class 2015
            'test_data/ES187_20180814/',                             # EXPORTS 1
            'test_data/HTSRB007_20180814/HST007_18June26.sip',       # EXPORTS 1
            ['test_data/HyperPro068_20180826/MPR068_18Jan05.sip', 'test_data/HyperPro068_20180826/HSE0187_23Aug17.sip'], # EXPORTS 1
            'test_data/HyperNav001_20170809/',                       # Hawaii
            'test_data/HyperNav002_20170807/',                       # Hawaii
            ['test_data/HyperPro012_20170808/MPR0012_17Aug07.sip', 'test_data/HyperPro012_20170808/HSE0266_16Aug11.sip']]    # Hawaii
TEST_FRAME_TO_PARSE = [552,
                       141,
                       # 1,
                       # 1,
                       2135,
                       2282,
                       1]

if __name__ == '__main__':
    instrument.SatViewRawToCSV(TEST_CAL[2], TEST_DATA[2])