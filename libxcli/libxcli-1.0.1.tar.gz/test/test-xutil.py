from xcommon.utils import *
from xcommon.xclient import *


import struct;
import binascii

# 
# 
# 




 
buff = XBuffer.Buffer()

 
buff.putString('1234567890abcdeffedcba0987654321qwe')

print('length is' + str(buff.length()));
cr32 = XUtil.crc32(buff.array(), 0, buff.length());
print('crc32 %d' % (cr32))
cr32 = binascii.crc32( buff.array() )
print('crc32 %d' % (cr32))

# 
XUtil.dump(buff.array(), 0, buff.length())

#c = XClient.Utils.packet( buff, 100, 'aaaaaaaaaaaaaaaaaaaa' )


buff.position();

i32 = buff.getInt32()
print('32 is ' + str(i32))

i32 = buff.getInt32()
print('32 is %x' % (i32))


buff.position();
s = buff.getString();
print('s is >>' + s + '<<');

buff.reset();
buff.putInt16(0x12);
 
i16 = buff.getInt16();
print('16 is %x' % (i16))



buff.reset();
buff.putInt64(0x12345678abcdef);
 
i64 = buff.getInt64();
print('64 is %x' % (i64))



buff2 = bytearray(20)
buff = bytearray(10);

buff[0] = 1 ;

print(buff);

print(len(buff));
# buff.join( 'abccccccccc' )

b1 = buff.extend(buff2)

print(buff);


intBytes = struct.pack("!i", 0x1234ABCD);


off = 4 ;
for i in range(4):
    buff[off+i] = intBytes[i]


print(len(buff))
print(buff)

XUtil.dump(buff);





