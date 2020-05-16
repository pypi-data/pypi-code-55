import dtit.pyCRCLib as crc
import numpy as np

print("-------------------------------")
print("Testing DTIT CRC Library")
print("-------------------------------\n")

# [01][04][00][0B][00][04] = [80][0B]
test_values = np.array([0x01, 0x04, 0x00, 0x0B, 0x00, 0x04]).astype(np.uint8)
crc16 = crc.pyMBCRC16(test_values)
olist = ' '.join('{:02X}'.format(a) for a in test_values)
print("pyMBCRC16([{:s}]) = {:02X} {:02X}, ground truth = 0x80, 0x0B\n".format(olist, crc16 & 0XFF, crc16 >> 8))

# [01][78][01][01][02][00][00][01][01] = [A9][63]
test_values = np.array([0x01, 0x78, 0x01, 0x01, 0x02, 0x00, 0x00, 0x01, 0x01]).astype(np.uint8)
crc16 = crc.pyMBCRC16(test_values)
olist = ' '.join('{:02X}'.format(a) for a in test_values)
print("pyMBCRC16([{:s}]) = {:02X} {:02X}, ground truth = 0xA9, 0x63\n".format(olist, crc16 & 0XFF, crc16 >> 8))

# [FF][FE][01][13][00][00][00][11] [00][56][32][2E][31][30][00][00] [00][00][00][00][00][00][00][00] [00]
# = [16][47]
dlist = [0xff, 0xfe, 0x01, 0x13, 0x00, 0x00, 0x00, 0x11, 0x00, 0x56, 0x32, 0x2e, 0x31, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
test_values = np.array(dlist).astype(np.uint8)
crc16 = crc.pyNBCRC16(test_values)
olist = ' '.join('{:02X}'.format(a) for a in test_values)
print("pyNBCRC16([{:s}]) = ".format(olist))
print("{:02X} {:02X}, ground truth = 0x16, 0x47\n".format(crc16 >> 8, crc16 & 0XFF))

# 44 54 00 0A 00 00 00 15 FF FF 00 00 0A 81 13 4E 00 12 00 17 02 E8 01 40 02 EA 5D 00 00
# = [BD][15]
dlist = [0x44, 0x54, 0x00, 0x0a, 0x00, 0x00, 0x00, 0x15, 0xff, 0xff, 0x00, 0x00, 0x0a, 0x81, 0x13, 0x4e, 0x00, 0x12, 0x00, 0x17, 0x02, 0xe8, 0x01, 0x40, 0x02, 0xea, 0x5d, 0x00, 0x00]
test_values = np.array(dlist).astype(np.uint8)
crc16 = crc.pyNBCRC16(test_values)
olist = ' '.join('{:02X}'.format(a) for a in test_values)
print("pyNBCRC16([{:s}]) = ".format(olist))
print("{:02X} {:02X}, ground truth = 0xBD, 0x15\n".format(crc16 >> 8, crc16 & 0XFF))

# 4454210100000000
dlist = [0x44, 0x54, 0x21, 0x01, 0x00, 0x00, 0x00, 0x00]
test_values = np.array(dlist).astype(np.uint8)
crc16 = crc.pyNBCRC16(test_values)
olist = ' '.join('{:02X}'.format(a) for a in test_values)
print("pyMBCRC16([{:s}]) = {:02X} {:02X}\n".format(olist, crc16 >> 8, crc16 & 0XFF))

# 44542102000000080000000000000000
dlist = [0x44, 0x54, 0x21, 0x02, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
test_values = np.array(dlist).astype(np.uint8)
crc16 = crc.pyNBCRC16(test_values)
olist = ' '.join('{:02X}'.format(a) for a in test_values)
print("pyMBCRC16([{:s}]) = {:02X} {:02X}\n".format(olist, crc16 >> 8, crc16 & 0XFF))

print("-------------------------------")